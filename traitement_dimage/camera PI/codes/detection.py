
from __future__ import print_function

import numpy as np
from numpy import pi, sin, cos
from matplotlib import pyplot as plt
import cv2

# built-in modules
from time import clock

# local modules
import common
def draw_hand_rect(frame):  
    print(frame.shape)
    rows,cols,_= frame.shape

    #hand_row_nw = np.array([6*rows/20,6*rows/20,6*rows/20,10*rows/20,10*rows/20,10*rows/20,14*rows/20,14*rows/20,14*rows/20])

    #hand_col_nw = np.array([9*cols/20,10*cols/20,11*cols/20,9*cols/20,10*cols/20,11*cols/20,9*cols/20,10*cols/20,11*cols/20])
    hand_row_nw = np.array([6*rows/40,6*rows/40,110,110,6*rows/40,130,140,150])

    hand_col_nw = np.array([710,720,720,710,730,730,730,730])
    #hand_row_nw = np.array([700,700,700])
    #hand_col_nw = np.array([1000,1050,1100])
    hand_row_se = hand_row_nw + 10
    hand_col_se = hand_col_nw + 10
    print("hand_row_nw"  ,hand_row_nw)
    print("hand_col_nw"  ,hand_col_nw)
    print("hand_row_se" , hand_row_se)
    print("hand_col_se", hand_col_se)
    
    size = hand_row_nw.size
    print(size)
    for i in xrange(size):
    	cv2.rectangle(frame,(hand_col_nw[i],hand_row_nw[i]),(hand_col_se[i],hand_row_se[i]),(0,255,0),1)
        #black = np.zeros(frame.shape, dtype=frame.dtype)
        #print (frame.dtype)
        #frame_final = np.vstack([black, frame])
    return frame,hand_row_nw,hand_col_nw

def set_hand_hist(frame):  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90,10,3], dtype=hsv.dtype)
    _,hand_row_nw,hand_col_nw = draw_hand_rect(frame)
     
    size = hand_row_nw.size
    for i in xrange(size):
        roi[i*10:i*10+10,0:10] = hsv[hand_row_nw[i]:hand_row_nw[i]+10, hand_col_nw[i]:hand_col_nw[i]+10]

    hand_hist = cv2.calcHist([roi],[0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)
    plt.imshow(hand_hist,interpolation = 'nearest')
    plt.show()
    return hand_hist

def apply_hist_mask(frame, hist):  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0,1], hist, [0,180,0,256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 100, 255, 0)
    thresh = cv2.merge((thresh,thresh, thresh))

    cv2.GaussianBlur(dst, (3,3), 0, dst)

    res = cv2.bitwise_and(frame, thresh)
    return res

def draw_contours(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray, 0, 255, 0)
	print(thresh)
	_,contours, hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)	
	print(contours)
	return contours

def draw_max_contour(contours):
	max_i = 0
	max_area = 0
	
	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_area = area
			max_i = i

	contour = contours[max_i]
	return contour
def draw_centroid(contour):
	moments = cv2.moments(contour)
	if moments['m00'] != 0:
		cx = int(moments['m10']/moments['m00'])
		cy = int(moments['m01']/moments['m00'])
		return (cx,cy)
	else:
		return None	
def draw_defects(contour):
	hull = cv2.convexHull(contour, returnPoints=False)
	if hull is not None and len(hull > 3) and len(contour) > 3:
		defects = cv2.convexityDefects(contour, hull)	
		return defects
	else: 
		return None
def draw_farthest_point(defects, contour, centroid):
	s = defects[:,0][:,0]
	cx, cy = centroid
	
	x = np.array(contour[s][:,0][:,0], dtype=np.float)
	y = np.array(contour[s][:,0][:,1], dtype=np.float)
				
	xp = cv2.pow(cv2.subtract(x, cx), 2)
	yp = cv2.pow(cv2.subtract(y, cy), 2)
	dist = cv2.sqrt(cv2.add(xp, yp))

	dist_max_i = np.argmax(dist)

	if dist_max_i < len(s):
		farthest_defect = s[dist_max_i]
		farthest_point = tuple(contour[farthest_defect][0])
		return farthest_point
	else:
		return None	

def draw_hull(contour):
	hull = cv2.convexHull(contour)
	return hull
def draw_final(frame, hist):  
    hand_masked = apply_hist_mask(frame, hist)

    contours= draw_contours(hand_masked)
    if contours is not None and len(contours) > 0:
        max_contour = draw_max_contour(contours)
        hull = draw_hull(max_contour)
        centroid = draw_centroid(max_contour)
        defects = draw_defects(max_contour)

        if centroid is not None and defects is not None and len(defects) > 0:   
            farthest_point = draw_farthest_point(defects, max_contour, centroid)

            if farthest_point is not None:
                plot_farthest_point(frame, farthest_point)
                plot_centroid(frame,centroid)
def plot_farthest_point(frame, point):
		cv2.circle(frame, point, 5, [0,0,255], -1)
def plot_centroid(frame, point):
		cv2.circle(frame, point, 5, [255,0,0], -1)

if __name__ == '__main__':
    import sys
    import getopt
    import numpy as np
	

frame = sys.argv[1]
base = sys.argv[2]
print (frame)
img = cv2.imread(frame)
base = cv2.imread(sys.argv[2])
img,_,_ = draw_hand_rect(base)
hist=set_hand_hist(img)
res=apply_hist_mask(img,hist)
cv2.imshow('image',res)
cv2.imshow('image',img)
draw_final(res,hist)
cv2.imshow('image',res)
cv2.waitKey(0)
cv2.destroyAllWindows()

