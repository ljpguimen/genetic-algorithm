import ctypes
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

#TODO: change directory to organize various different libraries used

# These functions are all detailed in the ANDOR "Software Development Kit.pdf" which should be located in the folder with this program
# The error codes are also found in that document (e.g. DRV_SUCCESS == 20002, DRV_IDLE == 20073)

def check_success(error_value, function_name):
	if (error_value != 20002):
		print(function_name,"Error", error_value)
		exit()

def main():
	
	read_mode_top = 4	# readout mode options: 0 Full Vertical binning;	1 Multi-Track;	2 Random-Track;	 3 Single-Track;	4 Image;


	# Load the atmcd64.dll file 
	andor_dll = ctypes.cdll.atmcd64d


	# Initialize camera
	aBuffer = ctypes.c_char_p()		# The buffer tells the initialize function where the driver files are. Currently, they're in the same folder as this .py file

	error_value = andor_dll.Initialize(aBuffer)
	check_success(error_value, "Initialize")


	# Determine size (in pixels of camera)
	gblXPixels = ctypes.c_int()		# Total number of horizontal pixels
	gblYPixels = ctypes.c_int()		# Total number of vertical pixels

	error_value = andor_dll.GetDetector(ctypes.byref(gblXPixels),ctypes.byref(gblYPixels))
	check_success(error_value,"GetDetector")


	# Set vertical shift speed to recommended value
	vertical_shift_index = ctypes.c_int()	# the index to access specific vertical shift speeds 
	vertical_speed = ctypes.c_float()	# speed of the vertical speed shift in microseconds per pixel shift

	error_value = andor_dll.GetFastestRecommendedVSSpeed(ctypes.byref(vertical_shift_index),ctypes.byref(vertical_speed))
	check_success(error_value,"Get Fastest Recommended Vertical Shift Speed")
	error_value = andor_dll.SetVSSpeed(vertical_shift_index)
	check_success(error_value,"Set Vertical Shift Speed")


	# Set horizontal shift speed to the maximum
	horizontal_shift_index = ctypes.c_int(0)		# the index to access specific horizontal shift speeds
	AD_converter_index = ctypes.c_int()				# the specific index to access a given A-D converter
	number_AD = ctypes.c_int(0)						# the number of A-D converters in the camera
	number_speeds = ctypes.c_int()					# number of speeds available
	horizontal_speed = ctypes.c_float()				# horizontal shift speed
	max_horizontal_speed = ctypes.c_float(0)		# maximum horizontal speed

	error_value = andor_dll.GetNumberADChannels(ctypes.byref(number_AD))
	check_success(error_value,"Get Number AD Channels")

	for each_AD in range(number_AD.value):
		error_value = andor_dll.GetNumberHSSpeeds(AD_converter_index, ctypes.c_int(0), ctypes.byref(number_speeds))
		check_success(error_value, "Get Number Horizontal Shift Speeds")
		for each_speed_index in range(number_speeds.value):
			error_value = andor_dll.GetHSSpeed(ctypes.c_int(each_AD),ctypes.c_int(0),ctypes.c_int(each_speed_index),ctypes.byref(horizontal_speed))
			check_success(error_value,"Get Horizontal Shift Speed")
			if (horizontal_speed.value > max_horizontal_speed.value):
				max_horizontal_speed.value = horizontal_speed.value
				horizontal_shift_index = ctypes.c_int(each_speed_index)
				AD_converter_index = ctypes.c_int(each_AD)
	
	error_value = andor_dll.SetADChannel(AD_converter_index)
	check_success(error_value,"Set AD Channel")

	error_value = andor_dll.SetHSSpeed(ctypes.c_int(0), horizontal_shift_index)
	check_success(error_value, "Set Horizontal Speed Index")

	# Turn the camera cooler on
	error_value = andor_dll.CoolerON()
	check_success(error_value,"Turn Cooler On")


	# Check to make sure cooler is on
	cooler_on = ctypes.c_int()

	error_value = andor_dll.IsCoolerOn(ctypes.byref(cooler_on))
	check_success(error_value, "Check if cooler is on")
	if (cooler_on.value != 1):
		print("Error: Cooler not on", "Exiting...")
		return False	#TODO: exit code or somethings


	# Set the readout mode of the camera 
	read_mode = ctypes.c_int(read_mode_top)		# readout mode options: 0 Full Vertical binning;	1 Multi-Track;	2 Random-Track;	 3 Single-Track;	4 Image;
	error_value = andor_dll.SetReadMode(read_mode)
	check_success(error_value,"Set Read Mode")


	# Set the acquisition mode
	acquisition_mode = ctypes.c_int(1)		# acquisition mode options: 1 Single scan;	2 Accumulate;	3 Kinetics;	 4 Fast Kinetics;	5 Run till abort;
	error_value = andor_dll.SetAcquisitionMode(acquisition_mode)
	check_success(error_value,"Set Acquisition Mode")


	# Set exposure time
	exposure_time = ctypes.c_float(0.1)		# time in seconds
	error_value = andor_dll.SetExposureTime(exposure_time)
	check_success(error_value, "Set Exposure Time")

	
	# Set trigger mode
	trigger_mode = ctypes.c_int(0)	# trigger mode options:	0 internal;	1 external;	6 external start;	7 external exposure (bulb);	9 external FVB EM;	10 software trigger;	12 external charge shifting;
	error_value = andor_dll.SetTriggerMode(trigger_mode)
	check_success(error_value, "Set Trigger Mode")

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

	error_value = andor_dll.GetAcquisitionTimings(ctypes.byref(actual_exposure_time),ctypes.byref(actual_accumulate_time),ctypes.byref(actual_kinetic_time))
	check_success(error_value, "Get Acquisition Timings")

	
	# Wait for two seconds to allow the camera to calibrate fully before starting acquisition
	time.sleep(2)	

	
	# Make sure the camera is in an idle state before starting an acquisition
	camera_status = ctypes.c_int()

	error_value = andor_dll.GetStatus(ctypes.byref(camera_status))
	check_success(error_value, "Get Camera Status")
	while (camera_status.value != 20073):	
		error_value = andor_dll.GetStatus(ctypes.byref(camera_status))
		check_success(error_value, "Get Camera Status")
		#print("Camera Status is ", camera_status.value)


	# Set the horizontal and vertical binning and the area of the image to be captured
	horizontal_binning = ctypes.c_int(1)		# Number of pixels to bin horizontally
	vertical_binning = ctypes.c_int(1)			# Number of pixels to bin vertically
	horizontal_start = ctypes.c_int(1)			# Start column of image to be taken (inclusive)
	horizontal_end = gblXPixels					# End column of image to be taken (inclusive)
	vertical_start = ctypes.c_int(1)			# Start row of image to be taken (inclusive)
	vertical_end = gblYPixels					# End row of image to be taken (inclusive)

	error_value = andor_dll.SetImage(horizontal_binning, vertical_binning, horizontal_start, horizontal_end, vertical_start, vertical_end);
	check_success(error_value, "Set Image")


	# Start the acquisition process 
	error_value = andor_dll.StartAcquisition()
	acquiring = check_success(error_value, "Start Acquisition")
	if (acquiring == False):
		andor_dll.AbortAcquisition()
	else:
		print("Starting Acquisition")


		# Wait until the acquisition is complete
		error_value = andor_dll.GetStatus(ctypes.byref(camera_status))
		check_success(error_value, "Get Camera Status")
		while (camera_status.value != 20073): 
			error_value = andor_dll.GetStatus(ctypes.byref(camera_status))
			check_success(error_value, "Get Camera Status")
			#print("Camera Status is ", camera_status.value)

		# Get the image data from the camera
		size = ctypes.c_int(gblXPixels.value*gblYPixels.value)
		image_pointer = ctypes.cast(ctypes.create_string_buffer( size.value*ctypes.sizeof(ctypes.c_long()) ),ctypes.POINTER(ctypes.c_long))

		error_value = andor_dll.GetAcquiredData(image_pointer, size)
		check_success(error_value, "Get Acquired Data")


		# Transfer the image from a pointer to a numpy array
		image = np.zeros((gblYPixels.value,gblXPixels.value))
		for x in range(gblXPixels.value):
			for y in range(gblYPixels.value):
				image[y,x] = image_pointer[x + y*gblXPixels.value]

		plt.imsave('filename.png', image, cmap=cm.gray)

	# Shut down camera
	error_value = andor_dll.ShutDown()
	check_success(error_value, "Shut down")
	
	
if __name__ == "__main__":
	main()
