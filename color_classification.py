#!/usr/bin/env python2.7

import cv
import math

RED = (231, 47, 39);
ORANGE = (238, 113, 25);
YELLOW = (255, 228, 15);
GREEN = (23, 106, 43);
BLUE = (46, 20, 141);
PURPLE = (115, 71, 79);
BROWN = (88, 60, 50);
BLACK = (10, 10, 10);
WHITE = (244, 244, 244);

colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, BROWN, BLACK, WHITE];

color_names = ["red", "orange", "yellow", "green", "blue", "purple", 
	"brown", "black", "white"];

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
	for i in range(1, len(arr)-1):
		if arr[i] < min_val:
			index = i
			min_val = arr[i]
	return index

# Prototyping code below

def avg_img_color(img_in):
	sum_r = 0
	sum_g = 0
	sum_b = 0
	img_mat = cv.GetMat(img_in)
	for r in range(0, img_mat.rows-1):
		for c in range(0, img_mat.cols-1):
			 sum_r += img_mat[r, c][0]
			 sum_g += img_mat[r, c][1]
			 sum_b += img_mat[r, c][2]
	
	num_pix = img_in.width * img_in.height
	avg_r = sum_r / num_pix
	avg_g = sum_g / num_pix
	avg_b = sum_b / num_pix

	return (avg_r, avg_g, avg_b)


image_red = cv.LoadImage("red.jpg")
min_dist_index = min_distance_index(avg_img_color(image_red))
print color_names[min_dist_index]
