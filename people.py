import numpy as np
import math
import time
from x_tools import x_tools

# // do I really need a figure of merit attribute?
"""Note, x_tools only returns True because I was told I did not need to finish it"""
check_genes = x_tools() # this checks whether a set of genes fits on the mirror without breaking it

def write_to_mirror():
    return # //write this function

class person(object):
    """A person contains some number of genes, a figure of merit, and a mutation amount"""
    def __init__(self, num_genes):
        self.genes = np.empty(num_genes, 'float', 'C')  # a person should have an empty array the size its number of genes
        self.figure_of_merit = None     # wait to define the person's figure of merit
        self.amount_mutated = 0.0       # the person hasn't mutated at all when they are created
        self.num_genes = num_genes      # store the number of genes the person has

    def test_person(self):
        num_seconds_to_wait = 0.01
        write_to_mirror()
        time.sleep(num_seconds_to_wait)
        return self.figure_of_merit_test()

    def figure_of_merit_test(self):
        return float(np.random.randint(0, 100))
        
class parent(person):
    """Parent is a child with a good figure of merit who can make children"""
    def __init__(self, num_genes, init_voltage = None, filename = None, child = None):  # //Change this as needed
        super().__init__(num_genes)     # inherit the attributes from the person class
        for i in range(self.genes.size):    # for each gene in the parent
            self.genes[i] = init_voltage    # make each gene's value equal to the initial voltage

class child(person):
    """Child contains genes (actuator voltages), figure of merit, and mutation amount"""
    def __init__(self, num_genes, parent_group):
        super().__init__(num_genes)     # inherit the attributes from the person class
        self.inherit_genes(parent_group)    # inherit genes from the parent(s) who are making children

    def inherit_genes(self, parent_group):
        while True:     # keep inheriting genes until the child doesn't break the mirror
            for j in range(self.num_genes):     # for each of the child's genes
                random_parent = np.random.randint(0,parent_group.num_parents)   # choose a random parent to inherit from
                self.genes[j] = parent_group.parents[random_parent].genes[j]    # inherit the jth gene from this random parent
            if check_genes.fits_mirror(self.genes):     # check if the child breaks the mirror
                break       # if the child doesn't break the mirror, leave the while loop

    def mutate(self, mut_squared):
        while True:     # Make sure the mutated child doesn't break the mirror
            old_genes = self.genes
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
            if check_genes.fits_mirror(old_genes):    # determine whether this child is safe for the mirror
                print(self.genes)
                if mutation_vector.size:    # if there were any mutations
                    self.amount_mutated = np.mean(mutation_vector)     # store the amount this gene was mutated by
                self.genes = old_genes      # the child's new genes are the successfully mutated genes
                break   # get out of the while loop and exit the function

            
class parent_group(object):
    """parent_group contains an array of parents"""
    def __init__(self, num_parents, num_genes, init_voltage):   # //Change this to correspond to parent constructor
        #if init_voltage isn't given, make it 30//
        self.parents = np.full((num_parents),parent(num_genes, init_voltage),parent,'C')
        self.num_parents = num_parents
        self.num_genes = num_genes

    def set_constant_voltage(self, voltage):
        parents = np.full((num_parents,num_genes),voltage,'float','C')

    def read_voltages_from_file(self, filename):
        return #//idk how to do this yet

    def test_parents(self):
        for i in range(self.num_parents):
            self.parents[i].test_person()

class child_group(object):
    """child_group contains an array of children"""
    def __init__(self, num_children, parent_group):
        if parent_group.num_parents > num_children:
            print('Error: You tried to create less children than parents')
        self.num_genes = parent_group.num_genes
        self.num_children = num_children
        children = np.empty(0)
        for i in range(num_children):
            children = np.append(children,child(self.num_genes,parent_group))
        self.children = children

    def mutate(self, mutation_percentage):
        """Mutates approximately the mutation percentage proportion of children"""
        mutation = mutation_percentage / 100
        mutation_squared = mutation*mutation
        for i in range(self.num_children):   # Mutate each child
            self.children[i].mutate(mutation_squared)            

    def test_children(self):
        figure_of_merit_matrix # doesn't work
        for i in range(self.num_children):
            fig_of_merit = self.children[i].test_person()
            figure_of_merit_matrix = figure_of_merit_matrix.append([fig_of_merit, i])
        return figure_of_merit_matrix

def test_people(child_group, parent_group):
    print(child_group.test_children())
    parent_group.test_parents()

def sort_people(child_group, parent_group):
    figures_of_merit = np.empty((child_group.num_children+parent_group.num_parents))
    for i in range(parent_group.num_parents):
        parent_group.parents[i].figure_of_merit