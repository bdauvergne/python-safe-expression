#!/usr/bin/python
from setuptools import setup, find_packages, Command
from unittest import TextTestRunner, TestLoader
from os.path import dirname
import os

class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests and runs them.
        '''
        base = dirname(__file__)
        tests = TestLoader().discover(base)
        t = TextTestRunner(verbosity = 4)
        t.run(tests)

setup(name='safe_expression',
        version='1',
        license='MIT',
        description='Safe expression evaluator',
        url='https://github.com/bdauvergne/python-safe-expression',
        author='Benjamin Dauvergne',
        author_email='bdauvergne@entrouvert.com',
        packages=find_packages(os.path.dirname(__file__) or '.'),
        cmdclass={'test': TestCommand})
