# coding=utf-8


from Mouvement import Mouvements
import pyautogui
import pickle
import importlib
import os

class gestionAction():
    """docstring for """
    def __init__(self,dict,exception={}):
        #dictionnaire possedant {key=fichierMouvement : value=Action a faire}
        self.dict = dict
        #dictionaire liant fonction de test à fonction a realiser
        #par exemple si on n'a qu'un seul doigt et que l'on veut juste deplacer la souris
        self.exception=exception

    def compare_to_mouvement(self,mouv):
        for excpt in self.exception.keys():
            if (excpt(mouv)):
                self.exception[excpt]()
                return

        for filename in self.dict.keys():
            if (mouv.look_like(Mouvements.read_from_file(filename))):
                self.dict[filename]()


    def save_to_file(self,filename):
        filename="conf/"+filename
        if ((not os.path.isdir(filename.rsplit('/',1)[0])) and os.path.exists(filename.rsplit('/',1)[0])) or not os.path.exists(filename.rsplit('/',1)[0]):
            os.makedirs(filename.rsplit('/',1)[0])
        with open(filename,"wb") as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(self)

    @staticmethod
    def read_from_file(filename):
        filename = "conf/"+filename
        with open(filename,"rb") as fichier:
            unpickler=pickle.Unpickler(fichier)
            conf=unpickler.load()
            return conf

def printYolo():
    print "Yolo"

def left_click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def rien():
    return

def unDoigt(mouv):
    return mouv.nbrDoigt==1
