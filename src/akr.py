"""
    Main script the AKR tool
"""
import argparse, os
import sys
sys.path.insert(1, './Parser')
import AST
import parser as model_parser

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
    parser = argparse.ArgumentParser()
    file = ""
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-i", "--input", dest="file", required=True, type=validate_file,
                        help="the file with the model", metavar="FILE")   
    args = parser.parse_args()
    try :
        file = open(args.file, "r")
    except OSError:
        print(f"Error: Couldn't open input file")
        sys.exit()

    problem = file.read()
    ast = model_parser.parse(problem)
    print(ast)


# the main entry 
if __name__ == "__main__" :
    main()