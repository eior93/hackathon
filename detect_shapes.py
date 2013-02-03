import numpy as np
import cv2
import Image, cv
import matplotlib.pyplot as plt
from smooth import smooth
import math
from color_classification import avg_img_color_np, min_distance_index
from colors import color_names

def x_var_filter(l):
	ans = np.std(l, 0)
	x, y = ans[0]
	if x * 1.9 > y:
		return False
	else:
		return True

# sum threshold in y directions to find peaks
def sum_y_and_thresh(thresh):
	thresh_y = []
	thresh_y_bin = []
	for c in range(0, img_width):
		sum_col = 0
		for r in range(0, img_height):
			# print str(r) + " " + str(c)
			sum_col += thresh[r, c]
		thresh_y.append(sum_col)
		if sum_col > 4000:
			thresh_y_bin.append(1)
		else:
			thresh_y_bin.append(0)
	return thresh_y_bin


# increase above 5000 -> walk until below 5000, use middle as cut point
def cuts_cross_threshold(thresh_y_bin, img_width):
	x_cuts = []
	start_x = 0
	tracing_ones = (thresh_y_bin[0] == 1) 
	for c in range(1, img_width):
		# if tracing_ones and thresh_y_bin[c] == 1:
			# do nothing
		if tracing_ones and thresh_y_bin[c] == 0:
			x_cuts.append(start_x) #math.floor((start_x + c)/2))
			x_cuts.append(c)
			start_x = c + 1
			tracing_ones = False 
		elif not(tracing_ones) and thresh_y_bin[c] == 1:
			tracing_ones = True;
			start_x = c
		# not tracing ones and found a 0
		elif not(tracing_ones) and thresh_y_bin[c] == 0: 
			start_x = c
	return x_cuts

# First pass band ids
def band_ids_first_pass(x_cuts, img_height, img):
	band_ids = {}
	
	top_row = 0
	bottom_row = img_height - 1
	num_vert_sections = 15

	for i in range(0, len(x_cuts) - 1):
		start_x = x_cuts[i]
		end_x = x_cuts[i+1]
		cropped_im = np.array(img[top_row:bottom_row])
		cropped_im = np.array([col[start_x:end_x] for col in cropped_im])

		avg_color = avg_img_color_np(cropped_im)

		min_dist_i = min_distance_index(avg_color)
		band_ids[i] = (min_dist_i, start_x, end_x) #.put(i, (min_dist_i, start_x, end_x))
		# print "Start_x:" + str(start_x) + "\t End_x:"+str(end_x)+ "\t" + color_names[min_dist_i]
	return band_ids

# Second pass band ids
def band_ids_second_pass(band_ids, img_height):
	x_cuts_2 = []
	top_row = 0
	bottom_row = img_height - 1
	BGD = 10
	# Find cuts for from bgd to nbgd and nbgd to bgd
	for i in range(0, len(band_ids.keys()) - 1):
			if band_ids[i][0] == BGD and band_ids[i+1][0] != BGD:
				x_cuts_2.append(band_ids[i][2])
			elif band_ids[i][0] != BGD and band_ids[i+1][0] == BGD:
				x_cuts_2.append(band_ids[i+1][1])	

	band_ids_2 = {}

	for i in range(0, len(x_cuts_2) - 1):
		start_x = x_cuts_2[i]
		end_x = x_cuts_2[i+1]
		cropped_im = np.array(img[top_row:bottom_row])
		cropped_im = np.array([col[start_x:end_x] for col in cropped_im])

		avg_color = avg_img_color_np(cropped_im)

		min_dist_i = min_distance_index(avg_color)
		band_ids_2[i] = (min_dist_i, start_x, end_x) #.put(i, (min_dist_i, start_x, end_x))
		# band_ids.append(min_dist_i)
		print "Start_x:" + str(start_x) + "\t End_x:"+str(end_x)+ "\t" + color_names[min_dist_i]
	return band_ids_2


f = 'test_res/resr4.jpg'

# Read in image
img = cv2.imread(f)

# Sharpen the image (unsharpen mask)
blur = cv2.blur(img, (7,1))
cv2.addWeighted(img, 1.5, blur, -0.5, 0, blur)

# Convert to grayscale
gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

img_width = len(img[0])
img_height = len(img)

thresh = cv2.Canny(gray, 30, 75)
thresh_y_bin = sum_y_and_thresh(thresh)
x_cuts = cuts_cross_threshold(thresh_y_bin, img_width)

band_ids = band_ids_first_pass(x_cuts, img_height, img)

band_ids_2 = band_ids_second_pass(band_ids, img_height)
 
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 
# 
# colors = [(255,0,0), 
# (0, 255, 0), 
# (0, 0, 255),
# (255, 255, 0),
# (0, 255, 255),
# (255, 0, 255)]
# 
# """
# # Find the longest contour
# 
# longest = []
# for cnt in contours:
# 	if len(cnt) > len(longest):
# 		longest = cnt
# 
# # Draw the longest contour on the image
# #cv2.drawContours(img, [longest], 0, colors[0], 3)
# """
# 
# # Only allow contours greater than 25
# contours = filter(lambda x: len(x) > 25, contours)
# 
# # Remove contours with greater x variance
# contours = filter(x_var_filter, contours)
# 
# x_means = []
# 
# 
# x_mean_thresh = img_width * 0.03
# # Pair all of the x means for each contour with the contour
# # Filter out contours that are too close
# for new_cnt in contours:
# 	new_mean = np.mean(new_cnt, 0)[0][0]
# 
# 	flagged = False
# 	for x_mean, cnt  in x_means:
# 		if abs(x_mean - new_mean) < x_mean_thresh:
# 			flagged = True
# 
# 	if not flagged:
# 		x_means += [(new_mean, new_cnt)]
# 
# filtered_contours = [ cnt for mean, cnt in x_means]
# 
# 
# for index, cnt in enumerate(filtered_contours):
# 	# Approximate each contour
#     approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt,True), True)
#     #print 'len(approx):', len(approx)
# 
#     #cv2.drawContours(img, [cnt], 0, colors[index % 6], 3)
# 
#     cv2.drawContours(img, [approx], 0, colors[index % 6], 5)
# 
# 
# cv2.imshow('img',img)
#cv2.imshow('gray', gray)


# cv2.waitKey(0)
# cv2.destroyAllWindows()
