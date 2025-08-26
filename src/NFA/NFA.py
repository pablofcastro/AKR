class NFA:
    """
        This class provides an implementation of Non-Deterministic Automata with epsilon transition.
        The epsilon symbol is represented with '' character.
    """

    def __init__(self, name, states, alphabet, transitions, start_state, accept_states):
        """ The name, states, alphabet, transitions, start_state, accept_states, are initiliazed"""
        self.name = name 
        self.states = states  # set of states
        self.alphabet = alphabet  # set of symbols (excluding epsilon)
        self.transitions = transitions  # dict: (state, symbol) -> set of states
        self.start_state = start_state # the start state
        self.accept_states = accept_states  # set of accepting states
        self.states_index = {st:i for i,st in enumerate(states)} # an enumaration of the states, useful for tranlating the automata to PRISM code
        self.trap_state = "" # the trap state if this exists

    def add_transitions(self, state, symbol, succ_states) :
        """ 
            A simple method for adding a set of transitions to the NFA:
            state: the origin state
            symbol: the symbol that observe the transition
            succ_states: the succesors added for the given transition
        """
        # a transtion exists
        if self.transitions.get((state, symbol)) : # if the transition exists
            self.transitions[(state, symbol)].update(succ_states)
        else : # if the transition does not exist
            self.transitions[(state, symbol)] = set() # a new set is created
            self.transitions[(state, symbol)].update(succ_states) # the elements are added to the set

    def remove_state(self, state) :
        """ Remove the given state from the NFA """
        # first, we remove the transitions
        for st, symbol in list(self.transitions.keys()) :
            if st == state :
                del self.transitions[(st, symbol)]

        # the state is removed
        self.states.discard(state)

    
    def closure(self, states) :
        """ It computes the closure of a set of states """
        stack = list(states) # the stack is initialised with the initial state
        closure = set(states) # this is a reflexo-transitive closure
        while stack:
            origin = stack.pop()
            for st, symbol in self.transitions.keys() :
                if st == origin :
                    for next_state in self.transitions.get((origin, symbol)) :  
                        if next_state not in closure :
                            closure.add(next_state)
                            stack.append(next_state)
        return closure
    
    def remove_disconnected(self) :
        """ Removes the disconnect components of the NFA """
        reachable = self.closure({ self.start_state })
        for state in self.states.difference(reachable) :
            self.remove_state(state)

    def epsilon_closure(self, states):
        """Returns the epsilon-closure of a given state, a stack is used instead of recurrence.
           state: the state for which the closure is computed
        """
        stack = list(states) # the stack is initialised with the initial state
        closure = set()
        while stack:
            origin = stack.pop()
            if self.transitions.get((origin, '')) :
                for next_state in self.transitions.get((origin, '')):  # '' represents epsilon
                    if next_state not in closure :
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def remove_epsilon(self) :
        """ Removes the epsilon transitions from every state, it first computes the closure and then removes the epsilon transitions """
        # if a state reaches a accept states by epsilon closure, then it is accepting too
        for state in self.states :
            if bool(self.epsilon_closure({state}).intersection(self.accept_states)) :
                self.accept_states.add(state)

        for state in self.states :
            for succ_state in self.epsilon_closure({state}) :
                for symbol in self.alphabet :
                    if self.transitions.get((succ_state, symbol)) : # if there is a transition 
                        self.add_transitions(state, symbol, self.transitions[(succ_state, symbol)]) # we add al the transitions with symbols to the NFA

        for state, symbol in list(self.transitions.keys()) : # epsilon trnasitions are removed
            if symbol == '' :
                del self.transitions[(state,symbol)]

        # the disconnected parts are removed
        self.remove_disconnected()

        # we reindex the states
        self.states_index = {st:i for i,st in enumerate(self.states)}

    def complete(self) :
        """
            This method completes the NFA adding an trap state
        """
        # we add a new trap state
        self.trap_state = "qtrap"
        assert not (self.trap_state in self.states)

        self.states.add(self.trap_state)
        # we complete the transitions, including the one for the trap state
        for state in self.states :
            for symbol in self.alphabet :
                if not ((state, symbol) in self.transitions) :
                    self.transitions[(state, symbol)] = { self.trap_state }
        
        # we reindex the states
        self.states_index = {st:i for i,st in enumerate(self.states)}


    def move(self, states, symbol):
        """Returns the set of states reachable from any of the input states using the given symbol."""
        result = set()
        for state in states:
            result.update(self.transitions.get((state, symbol)))
        return result

    def accepts(self, input_string):
        """Checks if the NFA accepts the input string."""
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
        return any(state in self.accept_states for state in current_states)
    
    def toPrism(self) :
        """ 
            Returns a PRISM representation for the current automata
        """
        # we index the states
        #state_index = { s:i for i,s in enumerate(self.states)}
        #print(state_index)

        # the automata are translate to an MDP in PRISM, the representation is a follows:
        # A transition delta(i, s) = {j0,...,jn}, is represented as a set of transitions:
        # [s] state=i -> 1 : state=j0
        #  ...
        # [s] state=i -> 1: state=jn
        result = (
                  f"""  module perception\n"""
                  f"""      state : [0..{len(self.states)-1}];\n"""
                  f"""      accept : [0..1];\n"""
            #      f"""      state : [0..{len(self.states)-1}] init {self.states_index[self.start_state]};\n"""
            #      f"""      accept : [0..1] init {1 if self.start_state in self.accept_states else 0};\n"""
                 )
        
        for state,simbol in self.transitions.keys() :
            for succ in self.transitions[(state, simbol)] :
                result = result + f"""      [{simbol}] (state={self.states_index[state]}) -> 1: (state' = {self.states_index[succ]}) & (accept'={1 if succ in self.accept_states else 0});\n"""
        result = result + " endmodule"
        return result

    def fromRegExp(ast) :
        """
            Constructs an automata corresponding to a regular expression
        """
        pass

    def __str__(self):
        return f"""(\n{self.states}, \n {self.transitions},\n {self.alphabet},\n {self.start_state},\n {self.accept_states}\n)"""
        
def test1() :
    """ A simple test """
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        ('q0', ''): {'q1'},
        ('q1', 'a'): {'q1', 'q2'},
        ('q1', 'b'): {'q1'}
    }
    start_state = 'q0'
    accept_states = {'q2'}

    nfa = NFA("foo", states, alphabet, transitions, start_state, accept_states)

    test_strings = ['a', 'ab', 'aa', 'b', 'aab', '']
    for s in test_strings:
        result = nfa.accepts(s)
        print(f"Input: {s!r} -> {'Accepted' if result else 'Rejected'}")

def test2() :
    """ A simple test """
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        ('q0', 'a'): {'q1'},
        ('q1', 'a'): {'q1', 'q2'},
        ('q1', 'b'): {'q1'}
    }
    start_state = 'q0'
    accept_states = {'q2'}

    nfa = NFA("foo", states, alphabet, transitions, start_state, accept_states)
    nfa.complete() # we complete the NFA
    print(nfa)

if __name__ == "__main__":
    test2()