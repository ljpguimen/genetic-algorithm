"""These functions manipulate the people generated in people.py"""
import numpy as np  # numpy is a python library for scientific computing

def test_people(child_group, parent_group, num_parents, num_children, dm_actuators):
    """determine the figure of merit for each parent and child"""
    figure_of_merit_matrix = np.empty(num_children + num_parents)       # initialize the figure of merit's matrix to have indices for each parent and child
    child_group.test_children(figure_of_merit_matrix, num_parents, dm_actuators)      # measure the children's figure of merit
    parent_group.test_parents(figure_of_merit_matrix, dm_actuators)      # measure the parents' figure of merit
    return figure_of_merit_matrix

def sort_people(figure_of_merit_matrix, parent_group, child_group, num_parents, num_init_parents = None):
    """find the top performing parents and children"""
    if num_init_parents is None:    # if the number initial parents isn't given
        num_init_parents = num_parents  # the number of initial parents is the number of parents
    unordered_best_indices = np.argpartition(-figure_of_merit_matrix, num_parents)[:num_parents]    # find indices of the best performing people
    best_people_indices = unordered_best_indices[np.argsort(-figure_of_merit_matrix[unordered_best_indices])]  # sort the best people from best to worst
    if best_people_indices[0] < num_init_parents:   # if the best person is a parent
        best_person = [parent_group.parents[best_people_indices[0]].genes, figure_of_merit_matrix[best_people_indices[0]]]    # store best person and their figure of merit
    else:   # since the best person isn't a parent, they must be a child
        best_person = [child_group.children[best_people_indices[0]-num_init_parents].genes, figure_of_merit_matrix[best_people_indices[0]]]    # store best person and their figure of merit
    best_parent_indices = np.empty(0, int)    # initialize the vector that will contain the indices of the best performing parents
    best_child_indices = np.empty(0, int)     # initialize the vector that will contain the indices of the best performing children
    for i in range(best_people_indices.size):   # determine whether each index is a parent or child
        if best_people_indices[i] < num_init_parents:   # if the index is less than the number of parents, the index corresponds to a parent
            best_parent_indices = np.append(best_parent_indices,best_people_indices[i])   # append this index to the best parent index array
        else:   # this index must correspond to a child
            best_child_indices = np.append(best_child_indices,best_people_indices[i]-num_init_parents)    # append this index to the best child index array
    if best_parent_indices.size == 0:   # if none of the parents were the best
        best_parent_indices = None      # set the array of indices to a None value
    if best_child_indices.size == 0:    # if none of the children were the best
        best_child_indices = None       # set the array of indices to a None value
    return best_parent_indices, best_child_indices, best_person