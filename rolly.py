
import sys
from XETLlexer.lexer import lexer
from XETLparser.operations import parser_tree
from XETLcore.utils.graph_tree import Tree_XETLtree
import sys
sys.setrecursionlimit(5000)

if __name__ == '__main__':
    a = """IF(1.2 > 1;  {}; "NOT")"""
    b = """IF(1.2 > 1;  {}; "NOT")"""
    for _ in range(0, 201
                   ):
        print(_)
        print(a)
        b = a.format(b)

    text_nested = b.replace('{}', "OK")


    tokens = lexer(text_nested)
    parse_result = parser_tree(tokens)
    if not parse_result:
        print('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    # Tree_XETLtree(ast, 'tree.png')


