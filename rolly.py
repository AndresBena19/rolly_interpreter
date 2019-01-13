import sys
from parser import *
from lexer import *
from graph_ast import Aritmetic_Exp, Tree_Program, IfExp

from anytree.exporter import DotExporter

if __name__ == '__main__':

    test_date  = """
                    A:= 2+1
                """

    tokens = rolly_lex(test_date)
    parse_result = rolly_parser(tokens)
    if not parse_result:
        print('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    # Generate graph base on the ast
    ast_g = Tree_Program(ast)

    env = {}
    ast.eval(env)

    print(env)
