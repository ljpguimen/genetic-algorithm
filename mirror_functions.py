"""These functions check whether the genes break the mirror and write genes to the mirror"""

import pyvisa

# // comment
# // connect to mirror

PCI_BOARDS = ['PXI4::5::INSTR', 'PXI4::4::INSTR']
ACTUATOR_ADDRESSES = [[],[]]
FIRST_ADDRESSES = 0
SECOND_ADDRESSES = 1

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

    def fits_mirror(self,genes):
        """Determine if a child breaks the mirror"""
        genes = genes*2.625   # This is the DM constant used in the original code
        valid = True    # the child is good until proven bad
        for i in range(len(self.dm_actuator_neighbors)):      # Test every actuator value with its neighbors' values
            valid = valid and (abs(genes[self.dm_actuator_neighbors[i][0]]-genes[self.dm_actuator_neighbors[i][1]]) <= 30)  # test voltage difference between neighboring actuators is less than 30
        return valid
    

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
print('dm_neighbors shape[0] ' + str(len(dm_neighbors)))
dm_neighbors.sort()
print(dm_neighbors)
print(dm_actuator_neighbor == dm_neighbors)
"""

def array_conversion(genes):    # // write this function
    return genes

def write_to_board(address, voltages):
    pci_card = pyvisa.ResourceManager()
    print(pci_card)
    print(pci_card.list_resources())
    deformable_mirror = pci_card.open_resource(PCI_BOARDS[address])
    lib = pci_card.visalib
    session = lib.open_default_resource_manager()
    dm_session = lib.open(session, PCI_BOARDS[address])
    lib.map_address(dm_session, 'PXI BAR0', 0, 255)
    for i in range(voltages):
        lib.poke_8(dm_session, addresses[i], voltages[i])
    lib.close(session)
    return

def write_to_mirror(genes, dm_actuators):
    within_range = True # the genes are in range unless proven to be out of range
    for i in range(genes.size):  # for each gene
        within_range = True and (genes[i] >= 0) and (genes[i] <= 250) # check that the voltages are between 0 and 250
    if within_range:    # if all of the genes are within the correct range
        if dm_actuators.fits_mirror(genes): # if the genes don't break the mirror
            genes = genes * 2.65  # multiply each voltage by 2.65 because this is a constant for Xinetics mirrors
            voltage_array = array_conversion(genes) # //
            write_to_board(FIRST_ADDRESSES, genes[:18])
            write_to_board(SECOND_ADDRESSES, genes[18:])
        else:
            print("Error: Tried writing the genes to the mirror, but they would've broken it")
    else:
        print('Error: Genes not in range')
    return

if __name__ == "__main__":
    print('You meant to run GeneticAlgorithm.py')
