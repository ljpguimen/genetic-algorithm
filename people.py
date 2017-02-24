import numpy as np
import math
import time
from mirror_functions import *
import csv

# // do I really need a amount mutated attribute?

class person(object):
    """A person contains some number of genes, a figure of merit, and a mutation amount"""
    def __init__(self, num_genes):
        self.genes = np.empty(num_genes, 'float', 'C')  # a person should have an empty array the size its number of genes
        self.amount_mutated = 0.0       # the person hasn't mutated at all when they are created
        self.num_genes = num_genes      # store the number of genes the person has

    def test_person(self):
        """write each person to the mirror for figure of merit measuring"""
        waiting_time = 0.01     # number of seconds to wait between writing voltages to the mirror and measuring the figure of merit 
        write_to_mirror()       # //write the genes to the mirror
        time.sleep(waiting_time)    # wait for the given amount of time
        return self.figure_of_merit_test()  # return the measured value

    def figure_of_merit_test(self):
        """measure the figure of merit of each person"""
        return float(np.random.randint(0, 100)) # //currently for test purposes
        


class parent(person):
    """Parent is a person with a good figure of merit who makes new children"""
    def __init__(self, num_genes, init_voltage = None, filename = None, person_genes = None):
        super().__init__(num_genes)     # inherit the attributes from the person class
        if not (init_voltage is None):
            for i in range(self.num_genes):    # for each gene in the parent
                self.genes[i] = init_voltage    # make each gene's value equal to the initial voltage
        elif not (file_values is None):
            for i in range(self.num_genes):
                self.genes[i] = file_values[i]
        elif not (person_genes is None):
            self.genes = person_genes
        else:
            print('Error: parent not initialized correctly')



class parent_group(object):
    """creates an array of parents"""
    def __init__(self, num_parents, num_genes, init_voltage = None, filename = None, best_child_indices = None, child_group = None, 
                 best_parent_indices = None, parent_group = None):   # //Change this to correspond to parent constructor
        self.num_genes = num_genes          # set the number of parents in the group
        self.num_parents = num_parents      # keep track of the number of genes in each parent
        if not (best_child_indices is None) and not (best_parent_indices is None):    # if indices of the child and parents were given//what if only the best were in the parents or only in the children
            parents = np.empty(0, parent)
            for i in range(best_child_indices.size):   # create i children
                parents = np.append(parents,parent(num_genes, None, None, child_group.children[best_child_indices[i]].genes))
            for i in range(best_parent_indices.size):
                parents = np.append(parents,parent(num_genes, None, None, parent_group.parents[best_parent_indices[i]].genes))
            self.parents = parents
        elif not (best_child_indices is None):
            parents = np.empty(0, parent)
            for i in range(best_child_indices.size):   # create i children
                parents = np.append(parents,parent(num_genes, None, None, child_group.children[best_child_indices[i]].genes))
            self.parents = parents
        elif not (best_parent_indices is None):
            parents = np.empty(0, parent)
            for i in range(best_parent_indices.size):
                parents = np.append(parents,parent(num_genes, None, None, parent_group.parents[best_parent_indices[i]].genes))
            self.parents = parents
        elif not (init_voltage is None):    # if an initial voltage is given
            self.parents = np.full((num_parents),parent(num_genes, init_voltage),parent,'C')    # create an array of parents where every gene is the initial voltage
        elif not (filename is None):
            # make sure filename is a string
            with open(filename, 'r') as f:
                return [float(row[1]) for row in csv.reader(f, delimiter='\t')]
            self.parents = np.full((num_parents),parent(num_genes, None, filename),parent,'C')    # create an array of parents from the file
        else:
            print("Error: parents weren't initialized correctly")   # the correct output arguments weren't given

    def read_voltages_from_file(self, filename):
        return #//idk how to do this yet

    def test_parents(self, figure_of_merit_matrix):
        """determine the figure of merit of each parent""" 
        for i in range(self.num_parents):   # test each parent
            figure_of_merit = self.parents[i].test_person()     # seave each figure of merit
            figure_of_merit_matrix[i] = figure_of_merit     # put this figure of merit (FOM) in a matrix with the rest of the FOM's



