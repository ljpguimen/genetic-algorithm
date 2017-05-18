import csv
import numpy as np
import time

# // enter the figure of merit as well
# // how to get the date in python
# // change reading from appending to initialized vector

def write_to_adf(array, filename):
    """Enter the //37 genes to write in the file as well as the filename without the .adf extenstion"""
    with open(filename + '.adf', 'w') as fileout:   # open the file to write values to
        tsvwriter = csv.writer(fileout, delimiter='\t') # write to the given file with values separated by tabs
        tsvwriter.writerow(['@ASCII_DATA_FILE'])    # start of the header
        tsvwriter.writerow(['NCurves=1'])   # number of genes which are output
        tsvwriter.writerow(['NPoints=39'])  # number of genes
        tsvwriter.writerow(['Subtitle={0} : {1}'.format(time.strftime("%m/%d/%y"), time.strftime("%I:%M %p"))])   # //insert date here
        tsvwriter.writerow(['Title=Save'])  # saving the file
        tsvwriter.writerow(['@END_HEADER']) # end the header
        for i in range(array.size):     # write each gene to the file
            tsvwriter.writerow([i+1, array[i]])     # write the index, a tab character, and then the gene's voltage
        tsvwriter.writerow([38, float(0)])  # this is the mutation amount
        tsvwriter.writerow([39, '4.980469E-3'])     # //this is the figure of merit

def read_adf(filename, num_genes):
    """Enter the filename as a string without the .adf extension at the end.
Also, it can only read the file if it is in the same folder as the program"""

    new_gene_array = np.empty(0, 'float')   # initialize array to hold the read genes
    with open(filename + '.adf', 'r') as filein:    # open the file to be read from
        tsvreader = csv.reader(filein, delimiter = '\t')    # make the values tab separated
        for row in tsvreader:   # for each row in the file
            if len(row) == 2:   # if the number of values in the row is 2
                if int(float(row[0])) <= num_genes:    # the first number is the index, only read in num_genes genes
                    new_gene_array = np.append(new_gene_array, int(float(row[1])))  # read in the second value as the gene voltage
    return new_gene_array


if __name__ == "__main__":
    print('You meant to run GeneticAlgorithm.py')
