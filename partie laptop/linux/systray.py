#!/usr/bin/python
# -*- coding: utf-8 -*-


import gtk
import pynotify
import pango
import calibrage
import conf
from gestionsouris import gestionSouris
from frame import gestionCamera
import signal
import argparse

import sys

class SystrayIconApp:
	ECRTACT=0
	TCHPAD=1
	PRNOTE=2


	def __init__(self, ipCam=None,nbrCam=None,debug=None):
		self.mode = SystrayIconApp.ECRTACT
		self.tray = gtk.StatusIcon()
		self.tray.set_from_file("icon.png")
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.set_tooltip(('Sample tray app'))
		self.conf=conf.conf.start_conf()
		self.debug=debug
		self.ipCam=ipCam
		self.nbrCam=nbrCam
		self.GS = gestionCamera(self.conf.dict[self.mode],self.ipCam, self.nbrCam,debug)
		self.GS.start()





	def on_right_click(self, icon, event_button, event_time):
		self.make_menu(event_button, event_time)

	def make_menu(self, event_button, event_time):
		menu = gtk.Menu()

		# show calibrage dialog
		calibrage = gtk.MenuItem("Calibrage")
		calibrage.show()
		menu.append(calibrage)
		calibrage.connect('activate', self.show_calibrage_dialog)

		self.addSeparator(menu)

		#Ecran tactile

		ecrTact = gtk.MenuItem("Ecran Tactile")
		ecrTact.show()
		menu.append(ecrTact)
		ecrTact.connect('activate', self.on_ecrTact_click)



		#touchpad
		tchPad = gtk.MenuItem("TouchPad")
		tchPad.show()
		menu.append(tchPad)
		tchPad.connect('activate', self.on_tchPad_click)

		#prise de note
		prNote = gtk.MenuItem("prise de note")
		prNote.show()
		menu.append(prNote)
		prNote.connect('activate', self.on_prNote_click)

		self.addSeparator(menu)

		#configuration

		conf=gtk.MenuItem("configuration")
		conf.show()
		menu.append(conf)
		conf.connect('activate', self.on_conf_click)

		afficheD=gtk.MenuItem("affichage des droites")
		afficheD.show()
		menu.append(afficheD)
		afficheD.connect('activate', self.toggleAffichageDroite)

		# add quit item
		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', self.on_quit)

		menu.popup(None, None, gtk.status_icon_position_menu,
		           event_button, event_time, self.tray)


	def addSeparator(self, menu):
		sep=gtk.SeparatorMenuItem()
		sep.show()
		menu.append(sep)


	def on_ecrTact_click(self,widget):
		self.mode = SystrayIconApp.ECRTACT
		pynotify.init("image")
		n = pynotify.Notification("SMATCH", "Ecran Tactile", "/home/moubinous/Documents/PI/awesome_pi/partie laptop/linux/icon.png",)
		n.show()
		self.GS.edit_conf(self.conf.dict[self.mode])


	def on_tchPad_click(self,widget):
		self.mode = SystrayIconApp.TCHPAD
		pynotify.init("image")
		n = pynotify.Notification("SMATCH", "touchPad", "/home/moubinous/Documents/PI/awesome_pi/partie laptop/linux/icon.png",)
		n.show()
		self.GS.edit_conf(self.conf.dict[self.mode])

	def toggleAffichageDroite(self,widget):
		self.GS.toggleAffichageDroite()

	def on_prNote_click(self,widget):
		self.mode = SystrayIconApp.PRNOTE
		pynotify.init("image")
		n = pynotify.Notification("SMATCH", "prise de note", "/home/moubinous/Documents/PI/awesome_pi/partie laptop/linux/icon.png",)
		n.show()
		self.GS.edit_conf(self.conf.dict[self.mode])

	def on_conf_click(self,widget):
		conf.confWindow(self)
		#return

	def reload_conf(self):
		self.conf=conf.conf.start_conf()
		self.GS.edit_conf(self.conf.dict[self.mode])

	def  show_calibrage_dialog(self, widget):
		cw = calibrage.calibrageWindows()
		self.GS.calibrationMode(cw)

	def on_quit(self,widget):
		self.GS.stop()
		self.GS.join()
		gtk.main_quit()


def get_arguments():
	ap= argparse.ArgumentParser()
	ap.add_argument('-u', '--usb',required=False,help="use the Webcam in USB",action="store_true")
	ap.add_argument('-c', '--cam', required=False,help="number of webcam required default 4" )
	ap.add_argument('-d', '--debug', required=False,help="screen of debug", action="store_true")
	args = vars(ap.parse_args())
	return args


if __name__ == "__main__":
	args = get_arguments()
	ipCam= None
	if not args['usb']:
		ipCam = ["cambasdroite.local","camhautdroite.local","camhautgauche.local","cambasgauche.local"]
		if args['cam']:
			ipCam =ipCam[:int(args['cam'])]

	#while(i<len(sys.argv)):
	#	ipCam.append(sys.argv[i])
	#	i+=1
	#if(len(sys.argv)==1):
	#	ipCam=None
	print args['usb'], args['cam']

	if (args['cam']==None):
		args['cam']=4

	myapp=SystrayIconApp(ipCam,int(args['cam']),args['debug'])
	gtk.gdk.threads_init()
	gtk.threads_enter()
	gtk.main()
	gtk.threads_leave()
