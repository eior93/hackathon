import numpy as np
import cv2

def crop_image(image_name):

    im = cv2.imread(image_name+'.jpg')
    print type(im)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    #print np.median(imgray)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    variances = []
    long_contours = []

    for cnt in contours:
        if len(cnt)>100:
            long_contours.append(cnt)
            
            #print cnt
            cv2.drawContours(im, [cnt], -1, (255,255,255),-1)
    cv2.drawContours(im, [cnt], -1, (255,255,255),-1)
  

    #cv2.drawContours(im, [long_contours[index]], -1, (255,255,255),3)

    cv2.imwrite(image_name+'G.jpg', im)

    row_vars = []
    for i in range(len(im)):
        row_vars.append(np.var(im[i]))
    #print row_vars
    #print np.median(row_vars)

    top_row = -1
    threshold = 2*np.median(row_vars)
    # assume that top of resistor is at least 10 pixels in
    for i in range(10, len(im)):
        # if row variance is high enough, remember
        if row_vars[i] > threshold:
            top_row = i
            break
    bottom_row = -1
    # same assumption here with bottom
    for i in reversed(range(1, len(im)-10)):
        if row_vars[i] > threshold:
            bottom_row = i
            break

    #print top_row
    #print bottom_row
    cropped_im = np.array(im[top_row:bottom_row])

    #column means
    col_means = []
    for i in range(10,len(im[0])-10):
        col_means.append(np.mean([col[i] for col in cropped_im]))
    #print np.median(col_means)
    #print np.var(col_means)
    #print np.mean(col_means)
    minMean =  np.min(col_means)
    maxMean =  np.max(col_means)
    col_threshold = (minMean + maxMean)/2
    #print col_means
    #print col_threshold

    left_col = -1
    right_col = -1
    for i in range(len(col_means)):
        if col_means[i]<col_threshold:
            left_col = i + 10
            break
    for i in reversed(range(len(col_means))):
        if col_means[i]<col_threshold:
            right_col = i - 10
            break
    #print left_col
    #print right_col

    cropped_im = np.array([col[left_col:right_col] for col in cropped_im])



    # crop by row again except by median
    row_medians = []
    for i in range(len(cropped_im)):
        row_medians.append(np.median(cropped_im[i]))

    top_row = -1
    threshold = 250
    # assume that top of resistor is at least 10 pixels in
    for i in range(0, len(cropped_im)):
        # if row variance is high enough, remember
        if row_medians[i] < threshold:
            top_row = i
            break
    bottom_row = -1
    # same assumption here with bottom
    for i in reversed(range(len(cropped_im))):
        if row_medians[i] < threshold:
            bottom_row = i
            break

    #print top_row
    #print bottom_row
    cropped_im = np.array(cropped_im[top_row:bottom_row])

    cv2.imwrite(image_name+'_cropped.jpg', cropped_im)


#image_names = ['IMAG1024', 'IMAG1025', 'IMAG1026', 'IMAG1027', 'IMAG1028', 'IMAG1029', 'IMAG1030']
#for im in image_names:
#    crop_image(im)
#image_name = "IMAG1028"
#crop_image(image_name)

#[col[top_row:bottom_row] for col in im]
    


##def testContours():
##
##    
##    image_name = 'IMAG1030'
##    im = cv2.imread(image_name+'.jpg')
##    print type(im)
##    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##    ret,thresh = cv2.threshold(imgray,127,255,0)
##    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##
##    variances = []
##    long_contours = []
##
##
##    #cv2.drawContours(im,contours,-1,(0,255,0),3)
##
##
##    for cnt in contours:
##        if len(cnt)>100:
##            #print cnt
##            long_contours.append(cnt)
##            variances.append(np.var([pt[0][1] for pt in cnt]))
##            
##            #print cnt
##            cv2.drawContours(im, [cnt], -1, (255,255,255),-1)
##
##    return im
##
##cv2.imwrite(image_name+'G.jpg', im)

