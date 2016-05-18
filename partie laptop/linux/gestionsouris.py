import pyautogui
import time
from Mouvement import Mouvements
import gestionAction
#import presentation

oldx,oldy=pyautogui.position()
mouv=False
tab=[]

#dict={"presentation/mouv_droite" : presentation.fleche_droite, "presentation/mouv_gauche" : presentation.fleche_gauche}
#exception={gestionAction.unDoigt : gestionAction.rien}
#GA= gestionAction.gestionAction(dict,exception)
#GA.save_to_file("presentation.conf")
GA = gestionAction.gestionAction.read_from_file("presentation.conf")

while True:
    x,y=pyautogui.position()
    if (not mouv) and (x!=oldx or y!=oldy):
        mouv=True;
        tab=[]
        print "reset"
    if mouv:
        if(x==oldx and y==oldy):
            mouv=False
            allFinger=[]
            allFinger.append(tab)
            mouvement=Mouvements(allFinger)
            GA.compare_to_mouvement(mouvement)

        else:
            tab.append((x,y))
            oldx=x
            oldy=y

    time.sleep(0.03)
