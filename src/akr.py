"""
    Main script the AKR tool
"""
import argparse, os
import sys
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
print(script_dir)
relative_file_path_parser = os.path.join(script_dir, 'Parser')
relative_file_path_nfa = os.path.join(script_dir, 'NFA')
#sys.path.insert(1, './Parser')
sys.path.insert(1, relative_file_path_parser)
#sys.path.insert(1, './NFA')
sys.path.insert(1, relative_file_path_nfa)
import AST
import parser as model_parser
import translator_regexp_nfa as translator
import MC as mc
import time
import subprocess

verbosity = 0 # a global variable for the verbosity

def validate_file(f):
    if not os.path.exists(f):
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError(f"Couldn't find {f}.")
    return f

def main() :
    """ This is the main function of the tool
        the options can be:
        + --help: shows the options
        + --file (-f): process a file
    """
    verbosity = 0 # the verbosity level, it is useful for testing
    prism_path = "../prism/prism"
    parser = argparse.ArgumentParser()
    spec_file_name = "temp/model.prism" # this is the file where the model is stored,
    # create the arguments for the command line  
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", dest="verbosity", type=int, metavar="VERBOSITY")
    parser.add_argument("-i", "--input", dest="file", required=True, type=validate_file,
                        help="The file with the model", metavar="FILE")  
    parser.add_argument("-a", "--alphabet", dest="alphabet", required=False, type=str,
                        help="The alphabet considered", metavar="ALPHABET")
    parser.add_argument("-pp", "--prism-path", dest="prism", required=False, type=str,
                        help="The path to prism tool, by default is ../prism/prism/", metavar="PRISMPATH")
    args = parser.parse_args()

    try :
        file = open(args.file, "r")
    except OSError:
        print(f"Error: Couldn't open input file")
        sys.exit()

     # we parse the alphabet, empty if no alphabet is given
    input_alphabet = []
    if args.alphabet is not None :
        input_alphabet = args.alphabet.split(',')
    
    # check for verbosity argument
    if args.verbosity is not None :
        verbosity = args.verbosity
        print("The verbosity is set to "+str(verbosity))

    # if a path to prism is given, we verify the argument
    if args.prism is not None :
         prism_path = args.prism

    try :
        result = subprocess.run(prism_path+"/bin/prism", capture_output=True, check=True)    
    except FileNotFoundError:
        # Prism was not found 
        print("Prism was not found...")
        print("Pass a correct path for prism, or follow the instructions in README.md")
        sys.exit(1)

    try :
        if not os.path.exists("temp"):
            os.mkdir("temp")
    except :
        print("Error creating the folder temp.")
        sys.exit(1)

    start_time = time.perf_counter() # to compute time 
    problem = file.read()
    ast = model_parser.parse(problem)
    
    # create a model with the prism MDP and the perceptions
    spec = {}
    spec['plts'] = str(ast.prismmodel)

    # we add the alphabet
    alphabet = set()
    for symbol in input_alphabet :
        alphabet.add(symbol)

    #spec['alphabet'] = alphabet

    # we add the perceptions to the model
    spec['perceptions'] = []
    for regexp in ast.perception.regexps :
        re_visitor = translator.TranslateToNFA(alphabet)
        regexp.accept(re_visitor)
        nfa = re_visitor.translate[str(regexp)]
        nfa.remove_epsilon()

        # if the automaton is not deterministic, we translate it to a determinist automaton
        if not nfa.is_dfa() :
            nfa.to_dfa() 
        
        # we translate the automaton to a live one
        nfa.to_live()
       
        spec['perceptions'].append((nfa,regexp))
    
    #for perception in spec['perceptions'] :
        # we create the file for the current preception
        #with open(spec_file_name, 'w') as f :
        #    f.write(spec['plts']+perception.toPrism())
    modelchecker = mc.ModelCheck(spec, prism_path, spec_file_name, verbosity)
    ast.property.accept(modelchecker)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Property checked: "+str(ast.property))
    if (modelchecker.to_states[str(ast.property)] == "true") | (modelchecker.to_states[str(ast.property)] == "false") :
        print("The property is " + modelchecker.to_states[str(ast.property)])
        if (modelchecker.to_states[str(ast.property)] == "true") and (isinstance(ast.property, AST.Kh)) :
            print("the witness is :" + modelchecker.witness)
    else :
        print("The property holds in states:" + str(modelchecker.get_states(str(ast.property))))
    print("Time: "+str(elapsed_time))

# the main entry 
if __name__ == "__main__" :
    main()