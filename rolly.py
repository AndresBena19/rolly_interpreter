import sys
from parser import *
from lexer import *
from graph_ast import Aritmetic_Exp, Tree_Program, IfExp

from anytree.exporter import DotExporter

if __name__ == '__main__':
    test_date = """
                z := "1992/12/11":
                
                format := "YYYY/MM/DD":
                a:= date(1999/12/27, format):
                b:= date(1996/12/27, format):
                w:= date(1999/12/27, format) - date(1996/12/27, format) :
                result := if (a = b; "True"; 'False')
                
                """


    test_ast = """                
                    format := "YYYY/MM/DD":
                    a := 3 * 2 + 1 / 2:
                    b:= date(1996/12/27) - date(2018/12/28)
                
                    """
    test_if = """
                format := "YYYY/MM/DD":
                if(not(not a > b or not date(1996/12/27) = 3) ; 
                        y:="True"
                      
                        ;
                                 y:="False")
                
                
                """
    text_aritmetic = """a := 3+2.4*1+6 + (3*3-2/(5*3))"""
    test = """a := 4 * (2 + 1)"""
    text_nested = """
                    y := 5:
                    if(1.1 > 1 and  2=4;
                     y := 1;
                      if(3.0 >= 2 and 2=2; y := 'ssad'))
                  """


    final = """ 
            result := if(False; "True"; if(True; "TRUE LOVE"; "False"))
            """

    test_nested = """
                  f := ((a+b-a*(2/2)) = 2 or True) and True:
                  if(not (f and False);
                                      if(True;
                                             if(False; 
                                                    result:="WIN";
                                             result:="NOT HERE"));
                  result:="GAME OVER")
                  """

    test_date_t = """
                  format := "DD/MM/YYYY":
                  fecha := "8/12/1996":
                  a:= date("8/12/1996", format)
                  """

    test_bool = """
               a := date(1999/12/27, "YYYY/MM/DD"):
               b :=  date(2018-12-27, "YYYY-MM-DD"):
               pedro := not( not (a < b or True)):
               f:=3:
               h:=5:
               c := f+h
               """

    tokens = rolly_lex(test_bool)
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
