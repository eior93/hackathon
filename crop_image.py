import numpy as np
import cv2
import math
#import matplotlib.pyplot as plt

def crop_image_2(image_name):
        imgray = cv2.imread(image_name+'.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        im = cv2.imread(image_name+'.jpg')
        
        img_width = len(imgray[0])
        img_height = len(imgray)

        sum_y = []
        sum_x = []

        # Summing across rows
        for r in range(0, img_height):
                sum_row = 0
                for c in range(0, img_width):
                        sum_row += imgray[r, c]
                sum_x.append(sum_row)

        # Find min energy across rows
        min_x = min(sum_x)
        min_x_index = sum_x.index(min_x)
        min_row = max(min_x_index - 50, 0) #100 #50 #15
        max_row = min(min_x_index + 50, img_height) #100 #50 #15
        cropped_im = np.array(im[min_row:max_row])
        
        # Summing across columns
        for c in range(0, img_width):
                sum_col = 0
                for r in range(min_row, max_row):
                        sum_col += imgray[r, c]
                sum_y.append(sum_col)
        
        min_col = min(sum_y)
        min_y_index = sum_y.index(min_col)
        min_col = min_y_index - 120 # 200 #100 # 30
        max_col = min_y_index + 120 # 200 #100 # 30 
        cropped_im = np.array([col[min_col:max_col] for col in cropped_im])
        
        cv2.imwrite(image_name+'_cropped.jpg', cropped_im)

def crop_image(image_name):
        im = cv2.imread(image_name+'.jpg')
        offset = 400
         # top_row = offset
        im_height = len(im)
        im_width = len(im[0])
         # bottom_row = im_height - offset # math.floor(im_height - offset/2)
        start_col = offset
        end_col = im_width - offset
 
         # im = np.array(im[top_row:bottom_row])
        im = np.array([col[start_col:end_col] for col in im])
   
        print "before: " + str(im_height) + " after: " + str(len(im))
        print "after: " + str(im_width) + " after: " + str(len(im[0]))

        imgray = cv2.imread(image_name+'.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        imgray = np.array([col[start_col:end_col] for col in imgray])

        cv2.imwrite(image_name + "gray.jpg", imgray)

        # imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
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
        row_offset = 200
        threshold = 2*np.median(row_vars)
        # assume that top of resistor is at least 10 pixels in
        for i in range(row_offset, len(im)):
                # if row variance is high enough, remember
                if row_vars[i] > threshold:
                        top_row = i
                        break
        bottom_row = -1
        # same assumption here with bottom
        for i in reversed(range(1, len(im)-row_offset)):
                if row_vars[i] > threshold:
                        bottom_row = i
                        break

        #print top_row
        #print bottom_row
        cropped_im = np.array(im[top_row:bottom_row])

##        cropped_im_gray = cv2.cvtColor(cropped_im,cv2.COLOR_BGR2GRAY)
##        sum_y = []
##        # Summing across 
##        for c in range(len(cropped_im_gray[0])):
##                sum_col = 0
##                for r in range(len(cropped_im_gray)):
##                        sum_col += cropped_im_gray[r, c]
##                sum_y.append(sum_col)
##        
##        min_col = min(sum_y)
##        min_y_index = sum_y.index(min_col)
##        min_col = max(min_y_index - 120, 0) # 200 #100 # 30
##        max_col = min(min_y_index + 120, len(cropped_im)-1) # 200 #100 # 30
##
##        cv2.imwrite(image_name+'_cropped2.jpg', cropped_im_gray)
##        
##        cropped_im = np.array([col[min_col:max_col] for col in cropped_im])
##        print sum_y
##        print min_y_index


        col_offset = 100
        #column means
        col_means = []
        for i in range(col_offset,len(im[0])-col_offset):
                col_means.append(np.mean([col[i] for col in cropped_im]))
        #print np.median(col_means)
        #print np.var(col_means)
        #print np.mean(col_means)
        minMean =  np.min(col_means)
        maxMean =  np.max(col_means)
        #col_threshold = (minMean + maxMean)/2
        col_threshold = minMean + 3.56*np.std(col_means)

        print minMean
        print maxMean
        print np.std(col_means)
        #print col_means
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


##
##        # crop by row again except by median
##        row_medians = []
##        for i in range(len(cropped_im)):
##                row_medians.append(np.median(cropped_im[i]))
##
##        top_row = -1
##        threshold = 250
##        # assume that top of resistor is at least 10 pixels in
##        for i in range(0, len(cropped_im)):
##                # if row variance is high enough, remember
##                if row_medians[i] < threshold:
##                        top_row = i
##                        break
##        bottom_row = -1
##        # same assumption here with bottom
##        for i in reversed(range(len(cropped_im))):
##                if row_medians[i] < threshold:
##                        bottom_row = i
##                        break
##
##        #print top_row
##        #print bottom_row
##        cropped_im = np.array(cropped_im[top_row:bottom_row])

        cv2.imwrite(image_name+'_cropped.jpg', cropped_im)

crop_image('picture1')
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

