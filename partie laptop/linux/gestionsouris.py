import pyautogui
import time
from Mouvement import Mouvements
from threading import Thread, RLock
import gestionAction



class gestionSouris(Thread):
    """docstring for """
    def __init__(self, filename):
        Thread.__init__(self)
        self.stopped = False
        self.lock = RLock()
        self.edit_conf(filename)


    def edit_conf(self,filename):
        with self.lock:
            self.GA = gestionAction.gestionAction.read_from_file(filename)

    def stop(self):
        with self.lock:
            self.stopped=True

    def isStopped(self):
        with self.lock:
            return self.stopped

    def run(self):
        oldx,oldy=pyautogui.position()
        mouv=False
        tab=[]
        while (not self.isStopped()):
            x,y=pyautogui.position()
            if (not mouv) and (x!=oldx or y!=oldy):
                mouv=True;
                tab=[]
            if mouv:
                if(x==oldx and y==oldy):
                    mouv=False
                    allFinger=[]
                    allFinger.append(tab)
                    mouvement=Mouvements(allFinger)
                    with self.lock:
                        self.GA.compare_to_mouvement(mouvement)

                else:
                    tab.append((x,y))
                    oldx=x
                    oldy=y

            time.sleep(0.03)
