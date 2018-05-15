

import numpy as np

import file_functions as file_f
import mirror_functions as mirror_f


def send_file():
	num_genes = 37
	filename = input('Please input the filename: ')
	saved_genes = file_f.read_adf(filename,num_genes)
	dm_actuators = mirror_f.actuator_array()
	print('You are setting voltages for deformable mirror')
	print('Actuator voltages are: ', saved_genes)
	mirror_f.write_to_mirror(saved_genes, dm_actuators)


def send_genes():
	num_genes = 37
	test_genes = np.zeros(37) + 0
	# test_genes[0]=70
	# test_genes = (np.arange(37)+1)*0.5
	print('This is the genes:\n',test_genes)
	print('You are setting voltages for deformable mirror')
	dm_actuators = mirror_f.actuator_array()
	mirror_f.write_to_mirror(test_genes, dm_actuators)


def test_actuators():
	num_genes = 37
	test_genes = np.zeros(37) + 0
	dm_actuators = mirror_f.actuator_array()
	print("You are testing individual actuator voltages.\n")
	while True:
		print("What would you like the singular test actuator's voltage to be?")
		print("\tNote: The voltages for all of the other actuators will be 0")
		voltage = float(input())
		print('Is this input okay: ', voltage, ' (Enter y or n)')
		good = input()  # get input from the user
		if good == 'y': # if the input was good
			break

	while True:
		test_genes = np.zeros(37) + 0
		while True:
			print("Which actuator would you like to test?\nEnter a integer from 0 to 36.")
			actuator_index = int(input())
			good = (actuator_index >= 0) and (actuator_index <= 36)
			if good == True: # if the input was good
				print("Testing actuator ", actuator_index, "\n")
				break
			print("You didn't enter a number between 0 and 36")
		test_genes[actuator_index] = voltage
		print("Voltages are: ", test_genes)
		mirror_f.write_to_mirror(test_genes, dm_actuators)
		print("Finished testing? (Enter 'y' or 'n')")
		done = input()
		if (done == 'y'):
			print("\nSending all 0's to the mirror")
			test_genes = np.zeros(37) + 0
			print("Voltages are: ", test_genes)
			mirror_f.write_to_mirror(test_genes, dm_actuators)
			break





if __name__ == "__main__":
	# To send a constant voltage to the mirror, uncomment the line directly below and comment the other lines
	# send_genes()

	# To send a file, comment the line above and uncomment the next two lines
	send_file()

	# To test individual actuators run this function
	#test_actuators()