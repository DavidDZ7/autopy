"""
Script to test the raspberry camera for taking pictures
"""
from picamera import PiCamera
import time


try:
	camera=PiCamera()
	#camera.resolution=(640,480)
	camera.vflip = True
	
	camera.start_preview()
	time.sleep(4)#wait n seconds
	camera.capture("test.jpg")

finally:
	camera.stop_preview()
	camera.close()
