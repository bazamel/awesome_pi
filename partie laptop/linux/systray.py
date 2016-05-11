#!/usr/bin/python
# -*- coding: utf-8 -*-


import gtk
import pynotify
import pango
import calibrage

class SystrayIconApp:
	ECRTACT=0
	TCHPAD=1
	PRNOTE=2

	def __init__(self):
		self.mode = SystrayIconApp.ECRTACT
		self.tray = gtk.StatusIcon()
		self.tray.set_from_file("icon.png")
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.set_tooltip(('Sample tray app'))


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

		# add quit item
		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', gtk.main_quit)

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


	def on_tchPad_click(self,widget):
		self.mode = SystrayIconApp.TCHPAD
		pynotify.init("image")
		n = pynotify.Notification("SMATCH", "touchPad", "/home/moubinous/Documents/PI/awesome_pi/partie laptop/linux/icon.png",)
		n.show()


	def on_prNote_click(self,widget):
		self.mode = SystrayIconApp.PRNOTE
		pynotify.init("image")
		n = pynotify.Notification("SMATCH", "prise de note", "/home/moubinous/Documents/PI/awesome_pi/partie laptop/linux/icon.png",)
		n.show()



	def  show_calibrage_dialog(self, widget):
		calibrage.calibrageWindows()




if __name__ == "__main__":
	SystrayIconApp()
	gtk.main()
