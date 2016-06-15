import pygtk
pygtk.require('2.0')
import gtk, sys, cairo
from math import pi
import cv2
from get_frame_from_arduino import ArduinoCam
import pyautogui
from frame import find_angle_from_frame
from threading import Thread, RLock


class calibrageWindows():

    def __init__(self):
        self.win = gtk.Window()
        self.win.set_decorated(False)
        self.win.set_icon_from_file("icon.png")

        # Makes the window paintable, so we can draw directly on it

        self.win.set_app_paintable(True)
        self.win.fullscreen()

        # This sets the windows colormap, so it supports transparency.
        # This will only work if the wm support alpha channel
        screen = self.win.get_screen()
        rgba = screen.get_rgba_colormap()
        self.win.set_colormap(rgba)
        self.win.connect('expose-event', self.expose)

        self.win.show()

    def quit(self):
        self.win.destroy()

    def expose (self,widget, event):
        cr = widget.window.cairo_create()

        # Sets the operator to clear which deletes everything below where an object is drawn
        cr.set_operator(cairo.OPERATOR_CLEAR)
        # Makes the mask fill the entire window
        cr.rectangle(0.0, 0.0, *widget.get_size())
        # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
        cr.fill()
        # Set the compositing operator back to the default
        cr.set_operator(cairo.OPERATOR_OVER)

        # Draw a fancy little circle for demonstration purpose
        cr.set_source_rgba(1,0.0,0.0,1)
        print widget.get_size()
        cr.arc(widget.get_size()[0]/2,widget.get_size()[1]/2,
               15,0,pi*2)
        cr.fill()

if __name__ == "__main__":

    calibrageWindows()
    gtk.main()
