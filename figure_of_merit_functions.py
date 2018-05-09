'''
Created on Wed March 28 2018

@author Yong Ma, yongm@umich.edu
'''

from pyicic.IC_ImagingControl import *
import numpy as np 
import matplotlib.pyplot as plt
import copy

def rgb2gray(rgb):
	'''Convert the 3-channel rgb image into grayscale
	'''
	r, g, b = rgb[:,:,0] , rgb[:,:,1] , rgb[:,:,2]
	gray  = 0.2989 * r + 0.587 * g + 0.114 * b
	return gray


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

	imgray = rgb2gray(frameout) # convert rgb image into grayscale

	
	satu = imgray[imgray>254].shape[0]
	if satu > 0:
		print('Image saturated with %d pixels'%satu)
		return 0
	else:
		
		# FOM1
		# I = abs(imgray)**2
		# x = np.arange(imgray.shape[1]).astype(float)
		# y = np.arange(imgray.shape[0]).astype(float)
		# mu0 = np.trapz(np.trapz(I, x ),y)
		# mean_x = np.trapz(np.trapz(I * x, x), y)/mu0
		# mean_y = np.trapz(np.trapz(I, x)*y, y)/mu0
		# r0 = 50
		# X, Y= np.meshgrid(x,y)
		# r = (Y - mean_y)**2 + (X - mean_x)**2
		# fom = (1-np.sum(imgray[r>=r0**2]) / np.sum(imgray) ) * np.sum(imgray[r<r0**2])
		# y_peak, x_peak = np.unravel_index(imgray.argmax(), imgray.shape) # find the target position for FOM calculation, here the maximum point is the target position
	

		#FOM2 (Image Moment)
		# x_peak = 520
		# y_peak = 554
		# xx = np.arange(imgray.shape[1]).astype(float)
		# yy = np.arange(imgray.shape[0]).astype(float)
		# X, Y= np.meshgrid(xx,yy)
		# d1 = (Y - y_peak)**2
		# d2 = (X - x_peak)**2
		# d = (d1+d2)**4
		# d[y_peak,x_peak]=1
		# fom = imgray / d
		# fom[y_peak,x_peak]=0
		# fom = np.sum(fom)

		#FOM3
		# fom = np.sum(imgray**2);

		#FOM4
		fom = np.sum(imgray);

		print(frameout.max(), fom)
		return fom

	# return frameout.max()



