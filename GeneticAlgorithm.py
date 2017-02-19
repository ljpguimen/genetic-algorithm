"""
Genetic algorithm code

python passes by object reference, so any transpose function will be costly

Note: the error is true by default

Start program and you have two options:
1) Load a file
2) run algorithm


How to load a file:
# still don't really know the history in/start from/history out variables
go to file path
read in file with .adf extension

There should be 39 values in the .adf file
37 actuator voltages
1 social efficiency gene
1 mutation information gene

Now the algorithm starts
start timer to progressively see how much time has elapsed
read diode  # what is the functionality of read diode at the beginning?
            # It is probably just to make sure that the diode can be read

Create children
Genetic mutation
Social test
choose parents for next generation
somehow Add the children and effectiveness to the graph

Then the repetitive part of the algorithm starts 
# This part also saves the best child ever
Create children
Genetic mutation
add parent for this generation
Social test
choose (best children) parents for next generation
somehow add to graph


"""
from people import *

"""Original function keeps track of time it ran"""
num_genes = 10              # number of genes of each person (or mirror actuators)
num_init_parents = 1        # number of parents to start with
init_voltage = 30           # initial voltage on mirror actuators
num_init_children = 10      # number of starting children
mutation_percentage = 20    # if you want 20% mutation, enter 20

new_parent = parent_group(num_init_parents, num_genes, init_voltage)
new_children = child_group(num_init_children, new_parent)

new_children.mutate(mutation_percentage)

test_people(new_children,new_parent)


"""
def main():


 # If this function is being run explicitly, I want the main funciton to be run.
 # Otherwise, do not run the main function and make another .py file to be able to import these funcitons
if __name__ == "__main__":
    main()
"""