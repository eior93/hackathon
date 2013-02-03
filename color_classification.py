#!/usr/bin/env python2.7

from colors import color_names, colors
import cv
import math
import os
import fnmatch
import numpy as np

# Distance formula between two colors
def distance(a, b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

# Minimum distance between a tuple for a color and color classifications
def min_distance_index(color_in):
	distances = [];
	for i in range(0, len(colors)-1):
		distances.append(distance(color_in, colors[i]))
	return min_index(distances)

def min_index(arr):
	index = 0
	min_val = arr[0]
	for i in range(1, len(arr)):
		if arr[i] < min_val:
			index = i
			min_val = arr[i]
	return index

def avg_img_color(img_in):
	sum_r = 0
	sum_g = 0
	sum_b = 0
	r_values = []
	g_values = []
	b_values = []
	img_mat = cv.GetMat(img_in)
	for r in range(0, img_mat.rows):
		for c in range(0, img_mat.cols):
			 sum_r += img_mat[r, c][2]
			 sum_g += img_mat[r, c][1]
			 sum_b += img_mat[r, c][0]
			 r_values.append(img_mat[r, c][2])
			 g_values.append(img_mat[r, c][1])
			 b_values.append(img_mat[r, c][0])
	
	num_pix = img_in.width * img_in.height

	return (np.median(r_values), np.median(g_values), np.median(b_values))
