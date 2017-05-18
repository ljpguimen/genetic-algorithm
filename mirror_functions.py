"""These functions check whether the genes break the mirror and write genes to the mirror"""

#import pyvisa   # Use this when using the pyvisa code in send_to_board
#from PyDAQmx import *   # Use this when using the pyDAQmx code in send_to_board
from ctypes import *
import win32com.client  # Use this when using the LabVIEW VI in send_to_board # Python ActiveX Client
import numpy as np

# // comment
# // comment under each function
PCI_BOARDS = [['PXI4::5::INSTR'], ['PXI4::4::INSTR']]
# the top row values are the addresses of actuators 0-18 and the bottom values are the addresses of the actuators 19-36
ACTUATOR_ADDRESSES = [[0x34, 0x54, 0x28, 0x38, 0x08, 0x04, 0x24, 0x50, 0x58, 0x2C, 0x30, 0x1C, 0x10, 0x14, 0x0C, 0x00, 0x3C, 0x20, 0x5C],
                      [0x24, 0x5C, 0x58, 0x54, 0x20, 0x10, 0x08, 0x1C, 0x14, 0x0C, 0x04, 0x00, 0x3C, 0x38, 0x34, 0x30, 0x2C, 0x28]]
FIRST_BOARD = 0
SECOND_BOARD = 1

class acuator_array(object):
    """This makes sure the voltage difference between neighboring actuators isn't too high"""
    def __init__(self):
        # create an array that represents the deformable mirror indices
        dm_array = [[-1,-1,28,27,26,-1,-1],
                    [-1,29,14,13,12,25,-1],
                    [30,15, 4, 3, 2,11,24],
                    [31,16, 5, 0, 1,10,23],
                    [32,17, 6, 7, 8, 9,22],
                    [-1,33,18,19,20,21,-1],
                    [-1,-1,34,35,36,-1,-1]]
        
        dm_actuator_neighbors = []      # initialize the empty list of neighboring actuators

        """The nested for loops go through the entire array and determine which actuators 
           are neighbors. It includes actuators which are diagonal to each other"""
        for i in range(len(dm_array)):  # go through each row
            for j in range(len(dm_array[i])):   # go through each column
                if abs(i-3) + abs(j-3) < 5:     # make sure the index at (i,j) is close enough to the center to represent a real actuator
                    start_actuator = dm_array[i][j]     # this will be the actuator examined in the for loop
                    if j !=len(dm_array[i])-1:      # if j is not in the last column
                        neighbor = dm_array[i][j+1]     # the actuator to the right is a neighbor
                        if neighbor != -1:      # make sure the actuator to the right is real
                            dm_actuator_neighbors.append([start_actuator,neighbor])     # append these neighbors to the list
                    if i!=len(dm_array)-1:  # if i is not in the last row
                        neighbor = dm_array[i+1][j]     # the actuator below is a neighbor
                        if neighbor != -1:      # make sure the actuator to the right is real
                            dm_actuator_neighbors.append([start_actuator,neighbor])     # append these neighbors to the list
                        if j != len(dm_array[i])-1:     # if j is not in the last column
                            neighbor = dm_array[i+1][j+1]   # the actuator on the bottom and to the right is a neighbor
                            if neighbor != -1:      # make sure the actuator to the right is real
                                dm_actuator_neighbors.append([start_actuator,neighbor]) # append these neighbors to the list
                        if j!=0:    # if j is at the beginning of the row
                            neighbor = dm_array[i+1][j-1]   # the actuator to the bottom left is a neighbor
                            if neighbor != -1:      # make sure the actuator to the right is real
                                dm_actuator_neighbors.append([start_actuator,neighbor]) # append these neighbors to the list
        self.dm_actuator_neighbors = dm_actuator_neighbors  # make the neighbors list an attribute
        """ This is brute force
        # array which contains all actuator neighbor pairs
        dm_neighbors = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[1,2],[1,3],[1,7],[1,8],[1,9],[1,10],
                        [1,11],[2,3],[2,12],[2,13],[2,10],[2,11],[2,25],[3,4],[3,12],[3,13],[3,5],[3,14],
                        [4,5],[4,13],[4,14],[4,15],[4,16],[4,29],[5,6],[5,7],[5,15],[5,16],[5,17],[6,7],[6,16],
                        [6,17],[6,32],[6,19],[6,33],[7,8],[7,32],[7,20],[7,19],[7,18],[8,9],[8,10],[8,19],
                        [8,20],[8,21],[9,10],[9,20],[9,21],[9,22],[9,23],[10,11],[10,22],[10,23],[10,24],[11,12],
                        [11,23],[11,24],[11,25],[12,13],[12,25],[12,26],[12,27],[13,14],[13,26],[13,27],[13,28],
                        [14,15],[14,27],[14,28],[14,29],[15,16],[15,29],[15,30],[15,31],[16,17],[16,30],[16,31],
                        [16,32],[17,18],[17,31],[17,32],[17,33],[18,19],[18,33],[18,34],[18,35],[19,20],[19,34],
                        [19,35],[19,36],[20,21],[20,35],[20,36],[21,22],[21,36],[22,23],[23,24],[24,25],[25,26],
                        [27,28],[28,29],[29,30],[30,31],[31,32],[32,33],[33,34],[34,35],[35,36]]
        """

    def fits_mirror(self,genes):
        """Determine if a child breaks the mirror"""
        genes = genes*2.625   # This is the DM constant used in the original code
        valid = True    # the child is good until proven bad
        for i in range(len(self.dm_actuator_neighbors)):      # Test every actuator value with its neighbors' values
            valid = valid and (abs(genes[self.dm_actuator_neighbors[i][0]]-genes[self.dm_actuator_neighbors[i][1]]) <= 30)  # test voltage difference between neighboring actuators is less than 30
        return valid
    

