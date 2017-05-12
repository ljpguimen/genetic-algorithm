"""These functions check whether the genes break the mirror and write genes to the mirror"""

import pyvisa
from PyDAQmx import *
import numpy as np

# // comment
# // comment under each function
PCI_BOARDS = ["PXI4::5::INSTR", "PXI4::4::INSTR"]
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

def send_to_board(board_num, voltages):
    # Declaration of variable passed by reference
    taskHandle = TaskHandle()
    read = int32()
    data = np.zeros((1000,), dtype=np.float64)

    try:
        # DAQmx Configure Code
        DAQmxCreateTask("",byref(taskHandle))
        DAQmxGetDevAOPhysicalChans(PCI_BOARDS[board_num], byref(data), bufferSize)
        print(data)
        DAQmxCreateAIVoltageChan(taskHandle,PCI_BOARDS[board_num],"",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

        # DAQmx Start Code
        DAQmxStartTask(taskHandle)

        # DAQmx Read Code
        DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

        print( "Acquired %d points",%read.value)
    except DAQError as err:
        print ("DAQmx Error: %s", %err)
    finally:
        if taskHandle:
            # DAQmx Stop Code
            DAQmxStopTask(taskHandle)
            DAQmxClearTask(taskHandle)
    return


    # This is the code for using pyVISA
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
            print(genes.size,'genes size')
            send_to_board(FIRST_BOARD, genes[:19])
            send_to_board(SECOND_BOARD, genes[20:])
        else:
            print("Error: Tried writing the genes to the mirror, but they would've broken it")
    else:
        print('Error: Genes not in range (within the write_to_mirror function)')
    return

if __name__ == "__main__":
    print('You meant to run GeneticAlgorithm.py')
