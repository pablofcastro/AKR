# AKR: A Model Checker for an Adaptative Knowing-How Probabilistic Logic

This tool implements the algorithm of model checking described in: 

*How Lucky Are You to Know Your Way? A Probabilistic Approach to Knowing How Logics
Pablo Castro, Pedro R. D'Argenio and Raul Fervari. KR 2025.*

The logic is described in the paper but it mainly implement an algoirthm to check formulas of the type:  

Kr(A,B) >= Q  

Intuitively, it says that an agent knows how to satisfy B from A, given a collection 
of perceptions.

# Running the tool

The tool uses the PRISM model checker for the verification. A PRISM distribution 
is included with AKR. As explained below, you can also use an already installed PRISM distribution.

## Running the tool using an installed version of PRISM

To run the tool using a installed version of prism just execute:

> python akr.py -i mymodel.kr -pp <prism-path>

where <prism-path> is the path to the prism installation. mymodel.kr is a file containing 
the specification to be analysed (see below).

## Running the tool without having PRISM installed

If the PRISM tool is not already installed, you can install PRISM using the provided distribution,
for that, execute the following commands from the main folder.

> cd prism/prism
> make

you can test if prism is installed by executing:

> ./bin/prism 

Now, for running the tool you can execute:

> python src/akr.py -i mymodel.kr 

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

> python src/akr.py -i mymodel.kr -a a,b,c

It verifies the specification in file mymodel.kr assuming alphabet {a,b,c}. Note that the used alphabet may have an impact in the verification.







 
