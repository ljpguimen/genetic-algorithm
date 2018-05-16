"""This file sets voltages on the mirror from a file, for a constant voltage, or tests
individual actuators

Functions:
send_file() -- sets voltages on the mirror from a file of actuator voltages
send_genes() -- sets constant voltages on the mirror which are determined within the function
test_actuators -- test the voltages for individual actuators
"""

import numpy as np  # general useful python library

import file_functions as file_f     # used to read from files
import mirror_functions as mirror_f     # used to write voltages to the mirror


def send_file():
    """ This sets voltages on the mirror from a file of actuator voltages
    """
    num_genes = 37  # there are 37 mirror voltages
    filename = input('Please input the filename: ')
    saved_voltages = file_f.read_adf(filename,num_genes)   # read the saved voltages from the given file
    dm_actuators = mirror_f.actuator_array()    # initialize the information about the mirror
    print('You are setting voltages for deformable mirror')
    print('Actuator voltages are: ', saved_voltages)   # show the operator what voltages they are sending to the mirror
    mirror_f.write_to_mirror(saved_voltages, dm_actuators) # send the voltages to the mirror


def send_genes():
    """This sets constant voltages on the mirror which are determined within the function
    """
    num_genes = 37  # there are 37 mirror voltages
    constant_voltage = 0
    test_voltages = np.zeros(37) + constant_voltage   # create array of 37 constant voltages
    print('This is the genes:\n',test_voltages)    # show the operator what the actuator voltages are
    print('You are setting voltages for deformable mirror')
    dm_actuators = mirror_f.actuator_array()    # initialize the information about the mirror
    mirror_f.write_to_mirror(test_voltages, dm_actuators)  # write the voltages to the mirror


def test_actuators():
	num_genes = 37  # there are 37 actuators
	test_voltages = np.zeros(37)    # initialize the array of test voltages to 0
	dm_actuators = mirror_f.actuator_array()    # initialize the information about the mirror
	print("You are testing individual actuator voltages.\n")
	while True:     # create a while loop until the test voltage is determined
		print("What would you like the singular test actuator's voltage to be?")
		print("\tNote: The voltages for all of the other actuators will be 0")
		voltage = float(input())    # get the voltage from the operator
		print('Is this input okay: ', voltage, ' (Enter y or n)')
		good = input()  # get input from the user
		if good == 'y': # if the input was good
			break

	while True:
		test_voltages = np.zeros(37)    # reinitialze the test voltage array to be 0s
		while True: # create a while loop until the actuator to be tested is determined
			print("Which actuator would you like to test?\nEnter a integer from 0 to 36.")
			actuator_index = int(input())
			good = (actuator_index >= 0) and (actuator_index <= 36)     # make sure the actuator is within the correct range
			if good == True: # if the input was good
				print("Testing actuator ", actuator_index, "\n")
				break
			print("You didn't enter a number between 0 and 36")
		test_voltages[actuator_index] = voltage # set the test actuators voltage to the specified voltage
		print("Voltages are: ", test_voltages)
		mirror_f.write_to_mirror(test_voltages, dm_actuators)   # write the set of voltages to the mirror
		print("Finished testing? (Enter 'y' or 'n')")
		done = input()  # determine if the user is done
		if (done == 'y'):
			print("\nSending all 0's to the mirror")
			test_voltages = np.zeros(37)    # set the actuator voltages back to 0    
			print("Voltages are: ", test_voltages)
			mirror_f.write_to_mirror(test_voltages, dm_actuators)   # write the set of voltages to the mirror
			break





if __name__ == "__main__":
	# To send a constant voltage to the mirror, uncomment the line directly below and comment the other lines
	# send_genes()

	# To send a file, comment the line above and uncomment the next two lines
	send_file()

	# To test individual actuators run this function
	#test_actuators()