"""
    This class implement a standard way of translating regexp to NFA it uses the visitor pattern for 
    mimicking recurrence.
"""
import sys
sys.path.insert(1, '../Parser')
import Parser.AST
import Parser.parser_regex as parser
import NFA.regex_visitor as visitor
import NFA.NFA as nfa
from lark import Lark, Transformer, v_args


class TranslateToNFA(visitor.RegexVisitor) :
    
    def __init__(self, alphabet) :
        self.translate = {}
        self.number_states = 0
        self.alphabet = alphabet # we consider the alphabet as a paramter, if this is empty it will completed by the visitor

    def generate_state(self) :
        """ Method to obtain new states """
        result = f"""q{self.number_states}"""
        self.number_states = self.number_states + 1
        return result

    def visit_regexvar(self, var) :
        """ This generates the automaton for a regexvar"""
        # the initial and final states are defined
        init_state = self.generate_state()
        final_state = self.generate_state()

        # the automaton states are defined
        states = { init_state, final_state }

        # the alphabet is defined
        #alphabet = { str(str(var)) }
        self.alphabet.add(str(str(var)))

        #the transitions are defined
        transitions = { (init_state, str(str(var))) : {final_state} }
        final_states = { final_state }
        result_nfa = nfa.NFA(str(var), states, self.alphabet, transitions, init_state, final_states)
        self.translate[str(str(var))] = result_nfa

    def visit_union(self, union) :
        init_state = self.generate_state()
        #final_state = self.generate_state()

        nfa_left = self.translate[str(union.left)]
        nfa_right = self.translate[str(union.right)]
        states = nfa_left.states.union(nfa_right.states) # we assume that there are no state collision 
        states.add(init_state)
        #states.add(final_state)

        transitions = {}
        transitions[(init_state,'')] = set()
        transitions[(init_state,'')].add(nfa_left.start_state)
        transitions[(init_state,'')].add(nfa_right.start_state)
        
        transitions.update(nfa_left.transitions)
        transitions.update(nfa_right.transitions)
        #final_states = { final_state }
        final_states = nfa_left.accept_states.union(nfa_right.accept_states)
        #alphabet = nfa_left.alphabet.union(nfa_right.alphabet)
        # we assume the alphabet are already constructed
        self.translate[str(union)] = nfa.NFA(str(union), states, self.alphabet, transitions, init_state, final_states)

    def visit_concatenation(self, concat) :
        left_nfa = self.translate[str(concat.left)]
        right_nfa = self.translate[str(concat.right)]
        
        init_state = left_nfa.start_state
        states = left_nfa.states | right_nfa.states # the union of the states
        #alphabet = left_nfa.alphabet | right_nfa.alphabet # the union of the alphabet
        final_states = right_nfa.accept_states
        transitions = {}
        transitions.update(left_nfa.transitions)
        transitions.update(right_nfa.transitions)
        for state in left_nfa.accept_states :
            if transitions.get((state, '')) :
                transitions[(state, '')].add(right_nfa.start_state)
            else :
                transitions[(state, '')] = { right_nfa.start_state }
        self.translate[str(concat)] = nfa.NFA(str(concat), states, self.alphabet, transitions, init_state, final_states)

    def visit_star(self, star) :
        inner_nfa = self.translate[str(star.regex)]
        init_state = inner_nfa.start_state
        states = inner_nfa.states
        final_states = inner_nfa.accept_states.union({ init_state })
        transitions = inner_nfa.transitions
        for state in final_states :
            if transitions.get((state,'')) :
                transitions[(state,'')].add(init_state)
            else :
                transitions[(state,'')]= { init_state }
        #alphabet = inner_nfa.alphabet
        self.translate[str(star)] = nfa.NFA(str(star), states, self.alphabet, transitions, init_state, final_states)

# Some basic tests
def test1() :
    form1 = "a"
    form2 = "(a+b)*"
    form3 = "a.b + a.(c+d)*"
    
    ast1 = parser.parse(form1)
    re_visitor = TranslateToNFA(set())
    ast1.accept(re_visitor)

    nfa = re_visitor.translate[form1]
    print(nfa.toPrism())
    nfa.remove_epsilon()
    print(nfa.toPrism())

def test2() :
    re = "(a + b)*"
    
    ast1 = parser.parse(re)
    re_visitor = TranslateToNFA(set())
    ast1.accept(re_visitor)

    nfa = re_visitor.translate[re]
    print(nfa)
    #print(nfa.toPrism())
    #print(re_visitor.translate.keys())
    nfa.remove_epsilon()
    print(nfa)
    #print(nfa.toPrism())


def test3() :
    re = "a . b + a . (c + d)*"
    #re = "a . b"
    ast1 = parser.parse(re)
    re_visitor = TranslateToNFA(set())
    ast1.accept(re_visitor)

    nfa = re_visitor.translate[str(ast1)]
    print(nfa.toPrism())
    #print(nfa)
    nfa.remove_epsilon()
    print(nfa.toPrism())

if __name__ == "__main__" :
    test2()