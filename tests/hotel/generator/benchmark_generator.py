# A simple script to generate the benchmark
import subprocess
import random

tangoNumber = 10 # number of examples
zambaNumber = 10 # number of examples
periconNumber = 10 # number of examples 

if __name__ == "__main__" :
    insNumber = {}
    insNumber["tango"] = [i*2 for i in range(tangoNumber) if i >= 4]
    insNumber["zamba"] = [i*2 for i in range(zambaNumber) if i >= 4]
    insNumber["pericon"] = [i*2 for i in range(periconNumber) if i >= 4]    
    # we generate the examples for tango

    for mode in ["tango", "pericon", "zamba"] :
        for prob in [0.25,0.50, 0.75] : # for these probs
            for i in insNumber[mode] :
                print(f"Generating {mode} files.")
                doorProbs = [str(random.random()) for _ in range(i)] 
                parameters = ["python", "main.py", str(prob)] + doorProbs + [mode] + [f"../benchmark/{mode}"]
                try :
                    result = subprocess.run(parameters, capture_output=True, text=True, check=True)
                except Exception as e:
                    print(f"Error Generating File: {e}")
    


