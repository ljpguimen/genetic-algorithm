"""
This module opens up the specific data acquisition hardware and returns the desired output

Functions:
ic() -- Grabs an image from an IC camera
NI_DAQ_voltage() -- acquires a voltage from the NI hardware (usually connected to the lock-in amplifier)

"""

# TODO get rid of # in front of exit()

import numpy as np 
import file_functions as file_f
import os

# These libraries are needed for IC cameras
#from pyicic.IC_ImagingControl import *
#import copy

# This is needed for the NI DAQ
import win32com.client	# Python ActiveX Client

# These libraries are needed for the Andor camera
import ctypes	
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class data_acqusition(object):
	"""description of class"""
	
	def __init__(self, device):
		self.device = device
		if (not ((device =="Andor") or (device == "NI DAQ") or (device == "IC"))):
			print("Error: The device you entered into data acquisition wasn't valid")
			exit()
		initialize_array = file_f.read_device_properties("\\"+ self.device + "\\" + self.device + " properties.txt")
		if (device == "Andor"):
			self.__initialize_andor(initialize_array)
		elif (device == "NI DAQ"):
			self.__initialize_NI_DAQ(initialize_array)
		elif (device == "IC"):
			self.__initialize_IC(initialize_array)

	def __check_success(self, error_value, function_name):
		if (error_value != 20002):
			print(function_name,"Error", error_value)
			#exit()

	def __initialize_andor(self, initialize_array):
		read_mode_top = int(initialize_array[0])	# readout mode options: 0 Full Vertical binning;	1 Multi-Track;	2 Random-Track;	 3 Single-Track;	4 Image;
		acquisition_mode_top = int(initialize_array[1])	# acquisition mode options: 1 Single scan;	2 Accumulate;	3 Kinetics;	 4 Fast Kinetics;	5 Run till abort;
		exposure_time_top = float(initialize_array[2])		# time in seconds
		trigger_mode_top = int(initialize_array[3])	# trigger mode options:	0 internal;	1 external;	6 external start;	7 external exposure (bulb);	9 external FVB EM;	10 software trigger;	12 external charge shifting;
		horizontal_binning_top = int(initialize_array[4])
		vertical_binning_top = int(initialize_array[5])
		horizontal_start_top = int(initialize_array[6])
		horizontal_end_top = int(initialize_array[7])
		vertical_start_top = int(initialize_array[8])
		vertical_end_top = int(initialize_array[9])


		
		
		# Load the atmcd64.dll file 
		directory_path = os.path.dirname(os.path.abspath(__file__)) # get the current directory's path
		self.andor_dll = ctypes.cdll.LoadLibrary(directory_path + '\\Andor\\atmcd64d.dll')


		# Initialize camera
		aBuffer = ctypes.c_char_p()		# The buffer tells the initialize function where the driver files are. Currently, they're in the same folder as this .py file

		error_value = self.andor_dll.Initialize(aBuffer)
		self.__check_success(error_value, "Initialize")


		# Determine size (in pixels of camera)
		gblXPixels = ctypes.c_int()		# Total number of horizontal pixels
		gblYPixels = ctypes.c_int()		# Total number of vertical pixels

		error_value = self.andor_dll.GetDetector(ctypes.byref(gblXPixels),ctypes.byref(gblYPixels))
		self.__check_success(error_value,"GetDetector")

		# Set vertical shift speed to recommended value
		vertical_shift_index = ctypes.c_int()	# the index to access specific vertical shift speeds 
		vertical_speed = ctypes.c_float()	# speed of the vertical speed shift in microseconds per pixel shift

		error_value = self.andor_dll.GetFastestRecommendedVSSpeed(ctypes.byref(vertical_shift_index),ctypes.byref(vertical_speed))
		self.__check_success(error_value,"Get Fastest Recommended Vertical Shift Speed")
		error_value = self.andor_dll.SetVSSpeed(vertical_shift_index)
		self.__check_success(error_value,"Set Vertical Shift Speed")


		# Set horizontal shift speed to the maximum
		horizontal_shift_index = ctypes.c_int(0)		# the index to access specific horizontal shift speeds
		AD_converter_index = ctypes.c_int()				# the specific index to access a given A-D converter
		number_AD = ctypes.c_int(0)						# the number of A-D converters in the camera
		number_speeds = ctypes.c_int()					# number of speeds available
		horizontal_speed = ctypes.c_float()				# horizontal shift speed
		max_horizontal_speed = ctypes.c_float(0)		# maximum horizontal speed

		error_value = self.andor_dll.GetNumberADChannels(ctypes.byref(number_AD))
		self.__check_success(error_value,"Get Number AD Channels")

		for each_AD in range(number_AD.value):
			error_value = self.andor_dll.GetNumberHSSpeeds(AD_converter_index, ctypes.c_int(0), ctypes.byref(number_speeds))
			self.__check_success(error_value, "Get Number Horizontal Shift Speeds")
			for each_speed_index in range(number_speeds.value):
				error_value = self.andor_dll.GetHSSpeed(ctypes.c_int(each_AD),ctypes.c_int(0),ctypes.c_int(each_speed_index),ctypes.byref(horizontal_speed))
				self.__check_success(error_value,"Get Horizontal Shift Speed")
				if (horizontal_speed.value > max_horizontal_speed.value):
					max_horizontal_speed.value = horizontal_speed.value
					horizontal_shift_index = ctypes.c_int(each_speed_index)
					AD_converter_index = ctypes.c_int(each_AD)
	
		error_value = self.andor_dll.SetADChannel(AD_converter_index)
		self.__check_success(error_value,"Set AD Channel")

		error_value = self.andor_dll.SetHSSpeed(ctypes.c_int(0), horizontal_shift_index)
		self.__check_success(error_value, "Set Horizontal Speed Index")

		# Turn the camera cooler on
		error_value = self.andor_dll.CoolerON()
		self.__check_success(error_value,"Turn Cooler On")


		# Check to make sure cooler is on
		cooler_on = ctypes.c_int()

		error_value = self.andor_dll.IsCoolerOn(ctypes.byref(cooler_on))
		self.__check_success(error_value, "Check if cooler is on")
		if (cooler_on.value != 1):
			print("Error: Cooler not on", "Exiting...")
			#exit()

		# Set the readout mode of the camera 
		read_mode = ctypes.c_int(read_mode_top)		
		error_value = self.andor_dll.SetReadMode(read_mode)
		self.__check_success(error_value,"Set Read Mode")


		# Set the acquisition mode
		acquisition_mode = ctypes.c_int(acquisition_mode_top)		
		error_value = self.andor_dll.SetAcquisitionMode(acquisition_mode)
		self.__check_success(error_value,"Set Acquisition Mode")


		# Set exposure time
		exposure_time = ctypes.c_float(exposure_time_top)		# time in seconds
		error_value = self.andor_dll.SetExposureTime(exposure_time)
		self.__check_success(error_value, "Set Exposure Time")

	
		# Set trigger mode
		trigger_mode = ctypes.c_int(trigger_mode_top)	
		error_value = self.andor_dll.SetTriggerMode(trigger_mode)
		self.__check_success(error_value, "Set Trigger Mode")

		# TODO Set up accumulation and kinetic capture & probs not video
		"""
		// only needed for accumulation acquisition 

		//float accumulation_cycle_time = .1; // seconds
		//errorValue = SetAccumulationCycleTime(accumulation_cycle_time);
		//if (errorValue != DRV_SUCCESS) {
		//std::cout << "Set accumulation cycle time Error\n";
		//std::cout << "Error: " << errorValue << "\n";
		//}
	
		//Only needed for kinetic capture

		//errorValue = SetBaselineClamp(1);
		//if (errorValue != DRV_SUCCESS) {
		//std::cout << "Set Baseline Clamp Error\n";
		//std::cout << "Error: " << errorValue << "\n";
		//}
	
		"""

	
		# Determine the actual times the camera is using for acquisition
		actual_exposure_time = ctypes.c_float()
		actual_accumulate_time = ctypes.c_float()
		actual_kinetic_time = ctypes.c_float()

		error_value = self.andor_dll.GetAcquisitionTimings(ctypes.byref(actual_exposure_time),ctypes.byref(actual_accumulate_time),ctypes.byref(actual_kinetic_time))
		self.__check_success(error_value, "Get Acquisition Timings")

		print('Exposure time is ', actual_exposure_time.value)

		# Set the horizontal and vertical binning and the area of the image to be captured
		horizontal_binning = ctypes.c_int(horizontal_binning_top)		# Number of pixels to bin horizontally
		vertical_binning = ctypes.c_int(vertical_binning_top)			# Number of pixels to bin vertically
		horizontal_start = ctypes.c_int(horizontal_start_top)			# Start column of image to be taken (inclusive)
		horizontal_end = ctypes.c_int(horizontal_end_top) 		# End column of image to be taken (inclusive)
		vertical_start = ctypes.c_int(vertical_start_top)			# Start row of image to be taken (inclusive)
		vertical_end = ctypes.c_int(vertical_end_top)		# End row of image to be taken (inclusive)

		self.number_x_pixels = horizontal_end_top - horizontal_start_top + 1
		self.number_y_pixels = vertical_end_top - vertical_start_top + 1

		error_value = self.andor_dll.SetImage(horizontal_binning, vertical_binning, horizontal_start, horizontal_end, vertical_start, vertical_end);
		self.__check_success(error_value, "Set Image")

	def __initialize_NI_DAQ(self, initialize_array):
		self.number_of_reads = initialize_array[0]
		LabVIEW = win32com.client.Dispatch("Labview.Application")   # Start running Labview
		self.pci0VI = LabVIEW.getvireference('C:\\Users\lambdacubed\Desktop\Mark\genetic_algorithm_python\get_average_photodiode_voltage.vi')    # path to the LabVIEW VI for the first board

	def __initialize_IC(self, initialize_array):
		return # TODO



	def acquire(self):
		if (self.device == "Andor"):
			self.__acquire_andor()
		elif (self.device == "NI DAQ"):
			self.__acquire_NI_DAQ()
		elif (self.device == "IC"):
			self.__acquire_IC()

	def __acquire_andor(self):
		camera_status = ctypes.c_int()
		error_value = self.andor_dll.GetStatus(ctypes.byref(camera_status))
		self.__check_success(error_value, "Get Camera Status")
		while (camera_status.value != 20073):	
			error_value = self.andor_dll.GetStatus(ctypes.byref(camera_status))
			self.__check_success(error_value, "Get Camera Status")

		# Start the acquisition process 
		error_value = self.andor_dll.StartAcquisition()
		acquiring = self.__check_success(error_value, "Start Acquisition")
		if (acquiring == False):
			self.andor_dll.AbortAcquisition()


			# Wait until the acquisition is complete
			error_value = self.andor_dll.GetStatus(ctypes.byref(camera_status))
			self.__check_success(error_value, "Get Camera Status")
			while (camera_status.value != 20073): 
				error_value = self.andor_dll.GetStatus(ctypes.byref(camera_status))
				self.__check_success(error_value, "Get Camera Status")
				#print("Camera Status is ", camera_status.value)

			# Get the image data from the camera
			size = ctypes.c_int(self.number_x_pixels*self.number_y_pixels)
			image_pointer = ctypes.cast(ctypes.create_string_buffer( size.value*ctypes.sizeof(ctypes.c_long()) ),ctypes.POINTER(ctypes.c_long))

			error_value = self.andor_dll.GetAcquiredData(image_pointer, size)
			self.__check_success(error_value, "Get Acquired Data")

			# TODO make this not a nested for loop
			# Transfer the image from a pointer to a numpy array
			image = np.zeros((self.number_y_pixels,self.number_x_pixels))
			for x in range(self.number_x_pixels):
				for y in range(self.number_y_pixels):
					image[y,x] = image_pointer[x + y*self.number_x_pixels]

			plt.imsave('filename.png', image, cmap=cm.gray)

	def __acquire_NI_DAQ(self):
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

	def __acquire_IC(self):
		return # TODO

	def shut_down(self):
		if (self.device == "Andor"):
			self.__shut_down_andor()
		elif (self.device == "NI DAQ"):
			self.__shut_down_NI_DAQ()
		elif (self.device == "IC"):
			self.__shut_down_IC()

	def __shut_down_andor(self):
		error_value = self.andor_dll.ShutDown()
		self.__check_success(error_value, "Shut down")

	def __shut_down_NI_DAQ(self):
		return

	def __shut_down_IC(self):
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



if __name__ == "__main__":
	device = data_acqusition("Andor")
	device.shut_down()