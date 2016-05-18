#
# coding=utf-8
import pygtk
pygtk.require("2.0")

import pickle
from systray import SystrayIconApp
import gtk
import gobject
import pyautogui
import time
from Mouvement import Mouvements

import os

class conf:
    """docstring for """
    def __init__(self,dict={SystrayIconApp.ECRTACT : "ecrTactDef.conf", SystrayIconApp.PRNOTE : "prNoteDef.conf", SystrayIconApp.TCHPAD : "tchPadDef.conf"  }):
        #a chaque mode on associe un fichier de conf
        self.dict=dict

    def save_to_file(self,filename):
        if filename=="default.cfg":
            print "interdit de reecrire la save par default"
            return
        with open("conf/"+filename,"wb") as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(self)

    def use_this_conf(self):
        return self.save_to_file("conf.cfg")

    def get_file(self,key):
        return self.dict[key]

    @staticmethod
    def read_from_file(filename):
        with open("conf/"+filename, "rb") as fichier:
            unpickler = pickle.Unpickler(fichier)
            conf=unpickler.load()
            return conf

    @staticmethod
    def start_conf():
        return conf.read_from_file("conf.cfg")

    @staticmethod
    def list_conf_file():
        files=os.listdir("conf")
        conffiles=[]
        for file in files:
            if(file.split(".")[-1]=="cfg"):
                conffiles.append(file)

        return conffiles


class confWindow:
    """docstring for """
    def __init__(self,systray):
        interface = gtk.Builder()
        interface.add_from_file('glade/confwindow.glade')

        self.systray=systray
        # initfileconf
        self.fileEcrTact = interface.get_object("fileEcrTact")
        self.fileTchPad = interface.get_object("fileTchPad")
        self.filePrNote = interface.get_object("filePrNote")
        self.mouvFileOpener= interface.get_object("OpenMouvFile")
        self.mouvFileOpener.set_current_folder("mouv")
        self.imgMouvSvg= interface.get_object("imMouvSVG")
        interface.connect_signals(self)

        #ComboBox init
        cell = gtk.CellRendererText()
        self.confFileChooser = interface.get_object("confFileChoose")
        self.confFileChooser.pack_start(cell, True)
        self.confFileChooser.add_attribute(cell,'text',0)
        self.store=gtk.ListStore(gobject.TYPE_STRING)
        self.init_list()

    def conf_changed(self,widget):
        self.confFileChooser.set_active(len(self.store)-1)

    def conf_choose_changed(self, widget):
        file=widget.get_active_text()
        if file!="personalisé" and file is not None:
            config=conf.read_from_file(file+".cfg")
            self.fileEcrTact.set_filename("conf/"+config.get_file(SystrayIconApp.ECRTACT))
            self.fileTchPad.set_filename("conf/"+config.get_file(SystrayIconApp.TCHPAD))
            self.filePrNote.set_filename("conf/"+config.get_file(SystrayIconApp.PRNOTE))

    def init_list(self):
        self.store.clear()
        for file in conf.list_conf_file():
            self.store.append([file.rsplit(".",1)[0]])
        self.store.append(["personalisé"])
        self.confFileChooser.set_model(self.store)
        self.confFileChooser.set_active(0)

    def save_conf(self,widget):
        dict={SystrayIconApp.ECRTACT : self.fileEcrTact.get_filename().rsplit("/",1)[1] , SystrayIconApp.PRNOTE : self.filePrNote.get_filename().rsplit("/",1)[1], SystrayIconApp.TCHPAD :self.fileTchPad.get_filename().rsplit("/",1)[1]   }
        config = conf(dict)
        file=pyautogui.prompt("nom du fichier?")
        if (file=="personalisé" or file=="default"):
            pyautogui.alert("interdit de sauvegarder au nom personalisé ou default")
            return
        config.save_to_file(file+".cfg")
        config.use_this_conf()
        self.systray.reload_conf()
        self.init_list()

    def open_mouv_file(self,widget):
        file=widget.get_filename().rsplit("mouv/",1)[1]
        self.mouvement=Mouvements.read_from_file(file).save_to_svg("temp.svg")
        self.update_picture()

    def update_picture(self):
        pixbuf = gtk.gdk.pixbuf_new_from_file("mouv/temp.svg")
        width=pixbuf.get_width()
        height=pixbuf.get_height()
        imgwidth=self.imgMouvSvg.get_allocation().width
        imgheight=self.imgMouvSvg.get_allocation().height
        scaled_buf = pixbuf.scale_simple(imgwidth,height*imgwidth/width,gtk.gdk.INTERP_BILINEAR)
        self.imgMouvSvg.set_from_pixbuf(scaled_buf)

    def on_mainWindow_destroy(self, widget):
        gtk.main_quit()

    # a changer lorsque l'on recuperera les positions
    def record_mouvement(self,widget):
        pyautogui.alert("appuyé sur entré lorsque vous êtes près a enregistrer")
        oldx,oldy=pyautogui.position()
        mouv=False
        tab=[]
        while True:
            x,y=pyautogui.position()
            if (not mouv) and (x!=oldx or y!=oldy):
                mouv=True;
                tab=[]
            if mouv:
                if(x==oldx and y==oldy):
                    mouv=False
                    allFinger=[]
                    allFinger.append(tab)
                    self.mouvement=Mouvements(allFinger)
                    self.mouvement.save_to_svg("temp.svg")
                    self.update_picture()
                    break
                else:
                    tab.append((x,y))
                    oldx=x
                    oldy=y

            time.sleep(0.03)

    def save_mouvement(self,widget):
        self.mouvement.save_to_file(pyautogui.prompt("nom du fichier?"))

if __name__ == '__main__':
    confWindow()
    gtk.main()
