import people
import people_functions as people_f
import msvcrt
import mirror_functions as mirror_f
import file_functions as file_f
import numpy as np
import initialization_functions as initialization_f

# // comment the rest of the code
# // add in a graph of the mirror
# // time the algorithm
# // add graph of parents

def genetic_algorithm():
    print('You are running the genetic algorithm')

    #This function sets all of the values of the number of parents, children, and mutation amount
    num_genes, num_init_parents, num_init_children, init_voltage, filename, num_parents, num_children, mutation_percentage = initialization_f.initialize()
    """Note: To change these for each iteration, go into inialization_functions.py in the initialize function"""

    print('Here are the options you have while the program is running:')
    print('\tPress the enter key if you would like to end the program')
    print('\tPress "m" if you would like to change the mutation percentage')
    print('\tPress "c" if you would like to change the number of children')
    print('\tPrees "p" if you would like to change the number of parents')
    print('Press the enter key to start the program')
    while True: # run an infinite loop until a key is pressed
        if msvcrt.kbhit():  # if the keyboard was hit
            keyboard_input = msvcrt.getwche()   # determine what was pressed on the keyboard
            if keyboard_input == '\r' or keyboard_input == '\n':    # if the key pressed was the enter key
                break   # break out of the infinite loop

    dm_actuators = mirror_f.acuator_array() # initialize the class to determine if actuator voltages break the mirror or not
    parents = people.parent_group(num_init_parents, num_genes, init_voltage, filename)    # create parents from above constraints
    children = people.child_group(num_init_children, parents, dm_actuators)       # create children from the given parents

    children.mutate(mutation_percentage, dm_actuators)    # mutate the children
    figure_of_merit_matrix = people_f.test_people(children, parents, num_init_parents, num_init_children, dm_actuators)     # determine the figure of merit for each parent and child
    best_parent_indices, best_child_indices, best_person = people_f.sort_people(figure_of_merit_matrix, parents, children, num_parents, num_init_parents)      # find the best performing parents and children
    print('best_person\n', best_person) # show the best person's genes and figure of merit

    while True:     # run an infinite loop until user says to stop
        if msvcrt.kbhit():  # if the keyboard was hit
            keyboard_input = msvcrt.getwche()   # determine what key was pressed
            if keyboard_input == '\r':  # if the enter key was pressed
                break   # get out of the loop
            if keyboard_input == 'm':   # if the m key was pressed
                print('\nThis is the current mutation percentage: ', mutation_percentage)
                mutation_percentage = initialization_f.change_value('float', 0, 100)
                break
            if keyboard_input == 'c':
                print('\nThis is the current number of children: ', num_children)
                mutation_percentage = initialization_f.change_value('int', num_parents-1)
                break
            if keyboard_input == 'p':
                print('\nThis is the current number of parents: ', num_parents)
                mutation_percentage = initialization_f.change_value('float', 0, num_children+1)
                break

        parents = people.parent_group(num_parents,num_genes, None, None, best_child_indices, children, best_parent_indices, parents)   # create parents from the best performing children
        children = people.child_group(num_children, parents, dm_actuators)       # create children from the just created parents

        children.mutate(mutation_percentage, dm_actuators)    # mutate the children
        figure_of_merit_matrix = people_f.test_people(children, parents, num_parents, num_children, dm_actuators)      # determine the figure of merit of each parent anc child
        best_parent_indices, best_child_indices, new_best_person = people_f.sort_people(figure_of_merit_matrix, parents, children, num_parents)        # find the best performing parents and children
        if new_best_person[1] > best_person[1]:     # determine if the best person's figure of merit in this run is better than the current best person's figure of merit
            best_person = new_best_person   # if the new best person is better, they are the overall best person ever
        print('best_person\n', best_person) # print out the best person ever made


    print('What would you like to do with the best person?')    # once the loop has finished, the user decides what to do with the genes made
    while True:     # create an infinite loop
        print('\tFor writing the genes to a file, input "write"')
        print('\tFor saving the nonexistent graph, input "graph"')  # // this isn't implemented yet
        print('\tFor doing nothing, input "none"')
        saving_option = input() # get user input for what they want to do
        if saving_option == 'write':    # if they want to write the genes to a file
            # // choose where to save this or see what files are already in this directory
            print("Enter the file name you want to be saved (for test.adf, input test):\nNote: this will overwrite a file with the same name")
            filename = input()  # get user input from for what filename they want
            # //check whether they inputted something correct and that they like it
            file_f.write_to_adf(best_person[0],filename)    # write the genes to the input file
            print('Would you like to do anything else? (y or n)')
            doing_more = input()    # see if the user wants to do more with the given data
            if doing_more == 'n':   # if they don't want to do anything else // also make sure that they enter either y or n
                break   # break out of the while loop
        elif saving_option == 'graph':  # if the user wants to save the graph
            print('Sorry, I dont have a graph function developed yet')
            print('Would you like to do anything else? (y or n)')
            doing_more = input()    # see if the user wants to do more with the given data
            if doing_more == 'n':   # if they don't want to do anything else // also make sure that they enter either y or n
                break   # break out of the while loop
        elif saving_option == 'none':   # if the user doesn't want to do anything with the data
            break   # break out of the while loop
        else:   # if they didn't enter one of the options
            print("You didn't enter a correct command")

# If this function is being run explicitly, I want the genetic algorithm funciton to be run.
# Otherwise, do not run the main function and so it only has the import functionality
if __name__ == "__main__":
    genetic_algorithm()
