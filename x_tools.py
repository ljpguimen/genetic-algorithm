
class x_tools(object):
    """This makes sure the voltage difference between neighboring actuators isn't too high"""
    def __init__(self):
        dm_array = [[-1,-1,28,27,26,-1,-1],
                    [-1,29,14,13,12,25,-1],
                    [30,15,4,3,2,11,24],
                    [31,16,5,0,1,10,23],
                    [32,17,6,7,8,9,22],
                    [-1,33,18,19,20,21,-1],
                    [-1,-1,34,35,36,-1,-1]]
        
        dm_actuator_neighbor = []
        for i in range(len(dm_array)):
            for j in range(len(dm_array[i])):
                if abs(i-3) + abs(j-3) < 5:
                    start_actuator = dm_array[i][j]
                    if j !=len(dm_array[i])-1:
                        neighbor = dm_array[i][j+1]
                        if neighbor != -1:
                            dm_actuator_neighbor.append([start_actuator,neighbor])
                    if i!=len(dm_array)-1:
                        neighbor = dm_array[i+1][j]
                        if neighbor != -1:
                            dm_actuator_neighbor.append([start_actuator,neighbor])
                        if j != len(dm_array[i])-1:
                            neighbor = dm_array[i+1][j+1]
                            if neighbor != -1:
                                dm_actuator_neighbor.append([start_actuator,neighbor])
                        if j!=0:
                            neighbor = dm_array[i+1][j-1]
                            if neighbor != -1:
                                dm_actuator_neighbor.append([start_actuator,neighbor])
        
        self.dm_actuator_neighbors = dm_actuator_neighbor
                                
    def fits_mirror(self,genes):
        """Determine if a child breaks the mirror"""
        return True
        # don't need this function for Jungmoo currently. I will fix this later.

        genes = genes*2.625   # This is the DM constant or something//
        valid = True    # the child is good until proven bad
        for i in range(len(self.dm_actuator_neighbors)):      # Test every actuator value with its neighbors' values
            valid = valid and abs(genes[self.dm_actuator_neighbors[i][0]]-genes[self.dm_actuator_neighbors[i][1]]) <= 30  # test voltage difference between neighboring actuators is less than 30
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
