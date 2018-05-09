"""These functions calculate the figure of merit for each person

Functions:
test_genes() -- Change any variable value in the program utilizing user input.
"""
NUMBER_OF_READS = 50

import win32com.client  # Use this when using the LabVIEW VI in send_to_board # Python ActiveX Client

def test_genes(genes):
    """Compute figure of merit that is least squares of y = index_value
    
    Parameters
    ----------
    genes: genes, 1D numpy array
        the genes or actuator voltages to be tested
    
    Returns
    -------
    figure_of_merit: figure of merit, variable type
        the measure of how good the mirror shape achieved a desired goal
    """
    
    LabVIEW = win32com.client.Dispatch("Labview.Application")   # Start running Labview
    pci0VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\get_average_photodiode_voltage.vi')    # path to the LabVIEW VI for the first board
    pci0VI._FlagAsMethod("Call")    # Flag "Call" as the method to run the VI in this path
    pci0VI.setcontrolvalue('error in (no error)', 0)   # set error in
    pci0VI.setcontrolvalue('number of reads', NUMBER_OF_READS)   # set addresses
    pci0VI.Call()   # Run the VI
    voltage = pci0VI.getcontrolvalue('voltage')    # retrieve error out
    error = pci0VI.getcontrolvalue('error out')    # retrieve error out
    if (error[1] != 0):   # check whether there was an error
        print('There was an error writing to board 0 at PXI4::5::INSTR')
        print('Error: ', error)
        print('Press anything and enter to exit...')
        input()
        exit()
    return -voltage

    
    # LabVIEW = win32com.client.Dispatch("Labview.Application")   # Start running Labview
    # pci0VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\get_average_photodiode_voltage.vi')    # path to the LabVIEW VI for the first board
    # pci0VI._FlagAsMethod("Call")    # Flag "Call" as the method to run the VI in this path
    # pci0VI.Call()   # Run the VI
    # FWHM = pci0VI.getcontrolvalue('FWHM (fs)')    # retrieve error out
    # if (error[1] != 0):   # check whether there was an error
    #     print('There was an error writing to board 0 at PXI4::5::INSTR')
    #     print('Error: ', error)
    #     print('Press anything and enter to exit...')
    #     input()
    #     exit()
    # return FWHM