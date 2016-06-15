from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import math
import sys

from affichageDroite import Screen

import pyautogui

import gestionAction
from threading import Thread, RLock

from Mouvement import Mouvements

from get_frame_from_arduino import ArduinoCam

class gestionCamera(Thread):
    """docstring for """
    correctionAngle={"Bas_Gauche": 0, "Bas_Droite": 0, "Haut_Gauche": 0, "Haut_Droite": 0}
    correction=False
    def __init__(self, filename, ipCam=None, nbrCam=None,debug=None):
        Thread.__init__(self)
        self.affichageDroite=None
        self.cw=None
        if debug!=False:
            self.affichageDroite=Screen()
        self.stopped = False
        self.lock = RLock()
        self.edit_conf(filename)
        self.arduinoCam=None
        self.nbrCam=nbrCam
        if ipCam!=None:
            self.ipCam=ipCam
            self.arduinoCam=[]
            for ip in self.ipCam:
                self.arduinoCam.append(ArduinoCam(ip))
            for cam in self.arduinoCam:
                cam.start()

    def toggleAffichageDroite(self):
        with self.lock:
            if self.affichageDroite==None:
                self.affichageDroite=Screen()
            else:
                self.affichageDroite.quit()
                self.affichageDroite=None

    def calibrationMode(self,cw):
        with self.lock:
            self.cw=cw

    def edit_conf(self,filename):
        with self.lock:
            self.GA = gestionAction.gestionAction.read_from_file(filename)


    def stop(self):
        with self.lock:
            if self.arduinoCam!=None:
                for cam in self.arduinoCam:
                    cam.stop()
                    cam.join()
            self.stopped=True

    def isStopped(self):
        with self.lock:
            return self.stopped



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

    def run(self):
        #i=0
        #while (i<1*12):
        #    (grabbed1, frame1) = cam1.read()
        #    i=i+1
        Mouv = None
        while (not self.isStopped()):
            Mouv=getMouv(self,cam=self.arduinoCam, nbrCam=self.nbrCam)
            if Mouv != None :
                #Mouv.save_to_svg("bidule.svg")
                with self.lock:
                    if (self.GA.compare_to_mouvement(Mouv)):
                        Mouv = None


        cv2.destroyAllWindows()


def find_angle_from_frame(frame, name):
    if frame is None:
        return
    greenLower = (66, 85, 25)
    greenUpper = (83, 255, 255)
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
        if ("Bas_Gauche" in name or "Haut_Droite" in name):
            angle = -((width-x)/(width/55.0)+17)+gestionCamera.correctionAngle[name]
        else:
            angle = x/(width/55.0)+17+gestionCamera.correctionAngle[name]
        #angle = float(math.atan(float((1)))*180/math.pi)
        #print name, angle
        return angle


def check_touch(x,y,data):
    if(x!=0 and y!=0):
    # Distance calculation
        if(len(data)==0):
            return False, [x , y, time.clock()]
        dist = math.sqrt((math.pow((x-data[0]),2))+(math.pow((y-data[1]),2)))
        #instantaneous velocity calculation pixel/seconde
        vit = (dist/(time.clock()-data[2]))
        #print time.clock()-data[2]
        data = [x,y,time.clock()]
        #threshold to be adjusted !!!!!
        if (vit<250):
            return True,data
        else:
            return False,data
    else: return False,data

def find_angle(img):
    greenLower = (66, 85, 45)
    greenUpper = (83, 255, 255)
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
    #cv2.imshow("Mask", mask)
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
        #angle = float(math.atan(float((1)))*180/math.pi
        return angle

def compute_angle_from_pos(x1,y1,x2,y2):
    a=math.atan((y1-y2)/(x1-x2))
    a=a*180/math.pi
    return a

def compute_intersect(a1,xc1,yc1,a2,xc2,yc2):
    if(a1==a2):
        return None
    a1=a1*math.pi/180
    a2=a2*math.pi/180
    x= (yc1 - math.tan(a1)*xc1 - (yc2 - math.tan(a2)*xc2))/(math.tan(a2)-math.tan(a1))
    y= math.tan(a1)*(x-xc1)+yc1
    return (x,y)

