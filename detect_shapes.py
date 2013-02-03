import numpy as np
import cv2


def x_var_filter(l):
	ans = np.std(l, 0)
	x, y = ans[0]
	if x * 1.9 > y:
		return False
	else:
		return True


f = 'test_res/resr6.jpg'

# Read in image
img = cv2.imread(f)

# Sharpen the image (unsharpen mask)
blur = cv2.blur(img, (7,1))
cv2.addWeighted(img, 1.5, blur, -0.5, 0, blur)

# Convert to grayscale
gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)



print 'width:', len(img[0])
print 'height:', len(img)
img_width = len(img[0])
img_height = len(img)


#ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
thresh = cv2.Canny(gray, 30, 75)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


colors = [(255,0,0), 
(0, 255, 0), 
(0, 0, 255),
(255, 255, 0),
(0, 255, 255),
(255, 0, 255)]

"""
# Find the longest contour

longest = []
for cnt in contours:
	if len(cnt) > len(longest):
		longest = cnt

# Draw the longest contour on the image
#cv2.drawContours(img, [longest], 0, colors[0], 3)
"""

# Only allow contours greater than 25
contours = filter(lambda x: len(x) > 25, contours)

# Remove contours with greater x variance
contours = filter(x_var_filter, contours)

x_means = []


x_mean_thresh = img_width * 0.03
# Pair all of the x means for each contour with the contour
# Filter out contours that are too close
for new_cnt in contours:
	new_mean = np.mean(new_cnt, 0)[0][0]

	flagged = False
	for x_mean, cnt  in x_means:
		if abs(x_mean - new_mean) < x_mean_thresh:
			flagged = True

	if not flagged:
		x_means += [(new_mean, new_cnt)]

filtered_contours = [ cnt for mean, cnt in x_means]


for index, cnt in enumerate(filtered_contours):
	# Approximate each contour
    approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt,True), True)
    #print 'len(approx):', len(approx)

    #cv2.drawContours(img, [cnt], 0, colors[index % 6], 3)

    cv2.drawContours(img, [approx], 0, colors[index % 6], 5)


cv2.imshow('img',img)
#cv2.imshow('gray', gray)
cv2.imshow('thresh', thresh)


cv2.waitKey(0)
cv2.destroyAllWindows()
