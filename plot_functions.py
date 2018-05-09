"""This file plots the graph of figures of merit and the mirror shape

Functions:
plot_performance() -- plots the figures of merit of the given people
plot_mirror() -- shows the mirror shape
"""

# TODO plot mirror function
# TODO first plot overhead and then faster every other time

import numpy as np
import matplotlib.pyplot as plt

def plot_performance(iteration_number, figures_of_merit):
    """plot the figures of merit for the current generation with the previous generations

    Parameters
    ----------
    iteration_number : the iteration number, int 
        The number of iterations the algorithm has gone through
    figures_of_merit : figures of merit, numpy 1d array
        This contains current best figures of merit.


    Returns
    -------
    iteration_number : the iteration number, int 
        The number of iterations the algorithm has gone through
    past_figures_of_merit : past figures of merit, numpy 2d array
        This contains figures of merit from all of the previous generations.
    """
    if iteration_number == 0:
        plt.figure(1)   # set the figure to be plotting to
        plt.ion()   # enable interactive mode so we can continuously draw on the graph
        plt.show()  # show the plot window
        plt.title('Figures of merit progression')   
        plt.xlabel('Iterations')
        plt.ylabel('Figures of merit')
    iteration_number = iteration_number + 1 # add one to the number of iterations
    iteration_vector = np.arange(0, iteration_number+1) # make a vector of [0, 1, 2, ... iteration_number]
    for i in range(0, figures_of_merit.shape[0]):
        plt.plot(iteration_vector, figures_of_merit[i], '-')    # plot the progression of this ith best figure of merit
    plt.draw()  # draw these things on the graph
    plt.pause(.001)     # pause the program so the plot can be updated
    return iteration_number, figures_of_merit