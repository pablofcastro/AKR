"""
    This class implement the main procedure of the model checking
"""
import sys
sys.path.insert(1, './Parser')
import AST
import parser_regex as parser
import form_visitor as visitor
import NFA as nfa
from lark import Lark, Transformer, v_args


class ModelCheck(visitor.FormulaVisitor) :
    
    def __init__(self) :
        self.to_states = {} # this dictionary symbolically relates every subformula with the states that hold that formula

    def visit_var(self, var) : 
        self.to_states[str(var)] = str(var) # each var characterizes itself

    def visit_or(self, disj) :
        self.to_states[str(disj)] = f""" {str(disj.left)} | {str(disj.right)}""" 
    
    def visit_and(self, conj) :
        self.to_states[str(conj)] = f""" {str(conj.left)} & {str(conj.right)}""" 
    
    def visit_not(self, neg) :
        self.to_states[str(neg)] = f""" ! {str(neg.operator)} """ 

    