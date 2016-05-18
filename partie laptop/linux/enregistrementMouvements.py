import pyautogui
import time
from Mouvement import Mouvements

oldx,oldy=pyautogui.position()
mouv=False
tab=[]
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
            print allFinger
            mouvement=Mouvements(allFinger)
            if(pyautogui.confirm("voulez vous sauvegarder?")=="OK"):
                mouvement.save_to_file(pyautogui.prompt("nom du fichier?"))
                break
            oldx,oldy=pyautogui.position()
            #mouvement.save_to_file("mouvSouris")
            #mouvement.save_to_svg("mouvSouris.svg")
        else:
            tab.append((x,y))
            oldx=x
            oldy=y

    time.sleep(0.03)
