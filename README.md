# AKR: A Model Checker for an Adaptative Knowing-How Probabilistic Logic with Regular Expression Perceptions

This tool implements the algorithm of model checking described in: 

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

The logic is described in the paper but it mainly implement an algoirthm to check formulas of the type:  

Kh(A,B) >= Q  

Intuitively, it says that an agent knows how to satisfy B from A, given a collection 
of perceptions.

# Installing the tool

The tool can be manually installed or using the provided *install.sh* script (see below). 

### Software Dependencies
- Python 3 or higher  
- [lark parsing toolkit](https://github.com/lark-parser/lark)

## Installing the tool using *install.sh*

The script *install.sh* provides a fast way to install the tool for the following operating systems:

- Linux (Ubuntu 20.04 or later) (on Intel based or ARM processor).

For running the script execute:
```
sudo ./install.sh
```
(root privileges are needed for installing lark). 

for other systems you have to proceed following the instructions in the next section. 

## Manual Installation

For the manual installation assuming that you are located in the main folder of the distribution, execute the following commands:

### install Prism

```
mkdir prism
cd prism
wget  https://github.com/prismmodelchecker/prism/archive/refs/heads/master.zip
zip master.zip
cd prism-master/prism
make
```
after this prism should be already installed in ```prism-master/prism```. Now, move the ```prism``` code to one leve down:
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

You also have to install lark, you can use pip3:

```
pip3 install lark
```

# Running the tool

## Running the tool 

After installing the tool as explained above, for running it  you can execute:

```
cd src/
python akr.py -i <mymodel>
``` 

where <mymodel> is a specification file. To test the tool you can execute:

```
python akr.py -i ../tests/fire-emergency/fire_emerg_1.kr 
```

from the src folder.


## Running the tool using an installed version of PRISM

You can also run the tool  using an already installed version of prism just execute:

```
python akr.py -i <mymodel> -pp <prism-path>
```

where <prism-path> is the path to the prism installation. <mymodel> is a file containing 
the specification to be analysed (see below).


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

By default the tool deducts the alphabet from the regular expressions. For instance, in the example above the alphabet deducted from the regular expressions is {a,b}. Alphabets can be passed as argument to the tool as follows:

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

In this example, a cleaning robot *Tango*  has to clean several rooms in a corridor. There is a README.md in 
the folder ```tests/hotel``` explaining the example in detail. In this folder you can find several instances of the example together with the scripts used for generating them

* ```tests/hotel/benchmark```it contains several of instances for the modes *milonga*, *canyengue*, and *salon*, each of them is expressed using a different regular expression.
* ``` tests/hotel/generator/benchmark_generator.py``` it generates all the instances in folder ```test/hotel/benchmark```,
* ``` tests/hotel/generator/evaluate_benchmark.py``` it evaluates the benchmark, running hte tool and saving the result in ```output.csv```,
* ``` tests/hotel/generator/generate_plots.py ``` it generates the plots for the result obtained in ``` output.csv``` and save them as .jpg.

For generating all the instances again, you have to execute (from the main tool folder):

```
cd tests/generator
python3  benchmark_generator.py
```

after this, all the files are in ```tests/hotel/benchmark``` stored in subfolders. 

For running the tool over these instances you can execute (from the main tool folder)

```
cd tests/generator
python3 evaluate_benchmark.py
```

After this, the script will generate a file ```output.csv``` with the obtained results.

If you want to generate plots with this data you can follow the following commands:
```
cd tests/generator
python3 generate_plots.py
```

you will see .jpg files with the plots corresponding to the data in output.csv.














 
