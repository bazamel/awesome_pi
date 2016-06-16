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
import gestionAction
from gestionsouris import gestionSouris
import os
import frame
from frame import gestionCamera

from get_frame_from_arduino import ArduinoCam

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
    def list_cfg_file():
        files=os.listdir("conf")
        cfgfiles=[]
        for file in files:
            if(file.split(".")[-1]=="cfg"):
                cfgfiles.append(file)

        return cfgfiles

    @staticmethod
    def list_conf_file():
        files=os.listdir("conf")
        conffiles=[]
        for file in files:
            if(file.split(".")[-1]=="conf"):
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


        self.listMouvFunc = interface.get_object("listMouvFunc")
        self.add_item_to_list()

        self.listMouvFunc2 = interface.get_object("listMouvFunc2")
        self.add_item_to_list2()

        interface.connect_signals(self)

        #ComboBox init
        cell = gtk.CellRendererText()
        self.cfgFileChooser = interface.get_object("cfgFileChoose")
        self.cfgFileChooser.pack_start(cell, True)
        self.cfgFileChooser.add_attribute(cell,'text',0)
        self.store=gtk.ListStore(gobject.TYPE_STRING)
        self.init_list_cfg()

        #ComboBox init
        cell = gtk.CellRendererText()
        self.confFileChooser = interface.get_object("confFileChoose")
        self.confFileChooser.pack_start(cell, True)
        self.confFileChooser.add_attribute(cell,'text',0)
        self.storeconf=gtk.ListStore(gobject.TYPE_STRING)
        self.init_list_conf()


    def add_item_to_list(self,widget=None,filename=None,func=None):
        if (widget!=None):
            self.confFileChooser.set_active(len(self.storeconf)-1)
            if widget.get_parent()!=self.listMouvFunc.get_children()[len(self.listMouvFunc.get_children())-1]:
                return
        fileChooser = gtk.FileChooserButton("Select a File", backend=None)
        fileChooser.set_current_folder("mouv/")
        fileChooser.connect("file-set", self.add_item_to_list)
        entry = gtk.Entry()
        hbox = gtk.HBox(False)
        hbox.add(fileChooser)
        hbox.add(entry)
        self.listMouvFunc.add(hbox)
        hbox.show()
        entry.show()
        fileChooser.show()
        if (filename is not None and func is not None):
            entry.set_text(func)
            fileChooser.set_filename(filename)

    def add_item_to_list2(self, widget=None, func1=None, func2=None):
        if (widget!=None):
            self.confFileChooser.set_active(len(self.storeconf)-1)
            if widget.get_parent()!=self.listMouvFunc2.get_children()[len(self.listMouvFunc2.get_children())-1]:
                return
        entry = gtk.Entry()
        entry2 = gtk.Entry()

        hbox = gtk.HBox(True)
        hbox.add(entry)
        hbox.add(entry2)
        self.listMouvFunc2.add(hbox)
        hbox.show()
        entry.show()
        entry2.show()
        if (func1 is not None and func2 is not None):
            entry.set_text(func1)
            entry2.set_text(func2)
        entry.connect("changed",self.add_item_to_list2)


    def cfg_changed(self,widget):
        self.cfgFileChooser.set_active(len(self.store)-1)


    def conf_choose_changed(self, widget):
        file=widget.get_active_text()
        if file!="nouveau" and file is not None:
            for child in self.listMouvFunc2.get_children():
                self.listMouvFunc2.remove(child)
            for child in self.listMouvFunc.get_children():
                self.listMouvFunc.remove(child)
            GA = gestionAction.gestionAction.read_from_file(file+".conf")
            for excep in GA.exception.keys():
                func = GA.exception[excep]
                self.add_item_to_list2(None, excep.__module__+"."+excep.__name__,func.__module__+"."+func.__name__)
            for key in GA.dict.keys():
                func=GA.dict[key]
                self.add_item_to_list(None,"mouv/"+key,func.__module__+"."+func.__name__)
            self.add_item_to_list(None)
            self.add_item_to_list2(None)

    def cfg_choose_changed(self, widget):
        file=widget.get_active_text()
        if file!="personalisé" and file is not None:
            config=conf.read_from_file(file+".cfg")
            self.fileEcrTact.set_filename("conf/"+config.get_file(SystrayIconApp.ECRTACT))
            self.fileTchPad.set_filename("conf/"+config.get_file(SystrayIconApp.TCHPAD))
            self.filePrNote.set_filename("conf/"+config.get_file(SystrayIconApp.PRNOTE))

    def init_list_conf(self):
        self.storeconf.clear()
        for file in conf.list_conf_file():
            self.storeconf.append([file.rsplit(".",1)[0]])
        self.storeconf.append(["nouveau"])
        self.confFileChooser.set_model(self.storeconf)
        self.confFileChooser.set_active(0)

    def init_list_cfg(self):
        self.store.clear()
        for file in conf.list_cfg_file():
            self.store.append([file.rsplit(".",1)[0]])
        self.store.append(["personalisé"])
        self.cfgFileChooser.set_model(self.store)
        self.cfgFileChooser.set_active(0)


    def save_conf(self,widget):
        dict={}
        excpt={}
        for child in self.listMouvFunc.get_children():
            c=child.get_children()
            if (c[0].get_filename()==None or len(c[1].get_text().split("."))<2):
                continue
            file = c[0].get_filename().rsplit("mouv/",1)[1]
            stringFunc=c[1].get_text()
            module=stringFunc.split(".")[0]
            funcname=stringFunc.split(".")[1]
            m=__import__(module)
            f=getattr(m,funcname)
            dict[file]=f

        for child in self.listMouvFunc2.get_children():
            c=child.get_children()
            if (len(c[0].get_text().split("."))<2 or len(c[1].get_text().split("."))<2):
                continue
            module1 = c[0].get_text().split(".")[0]
            funcname1 = c[0].get_text().split(".")[1]
            m1=__import__(module1)
            f1=getattr(m1,funcname1)

            module2=c[1].get_text().split(".")[0]
            funcname2=c[1].get_text().split(".")[1]
            m2=__import__(module2)
            f2=getattr(m2,funcname2)
            excpt[f1]=f2

        GA = gestionAction.gestionAction(dict,excpt)
        namefile=pyautogui.prompt("nom du fichier?")
        if (namefile=="personalisé" or namefile=="default"):
            pyautogui.alert("interdit de sauvegarder au nom personalisé ou default")
            return
        GA.save_to_file(namefile+".conf")
        self.init_list_conf()


    def save_cfg(self,widget):
        dict={SystrayIconApp.ECRTACT : self.fileEcrTact.get_filename().rsplit("conf/",1)[1] , SystrayIconApp.PRNOTE : self.filePrNote.get_filename().rsplit("conf/",1)[1], SystrayIconApp.TCHPAD :self.fileTchPad.get_filename().rsplit("conf/",1)[1]   }
        config = conf(dict)
        file=pyautogui.prompt("nom du fichier?")
        if (file=="personalisé" or file=="default"):
            pyautogui.alert("interdit de sauvegarder au nom personalisé ou default")
            return
        config.save_to_file(file+".cfg")
        config.use_this_conf()
        self.systray.reload_conf()
        self.init_list_cfg()

    def use_cfg(self,widget):
        dict={SystrayIconApp.ECRTACT : self.fileEcrTact.get_filename().rsplit("conf/",1)[1] , SystrayIconApp.PRNOTE : self.filePrNote.get_filename().rsplit("conf/",1)[1], SystrayIconApp.TCHPAD :self.fileTchPad.get_filename().rsplit("conf/",1)[1]   }
        config = conf(dict)
        config.use_this_conf()
        self.systray.reload_conf()
        self.init_list_cfg()

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
        self.systray.GS.stop()
        self.systray.GS.join()
        pyautogui.alert("appuyé sur entré lorsque vous êtes près a enregistrer")
        cam =[]
        if (self.systray.ipCam!=None):
            for ip in self.systray.ipCam:
                cam.append(ArduinoCam(ip))
            for c in cam:
                c.start()
            self.mouvement=frame.getMouv(cam=cam)
        else:
            self.mouvement=frame.getMouv(nbrCam=self.systray.nbrCam)
        self.mouvement.save_to_svg("temp.svg")
        self.update_picture()
        for c in cam:
            c.stop()
            c.join()
        self.systray.GS = gestionCamera(self.systray.conf.dict[self.systray.mode], self.systray.ipCam, self.systray.nbrCam, self.systray.debug)
        self.systray.GS.start()

    def save_mouvement(self,widget):
        self.mouvement.save_to_file(pyautogui.prompt("nom du fichier?"))

if __name__ == '__main__':
    confWindow()
    gtk.main()
