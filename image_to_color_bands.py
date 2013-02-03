#!/usr/bin/env python2.7

from detect_shapes import cropped_img_to_colors
from crop_image import crop_image_2, crop_image

def image_to_color_bands(image_name):
	# crop image
	crop_image_2(image_name)	
	# cropped image name
	cropped_filename = image_name + "_cropped.jpg"
	# identify color bands
	color_ids = cropped_img_to_colors(cropped_filename)
	return color_ids

print image_to_color_bands("pic")

# print image_to_color_bands("cropped_images/IMAG1025")
# print image_to_color_bands("cropped_images/IMAG1026")
# print image_to_color_bands("cropped_images/IMAG1027")
# print image_to_color_bands("cropped_images/IMAG1028")
# print image_to_color_bands("cropped_images/IMAG1029")
# print image_to_color_bands("flash_images/IMAG1018")
# print image_to_color_bands("flash_images/IMAG1020")
# print image_to_color_bands("flash_images/IMAG1021")