def getMouv(GC=None,mouv=None, cam=None, nbrCam=None):
    if nbrCam == None:
        nbrCam=4
    size=pyautogui.size()
    poscam={"Bas_Gauche": (0,size[1]), "Bas_Droite": (size[0],size[1]), "Haut_Gauche": (0,0), "Haut_Droite": (size[0],0)}
    vid= ["Bas_Droite", "Haut_Droite", "Haut_Gauche", "Bas_Gauche"]
    mycam=[]
    if (cam==None):
        for i in range(1,nbrCam+1):
            mycam.append(cv2.VideoCapture(i))

    #i=0
    #while (i<1*12):
    #    (grabbed1, frame1) = cam1.read()
    #    i=i+1

    data = []
    tab=[]
    mouvbegin=False
    angledebut=[]
    errorframe = 0
    while True:
        #print errorframe
        if(GC != None):
            if (GC.isStopped()):
                break
        #print cam
        frame=[]
        if (cam==None):
            for c in mycam:
                frame.append(c.read()[1])
        else:
            for c in cam:
                frame.append(c.get_frame())

        angles=[]
        if (GC!= None and GC.cw!=None):
            time.sleep(1)
        for i in range(len(frame)):
            if (frame[i]!=None or not (gestionCamera.correction and gestionCamera.correctionAngle[vid[i]]==0)):
                a = find_angle_from_frame(frame[i], vid[i])
                if (a!=None):
                    angles.append((a, vid[i]))
        if (GC!= None and GC.affichageDroite!=None):
            line=[]
            for angle in angles:
                    line.append(((int)(angle[0]),poscam[angle[1]][0],poscam[angle[1]][1]))
            GC.affichageDroite.createline(line)

        if (GC!= None and GC.cw!=None):
            if (len(angles)>=nbrCam-1):
                cx=size[0]/2.0
                cy=size[1]/2.0
                for angle in angles:
                    a = compute_angle_from_pos(cx,cy,poscam[angle[1]][0],poscam[angle[1]][1])
                    gestionCamera.correctionAngle[angle[1]]=a-angle[0]
                    print gestionCamera.correctionAngle
                gestionCamera.correction=True
                GC.cw.quit()
                print "end"
                GC.calibrationMode(None)

        else:
            #il faut que toujours les meme camera capte le meme mouvement
            if len(angledebut)!=0:
                anglesbis=[]
                for angle in angles:
                    if (angle[1] in angledebut):
                        anglesbis.append(angle)
                angles=anglesbis

            if (len(angles)>=3):
                #print angles
                i=0
                coords=[]
                while(i<len(angles)-1):
                    j = i+1
                    #calcul de toute les intersection
                    while(j < len(angles)):
                        if ((("Haut_Droite" in angles[i][1]) and ("Bas_Gauche" in angles[j][1])) or (("Haut_Droite" in angles[j][1]) and ("Bas_Gauche" in angles[i][1])) or (("Bas_Droite" in angles[i][1] ) and ( "Haut_Gauche" in angles[j][1])) or (("Bas_Droite" in angles[j][1]) and ( "Haut_Gauche" in angles[i][1]))):
                            j=j+1
                            continue

                        coord = compute_intersect(angles[i][0],poscam[angles[i][1]][0],poscam[angles[i][1]][1], angles[j][0], poscam[angles[j][1]][0],poscam[angles[j][1]][1])
                        if coord is not None:
                            coords.append(coord)
                        j=j+1
                    i=i+1

                if (len(coords)==0):
                    continue

                x,y=compute_coord(coords)
                errorframe=0
                touch,data=check_touch(x,y,data)
                #print(touch)
                if touch:
                    mouvbegin=True
                if mouvbegin:
                        if len(tab)==0:
                            for angle in angles:
                                angledebut.append(angle[1])
                        #print x,y
                        tab.append((x,y))
                        if len(tab)>15:
                            mouvbegin=False
                            supertab=[]
                            supertab.append(tab)
                            mouv=Mouvements(supertab)
                            return mouv

                        #if mouv!=None:
                        #    mouv.add_new_pos_to_finger(0,(x,y))
                        #    return mouv
                        #else:
                            #supertab=[]
                            #supertab.append(tab)
                            #mouv=Mouvements(supertab)
                            #return Mouv

                        #cam1.release()
                        #cam2.release()
                        #print tab
            else:
                if(errorframe<10 and mouvbegin):
                    errorframe+=1
                else:
                    #print tab
                    mouvbegin=False
                    if (len(tab)!=0):
                        supertab=[]
                        supertab.append(tab)
                        mouv=Mouvements(supertab)
                        return mouv
                #else:
                #    return mouv

        #time.sleep(0.05)


    cv2.destroyAllWindows()

