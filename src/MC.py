"""
    This class implement the main procedure of the model checking
"""
import sys
sys.path.insert(1, './Parser')
sys.path.insert(1, './Prism')
import AST
import PrismModel as prism
import form_visitor as visitor
import NFA as nfa
import sys, os, subprocess, csv, re, signal # needed for the system calls
import traceback
import re
from pathlib import Path

class ModelCheck(visitor.FormulaVisitor) :
    
    def __init__(self, model, prism_path, file, verbosity=0, plan=False, plan_path="") :
        """
            the constructor for this class:
                model: this is a dictionary where:
                    model["plts"] = this contains the plts in prism notation
                    model["perceptions"] =  this contains a list of perceptions (NFAs)
                prism_path: this is the path to prism
                file: the file where the prism model is
                verbosity: the verbosity level
                plan: if a plan should be printed or not
                plan_path: if a plan is requested a path to where to store the plan should passed
        """
        self.to_states = {} # this dictionary symbolically relates every subformula with the states that hold that formula
        self.model = model # model contains all the information about the model, the prism model and the perceptions as prism models
        self.prism_path = prism_path
        self.file = file # the file where the prism model is
        self.witness = "" # the witness for the property, if there is one
        self.verbosity = verbosity # the verbosity level
        self.plan = plan # if a plan should be obtained
        self.plan_path = plan_path # the path where the plan where be saved

    def __prism_call__(self, model, property, plan=False) :
        """
            Private method that calls prism and model checks property "property" in model "model"
        """
        verbosity = 0
        command = self.prism_path+"/bin/prism"
        with open(self.file, 'w') as f :
            f.write(model)
        row = {} # the results are saved to a dictionary
        if (self.verbosity >= 5) :
            print(model)
            print(property)
        try :
            if not self.plan :
                result = subprocess.run([command, self.file, '-pf', property], capture_output=True).stdout.decode()
            else :
                result = subprocess.run([command, self.file, "-pf", property, "-exportstrat", str(Path(self.plan_path) / "strat.txt"), "-exportstates", str(Path(self.plan_path) / "states.txt")], capture_output=True).stdout.decode()
                #process = subprocess.Popen([command, self.file, "-pf", property, "-exportstrat", str(Path(self.plan_path) / "strat.txt"), "-exportstates", str(Path(self.plan_path) / "states.txt"),], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                #result, stderr = process.communicate()
            if (self.verbosity >= 5) :
                print(result)
            for line in result.splitlines() :
                words = line.split()
                if line.startswith("States") : 
                    row["states"] = words[1]
                elif line.startswith("Transitions") : 
                    row["transitions"] = words[1]
                elif line.startswith("Result") : 
                    row["result"] = words[1]
                elif line.startswith("Time") :
                    row["time"] = words[4]
        except Exception:
            print(Exception)
            traceback.print_exc()
        return row

    def ___read_plan__(self) :
        """
            Reads a plan if one is requested
        """
        states = [] # a list to save the states, each state is repesented as a dictionary
        try : 
            with open(self.plan_path+'states.txt', "r") as file:
                content = file.read()
                start_line = content.splitlines()[0]
                match = re.match(r"\((.*?)\)", start_line) # we extract the attributes from the tuples
                if match:
                    attributes = [p.strip() for p in match.group(1).split(",")]
        except  :
            print("Error reading the states file.")
        

        try : 
            with open(self.plan_path+'strat.txt', "r") as file:
                for line in file :
                    state = {}
                    match = re.match(r"\((.*?)\)\s*=\s*(.*)", line)
                    values =  [p.strip() for p in match.group(1).split(",")]
                    for att,val in zip(attributes, values) :
                        if (att != "state") :
                            state[att] = val
                    state["action"] = match.group(2).strip()
                    states.append(state)
        except : 
            print("Error reading the plan file.")
        return states

    def get_states(self, property) :
        """ 
            It returns the states satisfying a property, it uses the last model saved
        """
        list_states = [] # the list of states satisfying the property
        command = self.prism_path+"/bin/prism"
        try :
            result = subprocess.run([command, self.file, '-pf', f"""filter(print,{property})"""], capture_output=True).stdout.decode()
            found = False
            for line in result.splitlines() :
                if line.startswith("Satisfying states") :
                    found = True
                    continue
                if line.startswith("Property satisfied") :
                    found = False
                if found & (line != ""):
                    words = line.split()
                    list_states.append(words[0])
        except Exception:
            print(Exception)
            traceback.print_exc()
        return list_states

    def visit_var(self, var) : 
        self.to_states[str(var)] = str(var) # each var characterizes itself

    def visit_or(self, disj) :
        if self.to_states[str(disj.left)] == "true" or self.to_states[str(disj.right)] == "true" :
            self.to_states[str(disj)] = "true"
        elif self.to_states[str(disj.left)] == "false" and self.to_states[str(disj.right)] == "false" :
            self.to_states[str(disj)] = "false"
        else :
            self.to_states[str(disj)] = f""" {self.to_states[str(disj.left)]} | {self.to_states[str(disj.right)]} """ 
    
    def visit_and(self, conj) :
        if self.to_states[str(conj.left)] == "true" and self.to_states[str(conj.right)] == "true" :
            self.to_states[str(conj)] = "true"
        elif self.to_states[str(conj.left)] == "false" or self.to_states[str(conj.right)] == "false" :
            self.to_states[str(conj)] = "false"
        else :
            self.to_states[str(conj)] = f""" {self.to_states[str(conj.left)]} & {self.to_states[str(conj.right)]} """ 
        
    def visit_not(self, neg) :
        if self.to_states[str(neg.operand)] == "true" :
            self.to_states[str(neg)] = "false"
        elif self.to_states[str(neg.operand)] == "false" :
            self.to_states[str(neg)] = "true"
        else :
            self.to_states[str(neg)] = f""" ! {str(neg.operand)} """ 

    def visit_kh(self, kh) :
        # to check Kh(A,B) :
        # We have to get the states satisfying A (s_A)
        # We have to get the states satisfying B (G)
        # For every perception P_i
        # we have to build  M' = M x P_i extended witht S_A (initial states)
        # check inf P_{M'}(G \times F_i) >= q for some i

        # we define the initial states
        init_states = "init : \n" + self.to_states[str(kh.left)]

        # by default the formula is evaluated to false
        self.to_states[str(kh)] = "false"

        # for every perception we check if the formula holds
        for perception,regex in self.model["perceptions"] :
            # we define the initial states
            init_states = "init  \n ("+self.to_states[str(kh.left)] + ") & " + f"""(state={perception.states_index[perception.start_state]})\nendinit"""

            # we construct the model
            #model = self.model["plts"]+"\n"+perception.toPrism()+"\n"+init_states # we construct the model

            module_system = prism.PrismModel(self.model["plts"])
            module_percep = prism.PrismModel(perception.toPrism())
            model = str(module_system.cross_product(module_percep))+"\n"+init_states # we construct the model

            end_states = " | ".join([f"""state={perception.states_index[end_state]}""" for end_state in perception.accept_states])
            # we define the property
            property = f"""Pmin=?[F ({self.to_states[str(kh.right)]} & ({end_states}))]>={kh.lb}"""

            # we call the model checker
            output = self.__prism_call__(model, property)
            if output["result"] == "true" :
                self.to_states[str(kh)] = "true"
                self.witness = str(regex) # we save the regexp that makes true the property
                if (self.plan) : # if a plan was requested
                    self.plan = self.___read_plan__()
                break # a perception that makes true the formula was found

