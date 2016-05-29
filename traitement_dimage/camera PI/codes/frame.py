from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import math
import sys

from Mouvement import Mouvements



def find_angle_from_frame(frame, name):
    if frame is None:
        return
    greenLower = (55, 85, 10)
    greenUpper = (149, 245, 255)
    
    #frame = imutils.resize(frame, width=600)
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
        
        # instantaneous velocity calculation
        
        # only proceed if the radius meets a minimum size
        if radius > 5:
          # draw the circle and centroid on the frame,
          # then update the list of tracked points
          cv2.circle(frame, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
          cv2.circle(frame, center, 5, (0, 0, 255), -1)

      # update the points queue
        if ("Bas_Gauche" in name or "Haut_Droite" in name):
            angle = -((width-x)/(width/55.0)+17)
        else:
            angle = x/(width/55.0)+17
        #angle = float(math.atan(float((1)))*180/math.pi)
        
        return angle
    
def check_touch(x,y,data):
    if(x!=0 and y!=0):
    # Distance calculation
        if(len(data)==0):
            data=[0,0,0]
        dist = math.sqrt((math.pow((x-data[0]),2))+(math.pow((y-data[1]),2)))
        #instantaneous velocity calculation pixel/seconde
        vit = (dist/(time.clock()-data[2]))
        #print time.clock()-data[2]
        data = [x,y,time.clock()]
        #threshold to be adjusted !!!!! 
        if (vit<500):
            return True,data
        else: 
            return False,data    
    else: return False,data
def find_angle(img):
    greenLower = (55, 85, 10)
    greenUpper = (149, 245, 255)
    frame = cv2.imread(img)
    #frame = imutils.resize(frame, width=600)
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
        if ("Bas_Gauche" in img or "Haut_Droite" in img):
            angle = -((width-x)/(width/55.0)+17)
        else:
            angle = x/(width/55.0)+17
        #angle = float(math.atan(float((1)))*180/math.pi)
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

    vid1 = sys.argv[1]
    vid2 = sys.argv[2]
    cam1 = cv2.VideoCapture(vid1)
    cam2 = cv2.VideoCapture(vid2)
    #i=0
    #while (i<1*12):
    #    (grabbed1, frame1) = cam1.read()
    #    i=i+1
    #data record ansx, ansy, anstime
    data = []
    tab=[]
    while True:

        (grabbed1, frame1) = cam1.read()
        (grabbed1, frame2) = cam2.read()
        
        a1 = find_angle_from_frame(frame1, vid1)
        a2 = find_angle_from_frame(frame2, vid2)
        
        if(frame1 is not None):
            cv2.imshow("Frame1", frame1)
        if (frame2 is not None):
            cv2.imshow("Frame2", frame2)
        if (not (a1 is None or a2 is None)):
            print a1, a2
            x,y = find_coord(a1, 0, 1080, a2, 1920,1080)
            tab.append((x,y))
            print tab
        #   touch,data=check_touch(x,y,data)
        #   print(touch)
        
            #print x,y

        key = cv2.waitKey(60) & 0xFF
        if key == ord("q"):
            print tab
            supertab=[]
            supertab.append(tab)
            Mouv=Mouvements(supertab)
            Mouv.save_to_svg("bidule.svg")
            Mouvements.read_from_file("mouv_droite").save_to_svg("mouv_droite.svg")
            print(Mouv.look_like(Mouvements.read_from_file("mouv_droite")))
            break


    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()
