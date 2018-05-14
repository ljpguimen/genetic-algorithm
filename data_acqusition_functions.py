"""
This module opens up the specific data acquisition hardware and returns the desired output

Functions:
ic() -- Grabs an image from an IC camera
NI_DAQ_voltage() -- acquires a voltage from the NI hardware (usually connected to the lock-in amplifier)

"""

from pyicic.IC_ImagingControl import *
import numpy as np 
import copy

import win32com.client  # Use this when using the LabVIEW VI to get the NI DAQ data # Python ActiveX Client


class data_acqusition(object):
	"""description of class"""
	
	def __init__(self, device):
		self.device = device
		if (not ((device =="Andor") or (device == "NI DAQ") or (device == "IC"))):
			print("Error: The device you entered into data acquisition wasn't valid")
			exit()
		initialize_array = file_f.read_device_properties(self.device + "/" + self.device + " properties")
		if (device == "Andor"):
			initialize_andor(initialize_array)
		elif (device == "NI DAQ"):
			initialize_NI_DAQ(initialize_array)
		elif (device == "IC"):
			initialize_IC(initialize_array)


	def initialize_andor(self):
		return # TODO 

	def initialize_NI_DAQ(self, initialize_array):
		self.number_of_reads = initialize_array[0]
		LabVIEW = win32com.client.Dispatch("Labview.Application")   # Start running Labview
		self.pci0VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\get_average_photodiode_voltage.vi')    # path to the LabVIEW VI for the first board

	def initialize_IC(self):
		return # TODO



	def acquire(self):
		if (self.device == "Andor"):
			acquire_andor()
		elif (self.device == "NI DAQ"):
			acquire_NI_DAQ()
		elif (self.device == "IC"):
			acquire_IC()

	def acquire_andor(self):
		return # TODO

	def acquire_NI_DAQ(self):
		"""Compute figure of merit that is average voltage reading from DAQ
        
		Returns
		-------
		voltage: voltage, variable type unknown -> maybe float
			the averaged voltage read by the NI DAQ hardware
		"""
		
		self.pci0VI._FlagAsMethod("Call")    # Flag "Call" as the method to run the VI in this path
		self.pci0VI.setcontrolvalue('error in (no error)', 0)   # set error in
		self.pci0VI.setcontrolvalue('number of reads', self.number_of_reads)   # set addresses
		self.pci0VI.Call()   # Run the VI
		voltage = self.pci0VI.getcontrolvalue('voltage')    # retrieve error out
		error = self.pci0VI.getcontrolvalue('error out')    # retrieve error out
		if (error[1] != 0):   # check whether there was an error
			print('There was an error writing to board 0 at PXI4::5::INSTR')
			print('Error: ', error)
			print('Press anything and enter to exit...')
			input()
			exit()
		return voltage

	def acquire_IC(self):
		return # TODO

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



