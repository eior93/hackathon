#!/usr/bin/env python2.7

from colors import color_names, colors
import cv
import math
import os
import fnmatch

from color_classification import distance, min_distance_index, avg_img_color, min_index

# Get average color sample values for knowing RGB values for colors
color_sample_dir = "color_samples"
os.chdir(color_sample_dir)

for color_i in range(0, len(color_names)):
	this_sample_filenames = fnmatch.filter(os.listdir('.'), color_names[color_i]+'*.jpg');
	num_samples = len(this_sample_filenames)
	color_tuples = []
	for sample_i in range(0, num_samples):
		color_tuples.append(
				avg_img_color(cv.LoadImage(this_sample_filenames[sample_i])))
	avg_r = sum([color[0] for color	in color_tuples]) / num_samples
	avg_g = sum([color[1] for color	in color_tuples]) / num_samples
	avg_b = sum([color[2] for color	in color_tuples]) / num_samples
	colors[color_i] = (avg_r, avg_g, avg_b)

for color_i in range(0, len(color_names)):
	print color_names[color_i].upper() + "\t=\t" + str(colors[color_i])

os.chdir("..")
