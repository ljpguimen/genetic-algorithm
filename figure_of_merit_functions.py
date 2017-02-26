def test_genes(genes):
    """Compute figure of merit that is least squares of y = index_value"""
    figure_of_merit = 0
    for i in range(genes.size):
        figure_of_merit = figure_of_merit + (genes[i]-i)*(genes[i]-i)
    return -figure_of_merit