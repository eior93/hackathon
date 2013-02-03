#!/usr/bin/env python2.7

from colors import color_names, colors
from color_classification import min_distance_index, avg_img_color
import cv
import os
import fnmatch

# Check performance
# TODO less hacky way to move to correct directory
print os.listdir(".")
os.chdir("test_images")

for color_i in range(0, len(color_names)):
	this_sample_filenames = fnmatch.filter(os.listdir('.'), color_names[color_i]+'*.jpg');
	num_samples = len(this_sample_filenames)
	if num_samples > 0:
		print "Expected Color: " + color_names[color_i]
		print "Classified Color: "
		for sample_i in range(0, num_samples):
			test_image = cv.LoadImage(this_sample_filenames[sample_i])
			min_dist_index = min_distance_index(avg_img_color(test_image))
			print "\t" + color_names[min_dist_index]

