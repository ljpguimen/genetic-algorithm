"""
This module opens up the specific data acquisition hardware and returns the desired output

Functions:
ic() -- Grabs an image from an IC camera
NI_DAQ_voltage() -- acquires a voltage from the NI hardware (usually connected to the lock-in amplifier)

"""

from pyicic.IC_ImagingControl import *
import numpy as np 
import copy


def ic():


	ic_ic = IC_ImagingControl()
	ic_ic.init_library()

	# open first available camera device
	cam_names = ic_ic.get_unique_device_names()
	# print(cam_names)
	cam = ic_ic.get_device(cam_names[0])
	cam.open()
	cam.reset_properties()

	# change camera properties
	# print(cam.list_property_names())         # ['gain', 'exposure', 'hue', etc...]
	cam.gain.auto = False                    # enable auto gain
	
	cam.exposure.value = -5

	# change camera settings
	formats = cam.list_video_formats()
	# print formats
	cam.set_video_format(formats[0])        # use first available video format
	cam.enable_continuous_mode(True)        # image in continuous mode
	cam.start_live(show_display=False)       # start imaging

	cam.enable_trigger(True)                # camera will wait for trigger
	if not cam.callback_registered:
		cam.register_frame_ready_callback() # needed to wait for frame ready callback

	cam.reset_frame_ready() 
		
	cam.send_trigger()

	cam.wait_til_frame_ready(1000)              # wait for frame ready due to trigger

	data, width, height, depth = cam.get_image_data()
	frame = np.ndarray(buffer=data,dtype=np.uint8,shape=(height, width, depth))
	frameout = copy.deepcopy(frame).astype(float)
	
	del frame
	# print(frameout.max())

	cam.stop_live()
	cam.close()

	ic_ic.close_library()
	
	return frameout


import win32com.client  # Use this when using the LabVIEW VI in send_to_board # Python ActiveX Client


def NI_DAQ_voltage():
    """Compute figure of merit that is least squares of y = index_value
        
    Returns
    -------
    voltage: voltage, variable type unknown -> maybe float
        the averaged voltage read by the NI DAQ hardware
    """

    NUMBER_OF_READS = 50

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
    return voltage