#!/usr/bin/env python2.7

from colors import color_names
import cv
import cv2
import numpy as np
import math
from color_classification import avg_img_color_np, min_distance_index

img = cv.LoadImage("test_res/resr4.jpg")

top_row = 0
bottom_row = img.height - 1
num_vert_sections = 15
# x_cuts = [1.0, 7.0, 65.0, 69.0, 75.0, 90.0, 102.0, 105.0, 110.0, 119.0, 173.0, 193.0, 196.0, 203.0, 262.0, 266.0, 272.0, 282.0, 295.0, 417.0, 468.0, 495.0, 508.0]

# jeanette is being very silly... parentheses are important
# x_cuts = [3.0, 19.0, 22.0, 67.0, 89.0, 93.0, 103.0, 118.0, 149.0, 155.0, 169.0, 199.0, 253.0, 257.0, 262.0, 277.0, 306.0, 361.0, 364.0, 411.0, 420.0, 427.0, 442.0, 445.0]

#resr3
# x_cuts = [3.0, 12.0, 14.0, 46.0, 59.0, 61.0, 70.0, 78.0, 99.0, 103.0, 116.0, 134.0, 168.0, 171.0, 174.0, 188.0, 203.0, 240.0, 242.0, 274.0, 279.0, 284.0, 294.0, 296.0]

#resr4
x_cuts = [34.0, 42.0, 46.0, 49.0, 56.0, 61.0, 63.0, 71.0, 113.0, 147.0, 150.0, 160.0, 166.0, 169.0, 178.0, 188.0, 203.0, 238.0, 274.0, 297.0, 327.0]

print img.width

for i in range(0, len(x_cuts) - 1):
	start_x = x_cuts[i]
	end_x = x_cuts[i+1]
	# start_x = math.floor(i*img.width/num_vert_sections)
	# end_x = math.floor((i+1)*img.width/num_vert_sections)
	cropped_im = np.array(img[top_row:bottom_row])
	cropped_im = np.array([col[start_x:end_x] for col in cropped_im])

	avg_color = avg_img_color_np(cropped_im)

	min_dist_i = min_distance_index(avg_color)

	print "Start_x:" + str(start_x) + "\t End_x:"+str(end_x)+ "\t" + color_names[min_dist_i]
	# cv2.imwrite("cropped_"+str(i)+".jpg", cropped_im)
