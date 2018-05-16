This is a genetic algorithm used for machine learning. It is a black-box optimization technique originally 
developed by O. Albert and was published in Optics Letters, Vol. 25, No. 15, August 1, 2000. It was then moved to 
python with some adjustments to get rid of any parts that were no longer used. 

HOW TO RUN
1) Open Anaconda Prompt by pressing the windows key and typing "Anaconda Prompt"
2) Navigate to the folder which contains GeneticAlgorithm.py (by using the "cd" and "dir" commands)
3) Type "python GeneticAlgorithm.py"


INITIALIZATION SETTINGS
Change the default running values in genetic_algorithm.ini


DATA ACQUISITION SETTINGS
To adjust data acquisition settings, navigate to the appropriate folder and adjust the properties.ini file
For example, navigate to "Andor/Andor properties.ini" and adjust those initialization settings.


HOW TO SET UP A NEW DATA ACQUISITION DEVICE
1) Create a folder with your new device 
2) Within that folder, create a properties.ini file formatted the same as the other .ini files.
3) Adjust the data_acquisition_functions.py file to include an initialize, acquire, and shut_down function for your device.
4) Include your device as an available option in the genetic_algorithm.ini file

Example: If you want to call your device "device1", create a folder named "device1". Within that folder, create
a file named "device1 properties.ini". Adjust data_acquisition_functions.py to have options for 
"elif (self.device == "device1"):" in its public functions (public functions do not have "__" in front of their name).
Then, go into genetic_algorithm.ini and let "device1" be an option.


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


