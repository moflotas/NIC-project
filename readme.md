# Genetic Programming for Combinational Logic Circuits Optimization using Modi structure

## Brief Introduction

In this project we develop a Genetic Programming algorithm to optimize the design of Combinational Logic Circuits (CLCs) for executing straight-line boolean programs using a specified set of available logic gates. The algorithm uses Modi nodes to build multi-output CLCs with small number of gates used. Despite our algorithm was able to find perfectly accurate solutions, those solutions were not always optimal in terms of gates number. Further improvements or more comprehensive fine-tuning may be required to achieve better results, however this method already proved to be efficient.

## Implementation

### Modi Program Tree Structure

- Implements multiple outputs in GP using program tree structure proposed by Zhang
- Produces **multiple values**, each corresponding to a different class in multiclass classification problem
- Outputs vector is virtual, only realized at program evaluation time and updated by the program tree
- Uses special structural **END nodes** to finish the tree with a single root

### Genetic Operators

- Essential components of genetic algorithms, impacting convergence rate, diversity, and quality of solutions obtained
- Chose **uniform mutation** as the most simple and reliable approach for our problem
- Chose **leaf-biased one-point crossover** to maintain diversity in the population and change the core functions of the trees while keeping inputs less likely to be modified
- **Tournament selection** with $p=1$ and tournament size in range from 5 to 20 was the most efficient

### Implementation Details

- Used **DEAP** Python framework
- Contains necessary genetic operators and provides API for both multi-objective fitness function and multi-output Genetic Programming algorithms
- Provides useful tools for statistics

## Examples

Here are some examples of our program execution on different inputs function to optimize
| two 2-bit numbers adder | full adder (6 logic gates) |
| --------------------- | -------------------------- |
| ![two 2-bit numbers adder](/pictures/2_2bit_numbers.png) | ![full adder (6 logic gates)](/pictures/full_adder.png)|

## Setup

- Install `python3.9`
- Create and activate virtual environment  
  - For Linux distributive
  - `python3.9 -m venv venv`
  - `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Test different functions in `main.py` changing `find_circuit` first argument
