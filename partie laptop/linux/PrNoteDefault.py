# coding=utf-8
import pygtk
pygtk.require('2.0')
import gtk
import pyautogui
import math
import cairo
from threading import RLock


class ZoneDessin(object):

    ZD = None

    def quit(self,widget):
        ZoneDessin.ZD=None
        self.win.destroy()

    def erase(self,widget):
        self.droites=[]
        self.drawing_area.queue_draw()

    def __init__(self):
        self.lock=RLock()
        self.droites=[]
        self.win = gtk.Window()
        self.win.fullscreen()
        self.win.set_app_paintable(True)
        self.drawing_area = gtk.DrawingArea()
        vbox=gtk.VBox()
        self.win.add(vbox)
        vbox.add(self.drawing_area)
        btn=gtk.Button("quit")
        erase=gtk.Button("erase")
        hbox=gtk.HBox()
        hbox.show()
        vbox.add(hbox)
        vbox.show()
        hbox.add(btn)
        hbox.add(erase)
        btn.show()
        erase.show()
        self.drawing_area.set_size_request(pyautogui.size()[0],pyautogui.size()[1]-50)
        self.drawing_area.connect("expose-event", self.expose)
        self.drawing_area.show()
        self.win.show()
        btn.connect("clicked",self.quit)
        erase.connect("clicked",self.erase)

    def addPos(self,pos):
        with self.lock:
            self.droites[-1].append(pos)
        self.drawing_area.queue_draw()
        print pos

    def newFigure(self):
        with self.lock:
            self.droites.append([])

        print "new"
        #print self.droites

    def expose(self,widget,event):
        cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        # Makes the mask fill the entire window
        cr.rectangle(0.0, 0.0, pyautogui.size()[0],pyautogui.size()[1])
        # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
        cr.fill()

        cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_source_rgb(1,1,1)
        cr.set_line_width(1)
        with self.lock:
            if self.droites!=None:
                for droite in self.droites:
                    if len(droite)!=0:
                        cr.move_to(droite[0][0],droite[0][1])
                        for pos in droite:
                            cr.line_to(pos[0],pos[1])
                        cr.stroke()

def trace(mouv):
    print mouv.tabMouvementDoigts
    if ZoneDessin.ZD==None:
        ZoneDessin.ZD=ZoneDessin()

    ZD = ZoneDessin.ZD
    if (len(mouv.tabMouvementDoigts[0])>=2):
        ZD.addPos(mouv.tabMouvementDoigts[0][-1])
    else:
        ZD.newFigure()
        ZD.addPos(mouv.tabMouvementDoigts[0][-1])

def one_finger(mouv):
    return mouv.nbrDoigt==1


if __name__ == '__main__':
    ZD = ZoneDessin()
    ZD.newFigure()
    ZD.addPos((450,520))
    ZD.addPos((800,520))
    ZD.addPos((800,750))
    gtk.main()
