"""
    Main script the AKR tool
"""
import argparse, os
import sys
sys.path.insert(1, './Parser')
sys.path.insert(1, './NFA')
import AST
import parser as model_parser
import translator_regexp_nfa as translator
import MC as mc
import time

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
    prism_path = "../prism/prism"
    parser = argparse.ArgumentParser()
    spec_file_name = "temp/model.prism" # this is the file where the model is stored, 
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-i", "--input", dest="file", required=True, type=validate_file,
                        help="the file with the model", metavar="FILE")   
    args = parser.parse_args()
    try :
        file = open(args.file, "r")
    except OSError:
        print(f"Error: Couldn't open input file")
        sys.exit()

    start_time = time.perf_counter() # to compute time 
    problem = file.read()
    ast = model_parser.parse(problem)
    
    # create a model with the prism MDP and the perceptions
    spec = {}
    spec['plts'] = str(ast.prismmodel)

    # we add the perceptions to the model
    spec['perceptions'] = []
    for regexp in ast.perception.regexps :
        re_visitor = translator.TranslateToNFA()
        regexp.accept(re_visitor)
        nfa = re_visitor.translate[str(regexp)]
        spec['perceptions'].append(nfa)
    
    #for perception in spec['perceptions'] :
        # we create the file for the current preception
        #with open(spec_file_name, 'w') as f :
        #    f.write(spec['plts']+perception.toPrism())
    modelchecker = mc.ModelCheck(spec, prism_path, spec_file_name)
    ast.property.accept(modelchecker)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Property checked: "+str(ast.property))
    if (modelchecker.to_states[str(ast.property)] == "true") | (modelchecker.to_states[str(ast.property)] == "false") :
        print("The property is " + modelchecker.to_states[str(ast.property)])
    else :
        print("The property holds in states:" + str(modelchecker.get_states(str(ast.property))))
    print("Time: "+str(elapsed_time))

# the main entry 
if __name__ == "__main__" :
    main()