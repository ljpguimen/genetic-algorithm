"""This file contains functions to initialize values and to change values which have been established"""
import msvcrt

# //comment the code

def change_value(datatype, lowerbound = None, upperbound = None):
    """For datatype enter 'float', 'int', or 'string'
The value must be within (lowerbound, upperbound)"""
    while True:
        print('What would you like to change it to?')
        if datatype == 'string':
            new_value = input()    # get the new mutation percentage from the user
            print('Is this input okay: ', new_value, ' (Enter y or n)')
            good = input()
            if good == 'y':
                break
        if datatype == 'int':
            new_value = int(input())
            if not(lowerbound is None) and not(upperbound is None):
                if (new_value <= lowerbound) or (new_value >= upperbound):
                    print('Error: You entered a value that is not within (', lowerbound, ', ', upperbound, ')')
                    break
            elif not(lowerbound is None):
                if (new_value <= lowerbound):
                    print('Error: You entered a value that is lower than or equal to ', lowerbound)
                    break            
            elif not(upperbound is None):
                if (new_value <= lowerbound) or (new_value >= upperbound):
                    print('Error: You entered a value that is higher than or equal to ',upperbound)
                    break
            print('Is this input okay: ', new_value, ' (Enter y or n)')
            good = input()
            if good == 'y':
                break
        if datatype == 'float':
            new_value = float(input())
            if not(lowerbound is None) and not(upperbound is None):
                if (new_value <= lowerbound) or (new_value >= upperbound):
                    print('Error: You entered a value that is not within (', lowerbound, ', ', upperbound, ')')
                    break
            elif not(lowerbound is None):
                if (new_value <= lowerbound):
                    print('Error: You entered a value that is lower than or equal to ', lowerbound)
                    break
            elif not(upperbound is None):
                if (new_value <= lowerbound) or (new_value >= upperbound):
                    print('Error: You entered a value that is higher than or equal to ',upperbound)
                    break
            print('Is this input okay: ', new_value, ' (Enter y or n)')
            good = input()
            if good == 'y':
                break
    return new_value

def change_others():
    """This function checks if the user wants to change anything else"""
    print('Would you like to change anything other variables?')
    print('Enter y or n')
    while True:
        user = input()
        if user == 'y':
            return True
        elif user == 'n':
            return False
        else:
            print('You entered an incorrect command')


def initialize():
    """This function defines all of the user specified values"""
    num_genes = 37              # number of genes of each person (or mirror actuators)
    num_init_parents = 1        # number of parents to start with
    num_init_children = 10     # number of starting children
    
    """Note: You can either have an initial voltage or a filename to read from, not both"""
    init_voltage = 30           # initial voltage on mirror actuators
    filename = None             # name of file to read from
    '''Note: Enter the filename as a string without the .adf extension at  the end.
             Also, it can only read the file if it is in the same folder as the program'''

    num_parents = 10            # number of parents in loop iterations
    num_children = 100          # number of children in loop iterations
    mutation_percentage = 5    # if you want 20% mutation, enter 20

    if not (init_voltage is None) and not (filename is None):
        print('Error: You have both an initial voltage and a filename to read from')

    print("These are the current variables' values: ")
    print('\tNumber of initial parents: ', num_init_parents)
    print('\tNumber of initial children: ', num_init_children, '\n')
    print('\tNumber of parents: ', num_parents)
    print('\tNumber of children: ', num_children, '\n')
    print('\tFilename to read from: ', filename)
    print('\tInitial voltage of starting parent: ', init_voltage, '\n')
    print('Would you like to change any of these values?\nEnter "y" or "n"')
    keyboard_input = input()        
    if keyboard_input == 'y':    # if the key pressed was the enter key
        while True:
            print('To change the number of initial parents, enter "initial parents"')
            print('To change the number of initial children, enter "initial children"')
            print('To change the number of parents, enter "parents"')
            print('To change the number of children, enter "children"')
            print('To change the filenmae or initial voltage, enter "init setting"')
            print('To change nothing, enter "none"')
            key_input = input()
            if key_input == 'initial parents':
                print('You are changing the number of initial parents')
                num_init_parents = change_value('int', 0, num_init_children+1)
                if not change_others():
                    break
            elif key_input == 'initial children':
                print('You are changing the number of initial children')
                num_init_children = change_value('int', num_init_parents-1)
                if not change_others():
                    break
            elif key_input == 'parents':
                print('You are changing the number of parents')
                num_parents = change_value('int', 0, num_children+1)
                if not change_others():
                    break
            elif key_input == 'children':
                print('You are changing the number of children')
                num_children = change_value('int', num_parents-1)
                if not change_others():
                    break
            elif key_input == 'init setting':
                print('You are changing the initialization setting')
                print('Would you like to change the filename or the initial voltage?')
                print('Enter "filename", "initial voltage", or "none"')
                keyboard_press = input()
                if keyboard_press == 'filename':
                    print('You are changing the filename')
                    print('When entering filenames, enter the name without the .adf extension')
                    print('Note: The file must be in the same directory as this program for the program to be able to read it')
                    filename = change_value('string')
                    init_voltage = None
                    if not change_others():
                        break
                if keyboard_press == 'initial voltage':
                    print('You are changing the initial voltage')
                    init_voltage = change_value('float', 0, 60)
                    filename = None
                    if not change_others():
                        break
                if keyboard_press == 'none':
                    if not change_others():
                        break
                else:
                    print('You did not enter a correct input')
            elif key_input == 'none':
                print('You are not changing anything')
                break
            else:
                print('You did not enter a valid command')
    if keyboard_input == 'n':
        print('\n')
    return num_genes, num_init_parents, num_init_children, init_voltage, filename, num_parents, num_children, mutation_percentage

if __name__ == "__main__":
    print('You meant to run GeneticAlgorithm.py')
