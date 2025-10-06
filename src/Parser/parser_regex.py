"""
This file defines the grammar for parser of regular expressions.
It is useful for manipulating RE and transform them to automata
"""

import logging
import Parser.AST as ast
from lark import Lark, Transformer, v_args
logging.basicConfig(level=logging.DEBUG)


# the grammar for regular expressions
grammar = """
    ?start: union
    
    ?union:  conc
          | union "+" conc ->  union

    ?conc: star
         | conc "." star ->  concatenation

    ?star: atom "*" -> star
         | atom

    ?atom: var  
         | "(" union ")"
        
    var: /[a-zA-Z_][a-zA-Z0-9_]*/   // Variable: alphanumeric starting with a letter

    %import common.WS
    %ignore WS
"""

@v_args(inline=True)

class ASTTransformer(Transformer) :
    union = ast.Union
    star = ast.Star
    concatenation = ast.Concatenation
    var = ast.RegexVar
    

# a function to parse a string, it returns an AST
def parse(regex) :
    regex_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree = regex_parser.parse(regex)
    return ASTTransformer().transform(tree)

def tests() :
    form1 = "a"
    form2 = "(a+b)*"
    form3 = "a.b + a.(c+d)*"
    

    reg_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    fparser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree1 = reg_parser.parse(form1)
    print(ASTTransformer().transform(tree1))

    tree2 = reg_parser.parse(form2)
    print(ASTTransformer().transform(tree2))

    tree3 = reg_parser.parse(form3)
    print(ASTTransformer().transform(tree3))
    

if __name__ == "__main__" :
    tests()


