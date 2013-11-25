from unittest import TestCase


class SafeExpressionTest(TestCase):
    def test_base(self):
        EXPRESSIONS = (
                ('2 %s 3', (('+', 5),
                          ('-', -1),
                          ('*', 6),
                          ('/', 2/3),
                          ('^', 1),
                          ('%', 2),
                          ('or', 2),
                          ('and', 3),
                          ('|', 3),
                          ('&', 2))),
                ('(1,2,3)[2]', 3),
        )

        from safe_expression import SafeExpression
        for template, parameters in EXPRESSIONS:
            if not isinstance(parameters, tuple):
                parameters = (((), parameters),)
            for parameter, result in parameters:
                expression = template % parameter
                se = SafeExpression(expression)
                self.assertEqual(se(), result)

    def test_pickle(self):
        from safe_expression import SafeExpression
        import pickle

        se = SafeExpression('1+1')
        self.assertEqual(se(), 2)
        d = pickle.dumps(se)
        se2 = pickle.loads(d)
        self.assertEqual(se2(), 2)


