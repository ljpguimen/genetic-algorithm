This is a genetic algorithm used for machine learning. It is a black-box optimization technique originally developed by O. Albert and was published
 in Optics Letters, Vol. 25, No. 15, August 1, 2000. It was then moved to 
python with some adjustments to get rid of any parts that were no longer 
used. 



Note: if you want to optimize the lowest figure of merit instead of the highest, change 
Self.people.sort(key=operator.attrgetter('figure_of_merit'), reverse = True) around line 232 of people.py so it is reverse = False
self.people.sort(key=operator.attrgetter('figure_of_merit'), reverse = False)




There a number of important variables that should be readily accessible to 
anyone using the program. I have listed what they are and their locations.
They should all be at the top of the program.



WAITING_TIME - time between writing to the mirror and measuring the figure of merit. 
location: people.py

PCI_BOARDS - addresses of the pci cards given in NI-MAX. 

location: mirror_functions.py



MAX_DIFF - maximum difference between neighboring actuators
location: mirror_functions.py

MAX_VOLTAGE - maximum voltage an actuator can have

location: mirror_functions.py



ADF_FOLDER - directory to store mirror files (as ascii data files)

location: file_functions.py



FOM_GRAPH_FOLDER - directory to store figure of merit graph data (as csv files)

location: file_functions.py



MIRROR_GRAPH_FOLDER - directory for the graphs of the mirror

location: file_functions.py
NUMBER_OF_READS - number of voltage values to average over in the photodiode
location: figure_of_merit_functions.py




The default starting values are given in initialization_functions.py 
starting a little after line 100. This has the following variables:
num_genes = 37              # number of genes of each person (or mirror actuators)

num_init_parents = 1        # number of parents to start with

num_init_children = 10     # number of starting children
    

init_voltage = 30           # initial voltage on mirror actuators

filename = None             # name of file to read from


num_parents = 10            # number of parents in loop iterations

num_children = 100          # number of children in loop iterations

mutation_percentage = 2    # if you want 20% mutation, enter 20

