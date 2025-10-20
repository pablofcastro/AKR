# AKR: A Model Checker for an Adaptative Knowing-How Probabilistic Logic with Regular Expression Perceptions

This tool implements the algorithm of model checking described in: 

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

The logic is described in the paper but it mainly implement an algorithm to check formulas of the type:  

Kh(A,B) >= Q  

Intuitively, it says that an agent knows how to satisfy B from A, given a collection 
of perceptions.

# Installing the tool

The tool can be either **manually** or **automatically** using the provided *install.sh* script (see below). 

---

## Requirements

Before installing, you meet the following requirements:

### Software Dependencies
- Python 3.8 or higher  
- [Lark parsing toolkit](https://github.com/lark-parser/lark)
- PRISM Model Checker (installed manually or via `install.sh`)

---

## Installing the tool using *install.sh*

The `install.sh` script provides an easy installation method for:

- **Linux (Ubuntu 20.04 or later)** — Intel or ARM processors

To install, run the command:
```
sudo ./install.sh
```
(root privileges are needed for installing lark). 

If you are using another operating system, please follow the Manual Installation instructions below.

## Manual Installation

If you already used the file *install.sh*, you can skip this section. 

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

# Examples

In the folder ```tests/```you can find two examples.

##  Fire emergency

This is the example described in 

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

the specification for the example can be found in folder ```fire-emergency/```

## Tango robot

In this example, a cleaning robot *Tango*  has to clean several rooms in a corridor. 

See tests/hotel/README.md for full details.


This folder includes:

* `tests/hotel/benchmark/`-- several instances for the modes milonga, canyengue, and salon

* `tests/hotel/generator/benchmark_generator.py` -- generates the instances

* `tests/hotel/generator/evaluate_benchmark.py` -- runs the tool on all instances and saves results to output.csv

* `tests/hotel/generator/generate_plots.py` -- generates .jpg plots from the results

### Regenrating all the instances

From the main folder execute:

```
cd tests/generator
python3  benchmark_generator.py
```

All generated files will appear under `tests/hotel/benchmark/`.

### Running the Tool on all Instances
From the main folder execute:

```
cd tests/generator
python3 evaluate_benchmark.py
```

his will produce an `output.csv` file with the verification results.

### GEnerating the plots 

To generate the plots again run the following command:
```
cd tests/generator
python3 generate_plots.py
```

This will create .jpg plot files corresponding to the data in output.csv.














 
