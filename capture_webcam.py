#!/usr/bin/env python2.7
import cv
import time

print "hello world"

cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)

camera_index = 0
capture = cv.CaptureFromCAM(0) #camera_index)

for i in range(0, 10):
	frame = cv.QueryFrame(capture)
	cv.SaveImage("pic" + str(i)+ ".jpg", frame)
	time.sleep(1)
