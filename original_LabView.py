"""This function does exactly what the original labview program did"""
import math
import sys
import numpy as np

def x_tools(bool):
    return True
# Creates a given number of children based on the given parents' genes
def create_children(num_child, parent_matrix):
    """This creates children"""
    size = parent_matrix.shape    # size contains dimensions of parent_matrix
    num_genes = size[0]             # Each row contains a specified gene
    num_parents = size[1]           # Each column is a parent
    if num_parents > num_child:
        print('Error: You tried to create less children than parents')
        exit()
    else:
        new_child_matrix = np.zeros((num_child,num_genes),'float', 'C')     # initialize child matrix
        for i in range(num_child):          # Make 'num_child' children
            while True:          # Generate children until you make one that doesn't break the mirror
                new_child = np.zeros(num_genes,'float', 'C')        # Initialize the new child vector
                for j in range(num_genes):          # generate 'num_genes' genes in each child
                    new_gene_index = np.random.randint(0,num_parents)     # decide which parent to inherit the gene from
                    new_child[j] = parent_matrix[j, new_gene_index]      # inherit this gene from the random parent
                if x_tools(new_child) == True:   # Check if this child breaks the mirror
                    break       # if this child does not break the mirror, move on
            new_child_matrix[i] = new_child         # Insert this child to the child matrix
        new_child_matrix = np.transpose(new_child_matrix)     # Transpose so each child has its own column
    return new_child_matrix         # Output the generated children matrix

def genetic_mutation(children_matrix, mutation_percentage):
    mutation_percentage = mutation_percentage / 100     # convert from percentage to decimal
    mut_squared = mutation_percentage*mutation_percentage    # this is used for a gaussian distribution
    print('mut_squared', mut_squared)
    children_matrix = np.transpose(children_matrix)   # Transpose so each child has its own row
    for i in range(children_matrix.shape[0]):       # Mutate each child. Each i is a different child
        while True:     # Mutate each child until it doesn't break the mirror
            # Should also keep track of the original child in case the mutated child doesn't fit the mirror
            index = children_matrix[i].size - 2     # determine which index is the last gene
            rand_nums = np.random.random_integers(-10000,10000,children_matrix[i].size)/10000    # create num_genes number of random numbers from -1 to 1
            rand_nums2 = np.random.random_integers(0,10000,children_matrix[i].size)/10000    # Generate random number between 0 and 1
            vector_of_rand_nums = np.empty(0,float,'C')
            for j in range(children_matrix[i].size):        # Mutate every gene
                print('stuff\n', -rand_nums[j]*rand_nums[j]/mut_squared)
                new_num = math.exp(-rand_nums[j]*rand_nums[j]/mut_squared)      # generate number in gaussian distribution where the standard deviation is the mutation percentage
                print('gauss_num\n', new_num)
                if (rand_nums2[j] < new_num) and (j < index):    # if the generated number is less than a random number between 0 and 1, mutate the gene
                    new_gene = rand_nums[j]*100 + children_matrix[i][j]     # mutate the gene
                    if new_gene > -100 and new_gene < 100:     # new_gene is good if abs(new_gene) < 100
                        children_matrix[i][j] = abs(new_gene)   # pass on the new gene
                        vector_of_rand_nums = np.append(vector_of_rand_nums,rand_nums[j])      # remember this random number
                # Note: if one of the if statement conditions isn't met, the original gene is kept
            children_matrix[i][index] = np.mean(vector_of_rand_nums)     # this is the average amount of mutation for each child
            if x_tools(children_matrix[i]) == True:    # determine whether this child is safe for the mirror
                break
    children_matrix = children_matrix.transpose()
    return children_matrix

# Calculate the figure of merit for each child to compare
def social_efficiency_test(child_matrix):
    child_matrix = np.transpose(child_matrix)
    for i in len(child_matrix):     # Test each child
        [genes, mutation_ratio] = extract_genes(child_matrix[i])    # outputs the 37 genes and the mutation ratios for each child in a vector
        write_child_mirror(child_matrix[i])     # Put child on mirror
        #wait some number of milliseconds
        fig_of_merit = figure_of_merit()
        child_matrix[i][num_genes - 2] = mutation_ratio     # second to last index is amount the child was mutated
        child_matrix[i][num_genes - 1] = fig_of_merit     # Make matrix with data about the childrens' performance
    child_matrix = child_matrix.transpose()
    return new_child_matrix

# Add parents to child matrix
def add_parents(child_matrix, parent_matrix):
    return child_matrix.append(parent_matrix)

# Sorts each of the children by how well they perform
def sort_generation(child_matrix_with_parents):
    fig_of_merits_index = child_matrix_with_parents[child_matrix_with_parents.shape[0]]     # Access vector of figure of merits for each child
    # Sort this into highest and lowest
    # take the top "number of parents" number of children to become parents
    return  #best figure of merit values, indices of best children

def keep_best_people(chilren_matrix_with_parents):
    figure_of_merits, best_people_indices = sort_generation(child_matrix_with_parents)
    #create new parent_matrix made up of these people
    # save the best child
    return #best child, new_parent_matrix


num_children = 10
parent_matrix = np.full((5,1),30,'double', 'C')    # Create zeros array of size 2 x 2 containing float types and indexed like a C matrix
print('Parent')
print(parent_matrix)
child_matrix = create_children(num_children,parent_matrix)
print('Child')
print(child_matrix)
mutation_percent = 20
#x_tools(child_matrix)
print(genetic_mutation(child_matrix,mutation_percent))