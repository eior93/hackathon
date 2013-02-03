import numpy as np
import cv2
import cv

f = 'flash_images/res_crop2.jpg'

if f == None:
	exit(1)

img = cv2.imread(f)
gray = cv2.imread(f,0)

#ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
thresh = cv2.Canny(gray, 30, 75)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

colors = [(255,0,0), 
(0, 255, 0), 
(0, 0, 255),
(255, 255, 0),
(0, 255, 255),
(255, 0, 255)]

# Find the longest contour

longest = []
for cnt in contours:
	if len(cnt) > len(longest):
		longest = cnt

# Draw the longest contour on the image
#cv2.drawContours(img, [longest], 0, colors[0], 3)


for index, cnt in enumerate(contours):
    approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt,True), True)
    #print 'len(approx):', len(approx)


    #cv2.drawContours(img, [cnt], 0, colors[index % 6], 3)

    cv2.drawContours(img, [approx], 0, colors[index % 6], 5)


# Creat the window
#cv.NamedWindow('img', cv.CV_WINDOW_AUTOSIZE)


cv2.imshow('img',img)
#cv2.imshow('gray', gray)
cv2.imshow('thresh', thresh)


cv2.waitKey(0)
cv2.destroyAllWindows()