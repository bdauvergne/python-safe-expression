import ast
import __builtin__

__all__ = ()

class InvalidExpression(Exception):
    def __init__(self, s, offset):
        self.args = (s, offset)
        self.offset = offset

class SafeNodeVisitor(ast.NodeVisitor):
    __SAFE_NODES = (
            ast.boolop,
            ast.cmpop,
            ast.expr,
            ast.slice,
            ast.unaryop,
            ast.operator,
            ast.Load,
    )
    __FORBIDDEN_NODES = (
            ast.Call,
    )

    def is_safe(self, node):
        return isinstance(node, self.__SAFE_NODES) and not isinstance(node, self.__FORBIDDEN_NODES)

    def generic_visit(self, node):
        if not self.is_safe(node):
            raise InvalidExpression("forbidden token %s" % node.__class__.__name__, node.col_offset)
        super(SafeNodeVisitor, self).generic_visit(node)

class NamesVisitor(ast.NodeVisitor):
    def __init__(self, collect=None):
        self.names = set() if collect is None else collect

    def visit_Name(self, node):
        self.names.add(node.id)

class SafeExpression(object):
    def __init__(self, s):
        self.st = self.__parse(s)
        self._code = None

    def __parse(self, s):
        if len(s.splitlines()) > 1:
            raise ValueError("newline forbidden")
        st = ast.parse(s)
        if not isinstance(st, ast.Module) or not len(st.body) == 1 or not isinstance(st.body[0], ast.Expr):
            raise ValueError('invalid expression')
        value = st.body[0].value
        visitor = SafeNodeVisitor()
        visitor.visit(value)
        return ast.Expression(value)

    def names(self):
        visitor = NamesVisitor()
        visitor.visit(self.st)
        return visitor.names

    @property
    def code(self):
        if not self._code:
            self._code = __builtin__.compile(self.st, '<source>', 'eval')
        return self._code

    def __getstate__(self):
        d = self.__dict__.copy()
        d['_code'] = None
        return d

    def __call__(self, **kwargs):
        var = {name: None for name in self.names()}
        var.update(kwargs)
        return eval(self.code, {'__builtin__': None}, var)

if __name__ == '__main__':
    while True:
        s = raw_input('> ')
        if not s:
            continue
        try:
            print SafeExpression(s)()
        except InvalidExpression, e:
            print ' ' * e.offset, '^'
            print '!Invalid expression!'
        except SyntaxError, e:
            print ' ' * e.offset, '^'
            print e.lineno
            print e.offset
            print '!SyntaxError!'
