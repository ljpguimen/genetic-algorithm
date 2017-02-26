import csv
import numpy as np
import msvcrt
import time

def write_to_adf(array):
    # ask for user input as to what they want the file to be named
    filename = 'test'
    with open(filename + '.adf', 'w') as fileout:
        tsvwriter = csv.writer(fileout, delimiter='\t')
        tsvwriter.writerow(['@ASCII_DATA_FILE'])
        tsvwriter.writerow(['NCurves=1'])
        tsvwriter.writerow(['NPoints=39'])
        tsvwriter.writerow(['Subtitle='])#insert date here
        tsvwriter.writerow(['Title=Save'])
        tsvwriter.writerow(['@END_HEADER'])
        for i in range(array.size):
            tsvwriter.writerow([i+1, array[i]])
        tsvwriter.writerow([38, float(0)])
        tsvwriter.writerow([39, '4.980469E-3'])

def read_adf(filename, num_genes):
    new_gene_array = np.empty(0, 'float')
    with open(filename + '.adf', 'r') as filein:
        tsvreader = csv.reader(filein, delimiter = '\t')
        for row in tsvreader:
            if len(row) == 2:
                if int(row[0]) <= num_genes:
                    new_gene_array = np.append(new_gene_array, row[1])
    return new_gene_array
"""
num_genes = 37
filename = 'test'
array = np.full(37, 30, 'float')
write_to_adf(array)
gene_array = read_adf(filename, num_genes)
print('gene_array\n')
print(gene_array)
print('array size ' + str(gene_array.size))
"""