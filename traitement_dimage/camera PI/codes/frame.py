from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import math
import sys





def find_angle(img):
    greenLower = (55, 85, 10)
    greenUpper = (149, 245, 255)
    frame = cv2.imread(img)
    print(frame.shape)
    #frame = imutils.resize(frame, width=600)
    print(frame.shape)
    width=frame.shape[1]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # construct a mask for the color "green", then perform
      # a series of dilations and erosions to remove any small
      # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
      # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

      # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        x,y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        center = (x,y)
        # only proceed if the radius meets a minimum size
        if radius > 5:
          # draw the circle and centroid on the frame,
          # then update the list of tracked points
          cv2.circle(frame, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
          cv2.circle(frame, center, 5, (0, 0, 255), -1)

      # update the points queue
        print x
        if ("Bas_Gauche" in img or "Haut_Droite" in img):
            angle = -((width-x)/(width/55.0)+17)
        else:
            angle = x/(width/55.0)+17
        #angle = float(math.atan(float((1)))*180/math.pi)
        print(angle)
        return angle

def find_coord(a1,xc1,yc1,a2,xc2,yc2):
    a1=a1*math.pi/180
    a2=a2*math.pi/180
    x= (yc1 - math.tan(a1)*xc1 - (yc2 - math.tan(a2)*xc2))/(math.tan(a2)-math.tan(a1))
    y= math.tan(a1)*(x-xc1)+yc1
    return x,y

  #angle = int(math.atan((y1-y2)/(x2-x1))*180/math.pi)
  #cv.PutText(img,str(angle),(int(x1)+50,(int(y2)+int(y1))/2),font,255)

#cv2.line(frame,(720,1280), center, (255,0,0), 2)
#cv2.line(frame,(600,700), center, (255,0,0), 2)
  # loop over the set of tracked points
#cv2.imshow("Frame", frame)
#key = cv2.waitKey(60) & 0xFF

  # if the 'q' key is pressed, stop the loop


# cleanup the camera and close any open windows
#cv2.waitKey(0)
#cv2.destroyAllWindows()
if __name__ == '__main__':

    img = sys.argv[1]
    img2 = sys.argv[2]
    a1 = find_angle(img)
    a2 = find_angle(img2)
    print a1, a2
    x,y = find_coord(a1, 0, 1080, a2+4, 1920,1080)
    print x,y
    x,y = find_coord(-30 , 0, 1080, 60, 1920,1080)
    print x,y
