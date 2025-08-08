"""
This file defines the grammar for the parser of the model checker.

A *model* is defined consists of three parts:

* the *PLTS*  part which defines an MDP,
* the *perception* part that defines the preception of the agent(s),
* the property to be checked.

The grammar identifies these two parts. The PLTS part is written in Prism 
notation, here it is only a text that is passed to PRISM
The preception part is defined as a sequence of regular expressions
"""

import logging
import AST as ast
from lark import Lark, Transformer, v_args
logging.basicConfig(level=logging.DEBUG)

# the grammar for formulas
grammar = """
    ?start:  "plts" ":" model  "perception" ":" regs "endperception" "property" ":" form "endproperty" -> spec
    
    ?model:   STRING -> plts

    ?property: form -> property

    ?regs: regex (";" regex)* -> perception

    ?regex: union

    ?union:  conc
          | union "+" conc -> union

    ?conc: star
         | conc "." star ->  concatenation

    ?star: atom
         | atom "*" -> star

    ?atom: var -> var
         | "(" union ")"  
    
    ?form: conj

    ?conj: disj
         | conj "&&" disj -> conj

    ?disj: elem
         | disj "||" elem -> disj

    ?elem: "!" elem -> neg
         | var      -> bool_var
         | "true"   -> true
         | "false"  -> false
         | "(" form ")"
         | "Kh" "(" form "," form ")" ">=" cons -> kh

     ?cons : constant -> constant

    var: /[a-zA-Z_][a-zA-Z0-9_]*/   // Variable: alphanumeric starting with a letter
    constant: /-?\d+(\.\d+)?([eE][+-]?\d+)?/  // Constants in decimal notation
    STRING:  /(.|\\n|\\r)+/ "endplts"
    
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""
@v_args(inline=True)

class ASTTransformer(Transformer) :
    spec = ast.Spec
    plts = ast.PrismModel
    property = ast.Property
    perception = ast.Perception
    union = ast.Union
    star = ast.Star
    concatenation = ast.Concatenation
    var = ast.RegexVar
    conj = ast.And
    disj = ast.Or
    neg =  ast.Not
    bool_var = ast.Var 
    kh = ast.Kh
    constant = ast.Constant
    
# a function to parse a string, it returns an AST
def parse(regex) :
    regex_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree = regex_parser.parse(regex)
    return ASTTransformer().transform(tree)

# a basic test
def test() :
    example1 = """plts: 
                    module system v : [0..1] init 0; 
                         [a] v = 0 -> 0.5:v'=1 + 0.5:v'=0 
                 endplts
                 perception : a*
                 endperception
                 property : Kh(!v,v) >= 1.0
                 endproperty""" 
    
    example2 = """plts: 
                     dsafdsa 
                     gjhggh
                     khjhh
                  endplts
                 perception : a*
                 endperception
                 property : Kh(p,q) >= 0.5
                 endproperty""" 

    ast = parse(example1)
    print(ast)
    
if __name__ == "__main__" :
    test()