def array_conversion(genes):    # // write this function
    return genes

def send_to_board(voltages0, voltages1):
    
    #There are 3 different sets of code to write to the board: calling functions in a LabVIEW dll, calling the LabVIEW VIs themselves, and using pyVISA 
    # This utilizes the dll created from custom made VIs which communicate directly to each pci card
    """
    volt_to_board = cdll.LoadLibrary('volt_to_board.dll')
    error_in = 0
    error_out = 0
    c_address0 = (c_int * len(ACTUATOR_ADDRESSES[0]))(*ACTUATOR_ADDRESSES[0])
    c_address1 = (c_int * len(ACTUATOR_ADDRESSES[1]))(*ACTUATOR_ADDRESSES[1])
    c_voltage0 = (c_float * len(voltages0.tolist()))(*voltages0.tolist())
    c_voltage1 = (c_float * len(voltages1.tolist()))(*voltages1.tolist())
    error_out = volt_to_board.Volt_to_board_0(c_address0, c_voltage0, error_in, error_out)
    print(error_out)
    error_out = volt_to_board.Volt_to_board_1(c_address1, c_voltage1, error_in, error_out)
    print(error_out)
    return
    """

    # This is the code for running the LabView VI which communicates with the deformable mirror 
    
    LabVIEW = win32com.client.Dispatch("Labview.Application")
    pci0VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\Volt_to_board_0.vi')    # path the LabVIEW VI
    pci0VI._FlagAsMethod("Call")    # Flag "Call" as method
    pci0VI.setcontrolvalue('error in (no error)', 0)   # set first input
    pci0VI.setcontrolvalue('addresses', ACTUATOR_ADDRESSES[0])   # set first input
    pci0VI.setcontrolvalue('values to write', voltages0.tolist())   # set first input
    pci0VI.Call()   # Run the VI
    result = pci0VI.getcontrolvalue('error out')
    print(result)

    
    pci1VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\Volt_to_board_1.vi')    # path the LabVIEW VI
    pci1VI._FlagAsMethod("Call")    # Flag "Call" as method
    pci1VI.setcontrolvalue('error in (no error)', 0)   # set first input
    pci1VI.setcontrolvalue('addresses', ACTUATOR_ADDRESSES[1])   # set first input
    pci1VI.setcontrolvalue('values to write', voltages1.tolist())   # set first input
    pci1VI.Call()   # Run the VI
    result = pci1VI.getcontrolvalue('error out')
    print(result)
    return
    

    # This is the code for testing whether python can run a test labview VI
    # This worked!!! YAY
    """
    Input1 = 10
    Input2 = 20
    LabVIEW = win32com.client.Dispatch("Labview.Application")
    VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\Algorithm_test_VI\python.vi')    # path the LabVIEW VI
    pciVI._FlagAsMethod("Call")    # Flag "Call" as method
    pciVI.setcontrolvalue('Input 1', str(Input1))   # set first input
    pciVI.setcontrolvalue('Input 2', str(Input2))   # set first input
    pciVI.Call()   # Run the VI
    result = pciVI.getcontrolvalue('Sum')
    print(result)
    return
    """

    # This is the code for using pyVISA, but it doesn't support PXI devices at the moment (5/18/2017)
    """
    rm = pyvisa.ResourceManager()   # instantiate an object to manage all devices connected to the computer
    #print(rm.list_resources())  # show which things are connected to the computer
    deformable_mirror = rm.open_resource(PCI_BOARDS[board_num])
    lib = rm.visalib    # access the library for low-level "hardware" functions
    session = lib.open_default_resource_manager() # open hardware level manager of devices attached to the computer
    dm_session = lib.open(session[0], PCI_BOARDS[board_num]) # open access to the correct pci card
    lib.map_address(dm_session[0], pyvisa.constants.VI_PXI_BAR0_SPACE, 0, 0xFF) # connect the pci memory addresses to the program's memory addresses
    print(type(voltages[0]), 'voltages size')
    for i in range(voltages.size):   # for each of the 37 voltages
        lib.poke_8(dm_session[0], ACTUATOR_ADDRESSES[board_num][i], int(voltages[i]))   # write the voltage into the memory accessed by the pci card
    # //call viUnmapAddress?
    lib.close(session[0])  # close the pci card
    return """

def write_to_mirror(genes, dm_actuators):
    within_range = True # the genes are in range unless proven to be out of range
    for i in range(genes.size):  # for each gene
        within_range = True and (genes[i] >= 0) and (genes[i] <= 250) # check that the voltages are between 0 and 250
    if within_range:    # if all of the genes are within the correct range
        if  dm_actuators.fits_mirror(genes): # if the genes don't break the mirror
            genes = genes * 2.65  # multiply each voltage by 2.65 because this is a constant for Xinetics mirrors
            voltage_array = array_conversion(genes) # // do this
            send_to_board(genes[:19], genes[19:])
        else:
            print("Error: Tried writing the genes to the mirror, but they would've broken it")
    else:
        print('Error: Genes not in range (within the write_to_mirror function)')
    return

if __name__ == "__main__":
    print('You meant to run GeneticAlgorithm.py')
