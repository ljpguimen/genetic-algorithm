This is a genetic algorithm used for machine learning. It is a black-box optimization technique originally developed by O. Albert and was published
 in Optics Letters, Vol. 25, No. 15, August 1, 2000. It was then moved to 
python with some adjustments to get rid of any parts that were no longer 
used. 

Change the default running values in genetic_algorithm.ini

How to run the genetic algorithm:

1) Open Anaconda Prompt by pressing the windows key and typing "Anaconda Prompt"
2) Navigate to the folder which contains GeneticAlgorithm.py (by using the "cd" and "dir" commands)
3) Type "python GeneticAlgorithm.py"



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