class child(person):
    """Child contains genes (actuator voltages), figure of merit, and mutation amount"""
    def __init__(self, num_genes, parent_group):
        super().__init__(num_genes)     # inherit the attributes from the person class
        self.inherit_genes(parent_group)    # inherit genes from the parent(s) who are making children

    def inherit_genes(self, parent_group):
        """inherit each gene from a random parent"""
        while True:     # keep inheriting genes until the child doesn't break the mirror
            for j in range(self.num_genes):     # for each of the child's genes
                random_parent = np.random.randint(0,parent_group.num_parents)   # choose a random parent to inherit from
                self.genes[j] = parent_group.parents[random_parent].genes[j]    # inherit the jth gene from this random parent
            if True:     # check if the child breaks the mirror
                break       # if the child doesn't break the mirror, leave the while loop

    def mutate(self, mut_squared):
        """mutates each child according to the mutation percentage given"""
        while True:     # Make sure the mutated child doesn't break the mirror
            old_genes = self.genes  # don't mutate the genes directly in case the mutated genes break the mirror
            mutation_vector = np.empty(0,float,'C')     # Initialize vector to store the amounts that genes are mutated by
            mutation_amount = np.random.random_integers(-10000,10000,self.num_genes)/10000    # create num_genes number of random numbers from -1 to 1
            mutation_condition = np.random.random_integers(0,10000,self.num_genes)/10000    # Generate num_genes number of random numbers from 0 and 1
            for j in range(self.num_genes):        # Attempt to mutate every gene
                gauss_num = math.exp(-mutation_amount[j]*mutation_amount[j]/mut_squared)      # Generate random number in a gaussian distribution
                if (mutation_condition[j] < gauss_num):    # this makes smaller mutations more probable
                    new_gene = abs(mutation_amount[j]*100 + old_genes[j])     # mutate the gene
                    if new_gene < 100:     # new_gene is good if abs(new_gene) < 100
                        old_genes[j] = new_gene  # pass on the new gene
                        mutation_vector = np.append(mutation_vector, mutation_amount[j])      # remember the amount of mutation for that gene
                # Note: if one of the if statement conditions isn't met, the original gene is kept
            if True:    # determine whether this child is safe for the mirror
                print(self.genes)
                if mutation_vector.size:    # if there were any mutations
                    self.amount_mutated = np.mean(mutation_vector)     # store the amount this gene was mutated by
                self.genes = old_genes      # the child's new genes are the successfully mutated genes
                break   # get out of the while loop and exit the function



class child_group(object):
    """creates an array of children"""
    def __init__(self, num_children, parent_group):
        if parent_group.num_parents > num_children:     # create more children than parents
            print('Error: You tried to create less children than parents')
        self.num_genes = parent_group.num_genes     # the number of genes in each child is the same as the number of genes in each parent
        self.num_children = num_children        # set the number of children
        children = np.empty(0)      # initialize the children matrix
        for i in range(num_children):   # create i children
            children = np.append(children,child(self.num_genes,parent_group))   # append a new child onto the children array
        # Note: must append the children instead of initializing becuase initializing creates num_children instances of the same child in the vector
        self.children = children    # set this array to be the children attribute

    def mutate(self, mutation_percentage):
        """Mutates approximately the mutation percentage proportion of children"""
        mutation = mutation_percentage / 100    # convert the percentage to a decimal
        mutation_squared = mutation*mutation    # square the mutation percentage for later use
        for i in range(self.num_children):   # Mutate each child
            self.children[i].mutate(mutation_squared)        # call the mutate attribute    

    def test_children(self, figure_of_merit_matrix, num_parents):
        """determine the figure of merit for each child"""
        for i in range(self.num_children):  # test each child's performance
            figure_of_merit = self.children[i].test_person()    # measure the figure of merit of the child
            figure_of_merit_matrix[num_parents+i] = figure_of_merit     # put this value in the matrix in the indices after the indices allotted for the parents
        return figure_of_merit_matrix
