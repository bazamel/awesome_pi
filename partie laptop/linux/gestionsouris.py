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
            mouvement.save_to_svg("test.svg")
            if mouvement.look_like(Mouvements.read_from_file("mouvSouris"),90):
                print "ca marche"
        else:
            tab.append((x,y))
            oldx=x
            oldy=y

    time.sleep(0.05)
