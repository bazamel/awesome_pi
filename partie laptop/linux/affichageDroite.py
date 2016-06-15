import pygtk
pygtk.require('2.0')
import gtk
import pyautogui
import math
import cairo

class Screen():
    """docstring for """
    def quit(self):
        self.win.destroy()

    def __init__(self):
        self.win = gtk.Window()
        self.win.fullscreen()
        self.win.set_app_paintable(True)
        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.set_size_request(pyautogui.size()[0],pyautogui.size()[1])
        self.win.add(self.drawing_area)

        self.drawing_area.connect("expose-event", self.expose)
        self.drawing_area.show()
        self.win.show()

    def setDroite(self,droites):
        self.droites=droites

    def expose(self,widget,event):
        cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        # Makes the mask fill the entire window
        cr.rectangle(0.0, 0.0, pyautogui.size()[0],pyautogui.size()[1])
        # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
        cr.fill()

        cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_source_rgb(1,1,1)
        cr.set_line_width(5)
        if self.droites!=None:
            for droite in self.droites:
                angle = droite[0]*math.pi/180
                x2=droite[1]
                y2=droite[2]
                if x2!=0:
                    y= math.tan(angle)*(0-x2)+y2
                    cr.move_to(0,y)
                    cr.line_to(x2,y2)
                    cr.stroke()
                else:
                    y= math.tan(angle)*(pyautogui.size()[0]-x2)+y2
                    cr.move_to(pyautogui.size()[0],y)
                    cr.line_to(x2,y2)
                    cr.stroke()


    def createline(self,droites):
        self.setDroite(droites)
        self.drawing_area.queue_draw()





if __name__ == '__main__':
    #t.createline([(45,1920,1080)])
    t = Screen()
    t.createline([(45,0,0),(45,1920,1080)])
    gtk.main()
    #t.test.event_generate("quit",when="tail")
    #t = Screen([(45,0,0)])