def compute_coord(coords):
    x=0
    y=0
    #print coords
    for coord in coords:
        x+=coord[0]/len(coords)
        y+=coord[1]/len(coords)
    #print x,y

    return x,y


if __name__ == '__main__':
    size=pyautogui.size()
    poscam={"Bas_Gauche": (0,size[1]), "Bas_Droite": (size[0],size[1]), "Haut_Gauche": (0,0), "Haut_Droite": (size[0],0)}
    vid=[]
    cam=[]
    if (len(sys.argv)<6):
        for i in range(1,len(sys.argv)):
            vid.append(sys.argv[i])
            cam.append(cv2.VideoCapture(i))
    else:
        for i in range(1, (len(sys.argv)+1)/2):
            vid.append(sys.argv[i])
        for i in range(1+len(vid), len(sys.argv)):
            cam.append(ArduinoCam(sys.argv[i]))
        for c in cam:
            c.start()
    #while (i<1*12):
    #    (grabbed1, frame1) = cam1.read()
    #    i=i+1

    data = []
    tab=[]
    mouvbegin=False
    angledebut=[]
    while True:

        frame=[]
        if(len(sys.argv)<6):
            for c in cam:
                frame.append(c.read()[1])
        else:
            for c in cam:
                frame.append(c.get_frame())

        angles=[]
        for i in range(len(frame)):
            if (frame[i]!=None):
                a = find_angle_from_frame(frame[i], vid[i])
                if (a!=None):
                    angles.append((a, vid[i]))

        #print a1,a2,a3
        for i in range(len(frame)):
            if(frame[i] is not None):
                cv2.imshow("Frame"+`i`, frame[i])

        if len(angledebut)!=0:
            anglesbis=[]
            for angle in angles:
                if (angle[1] in angledebut):
                    anglesbis.append(angle)
            angles=anglesbis

        if (len(angles)>=3):
            print len(angles)
            i=0
            coords=[]
            while(i<len(angles)-1):
                j = i+1
                while(j < len(angles)):
                    if ((("Haut_Droite" in angles[i][1]) and ("Bas_Gauche" in angles[j][1])) or (("Haut_Droite" in angles[j][1]) and ("Bas_Gauche" in angles[i][1])) or (("Bas_Droite" in angles[i][1] ) and ( "Haut_Gauche" in angles[j][1])) or (("Bas_Droite" in angles[j][1]) and ( "Haut_Gauche" in angles[i][1]))):
                        j=j+1
                        continue

                    coord = compute_intersect(angles[i][0],poscam[angles[i][1]][0],poscam[angles[i][1]][1], angles[j][0], poscam[angles[j][1]][0],poscam[angles[j][1]][1])
                    if coord is not None:
                        coords.append(coord)
                    j=j+1
                i=i+1
            if (len(coords)==0):
                continue
            x,y=compute_coord(coords)

            touch,data=check_touch(x,y,data)
            print(touch)
            if touch:
                mouvbegin=True
            if mouvbegin:
                    tab.append((x,y))
                    #print tab
        else:
            mouvbegin=False

        key = cv2.waitKey(60) & 0xFF
        if key == ord("q"):
            if (len(tab)!=0):
                supertab=[]
                supertab.append(tab)
                Mouv=Mouvements(supertab)
                Mouv.save_to_svg("bidule.svg")
                Mouvements.read_from_file("presentation/mouv_droite").save_to_svg("mouv_droite.svg")
                print(Mouv.look_like(Mouvements.read_from_file("presentation/mouv_droite")))
            if (len(sys.argv)>6):
                for c in cam:
                    c.stop()
                    c.join()
            break

        time.sleep(0.08)


    #cam1.release()
    #cam2.release()
    cv2.destroyAllWindows()
