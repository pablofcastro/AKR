# AKR: A Model Checker for an Adaptative Knowing-How Probabilistic Logic with Regular Expression Perceptions

This is the artifact corresponding to the paper:

*AKR: A Model Checker for an Adaptative Probabilistic Knowing-How Logic*

submitted to TACAS 2026.

This tool implements the algorithm of model checking as described in: 

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

That is, the tool allows on to model check formulas of type:

Kh(A,B) >= Q  

Intuitively, it says that an agent knows how to satisfy B from A, given a collection 
of perceptions.

# Installing the tool in TACAS Virtual Machine

The tool can be installed in the TACAS Virtual Machine (running in  an Intel/AMD 64 bit or an ARM 64 bit processor) all the dependecies are incluided in the given .zip file:

- [Lark parsing toolkit](https://github.com/lark-parser/lark)
- PRISM Model Checker (installed manually or via `install.sh`)

The tool is entirely written in Python, the TACAS virtual Machine already has a Python interpreter installed.

To install the tool in the TACAS virtual Machine proceed as follows

## 1. Download the .zip file from Zenodo

## 2. Unzip de file

This can be done using the command `zip`:

```
unzip akr.zip
```

this will create the folder `akr/` where the sources and executables for the tool are located.

## 3. Run the *install.sh*

To install, run the command for the main directory of the tool:
```
sudo ./install.sh
```
(root privileges are needed for installing lark). 

** If you are using another operating system, please follow the Manual Installation instructions at the end of this document.**

# Running the tool

After installation, you can execute the tool from the main tool folder as follows:

```
cd src/
python3 akr.py -i <mymodel>
``` 

where ```<mymodel>``` is a specification file. 

For example, to test the tool execute (from the src folder):

```
cd src/
python akr.py -i ../tests/fire-emergency/fire_emerg_1.kr 
```

This model checks the specification `fire_emerg_1.kr`.

## Running the Benchmark

The files of the benchmark presented in the paper are located in the folder `tests/hotel/benchmark`.

To run the tool over the benchmark and replicate the results you have to execute the script `evaluate_benchmark.py` located in folder 
`tests/hotel/generator`. More precisely, from the main tool folder you have to execute the following commands:

```
cd tests/hotel/generator
python3 evaluate_benchmark.py
```

This will model check all the benchmark files and save the results in a file `output.csv`


## Generating the plots

To generate the plots again run the following command:
```
cd tests/hotel/generator
python3 generate_plots.py
```

This will create .jpg plot files corresponding to the data in output.csv.

## Generating all the benchmark again

If you want to generate again the benchmark, from the main folder execute:

```
cd tests/hotel/generator
python3  benchmark_generator.py
```

This generates new files, the script uses a random number generator for creating actions probabilities, that is, the files generated could be different from the one provided in the distribution.

All generated files will appear in the folder: `tests/hotel/benchmark/`.

##  Fire emergency Example

This is another example described in the paper:

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

the specification for this example can be found in folder ```fire-emergency/```.

# Manual Installation

** Follow the instructions in this section only if you want to install the tool NOT USING the script install.sh, otherwise you can skip this section. **

Assuming you are in the main folder of the distribution, follow these steps.

For the manual installation, assuming that you are located in the main folder of the distribution, follows the next steps.

### 1. install Prism

```
mkdir prism
cd prism
wget  https://github.com/prismmodelchecker/prism/archive/refs/heads/master.zip
zip master.zip
cd prism-master/prism
make
```
After compilation, PRISM should be located in prism-master/prism.
Move it one level up and run its installer:
```
mv prism-master/prism prism
cd prism
./install.sh
```
You can test if prism is installed executing: 
```
cd prism/bin
./prism
```

### 2. Install Lark

Install the Lark parser using `pip3`:

```
pip3 install lark
```

# Running the tool

## Running the tool 

After installation, you can run the tool from the main tool folder as follows:

```
cd src/
python3 akr.py -i <mymodel>
``` 

where ```<mymodel>``` is a specification file. To test the tool execute:

```
python akr.py -i ../tests/fire-emergency/fire_emerg_1.kr 
```

from the src folder.


## Running the tool using an installed version of PRISM

You can also run the tool using an already installed version of PRISM by specifying its path:

```
python akr.py -i <mymodel> -pp <prism-path>
```

where:
* <prism-path> -- path to your PRISM installation,
* <mymodel> -- specification file.


# The specification file

The input of the model checker consists of a specification, it is made of three parts:

* A PRISM model describing a MDP,
* A list of perceptions, described as regular expressions,
* A AKR property to be checked.

The following is a simple example of specification:

```
plts: 
    module mymodel:
        v : bool; 
        [a] v = false -> 0.5:(v'=true) + 0.5:(v'=false); 
        [b] v = true -> 0.1:(v'=true) + 0.9:(v'=false); 	
    endmodule
endplts

perception : a*;(a+b)
endperception

property : Kh(!v,v) >= 0.5
endproperty 
```

By default the tool infers the alphabet from the regular expressions. For instance, in the example above the alphabet deducted from the regular expressions is {a,b}. You can override this manually:

```
python src/akr.py -i mymodel.kr -a a,b,c
```

It verifies the specification in file mymodel.kr assuming alphabet {a,b,c}. Note that the used alphabet may have an impact in the verification.

















 
