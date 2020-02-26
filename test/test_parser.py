import unittest
import sys
from XETLlexer.lexer import lexer
from XETLparser.operations import parser_tree


class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.setrecursionlimit(5000)

    @classmethod
    def tearDownClass(cls):
        sys.setrecursionlimit(1000)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_deep_nested_operation(self):
        a = """IF(1.2 > 1;  {}; "NOT")"""
        b = """IF(1.2 > 1;  {}; "NOT")"""
        for _ in range(0, 200):
            b = a.format(b)

        text_nested = b.replace('{}', "OK")
        tokens = lexer(text_nested)
        parser_tree(tokens)