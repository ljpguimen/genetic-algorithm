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
num_init_children = 10      # number of starting children

num_parents = 10            # number of parents in loop iterations
num_children = 100          # number of children in loop iterations
init_voltage = 30           # initial voltage on mirror actuators
mutation_percentage = 20    # if you want 20% mutation, enter 20

'''have an initialize function here which would be able to 
create the dm_actuator_neighbor
array and connect to any needed devices'''

parents = parent_group(num_init_parents, num_genes, init_voltage)    # create parents from above constraints
children = child_group(num_init_children, parents)       # create children from the given parents

children.mutate(mutation_percentage)    # mutate the children
figure_of_merit_matrix = test_people(children, parents, num_init_parents, num_init_children)     # determine the figure of merit for each parent and child
print(figure_of_merit_matrix)
best_parent_indices, best_child_indices = sort_people(figure_of_merit_matrix, num_parents, num_init_parents)      # find the best performing parents and children
print('done?')
'''
while True:
    parents = parent_group(num_parents,num_genes, None, best_child_indices, children, best_parent_indices, parents)   # create parents from the best performing children
    children = child_group(num_children, parents)       # create children from the just created parents
    
    children.mutate(mutation_percentage)    # mutate the children
    figure_of_merit_matrix = test_people(children, parents, num_parents, num_children)      # determine the figure of merit of each parent anc child
    print(figure_of_merit_matrix)
    best_parent_indices, best_child_indices = sort_people(figure_of_merit_matrix, num_parents)        # find the best performing parents and children
    # somehow create a way to stop the program based on user input
    # also make the user able to change things like mutation percentage or any other relevant variable
    # save the best child'''
"""
def main():


 # If this function is being run explicitly, I want the main funciton to be run.
 # Otherwise, do not run the main function and make another .py file to be able to import these funcitons
if __name__ == "__main__":
    main()
"""