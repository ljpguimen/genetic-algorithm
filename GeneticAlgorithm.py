"""
Genetic algorithm code

Note: the error is true by default

Start program and you have two options:
1) Load a file
2) run algorithm

Now the algorithm starts
start timer to progressively see how much time has elapsed
read diode  # what is the functionality of read diode at the beginning?
            # It is probably just to make sure that the diode can be read

somehow Add the children and effectiveness to the graph


"""
import people
import people_functions as people_f
import msvcrt

# // do the if def main(): thing for the rest of the files

#def genetic_algorithm():
# also make the user able to change things like mutation percentage or any other relevant variable
"""Original function keeps track of time it ran"""
num_genes = 10              # number of genes of each person (or mirror actuators)
num_init_parents = 1        # number of parents to start with
num_init_children = 10      # number of starting 
filename = None             # name of file to read from

num_parents = 10            # number of parents in loop iterations
num_children = 100          # number of children in loop iterations
init_voltage = 30           # initial voltage on mirror actuators
mutation_percentage = 20    # if you want 20% mutation, enter 20

'''have an initialize function here which would be able to 
create the dm_actuator_neighbor
array and connect to any needed devices'''

print('Press the enter key if you would like to end the program')

parents = people.parent_group(num_init_parents, num_genes, init_voltage, filename)    # create parents from above constraints
children = people.child_group(num_init_children, parents)       # create children from the given parents

children.mutate(mutation_percentage)    # mutate the children
figure_of_merit_matrix = people_f.test_people(children, parents, num_init_parents, num_init_children)     # determine the figure of merit for each parent and child

best_parent_indices, best_child_indices, best_person = people_f.sort_people(figure_of_merit_matrix, parents, children, num_parents, num_init_parents)      # find the best performing parents and children
print('best_person\n', best_person)

while True:
    if msvcrt.kbhit():
        if msvcrt.getwche() == '\r' or msvcrt.getwche() == '\n':
            break
    parents = people.parent_group(num_parents,num_genes, None, None, best_child_indices, children, best_parent_indices, parents)   # create parents from the best performing children
    children = people.child_group(num_children, parents)       # create children from the just created parents

    children.mutate(mutation_percentage)    # mutate the children
    figure_of_merit_matrix = people_f.test_people(children, parents, num_parents, num_children)      # determine the figure of merit of each parent anc child
    best_parent_indices, best_child_indices, new_best_person = people_f.sort_people(figure_of_merit_matrix, parents, children, num_parents)        # find the best performing parents and children
    if new_best_person[1] > best_person[1]:
        best_person = new_best_person
    print('best_person\n', best_person)
"""
def main():
 # If this function is being run explicitly, I want the genetic algorithm funciton to be run.
 # Otherwise, do not run the main function and so it only has the import functionality
    if __name__ == "__main__":
        genetic_algorithm()
        """
