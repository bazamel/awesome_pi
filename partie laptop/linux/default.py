import pyautogui
from Mouvement import Mouvements

def one_finger(mouv):
    return (mouv.nbrDoigt==1 and len(mouv.tabMouvementDoigts[0])>1)


def edit_mous_pos(mouv):
    dx = mouv.tabMouvementDoigts[0][-1][0]-mouv.tabMouvementDoigts[0][0][0]
    dy = mouv.tabMouvementDoigts[0][-1][1]-mouv.tabMouvementDoigts[0][0][1]
    dx= dx
    dy= dy
    pyautogui.moveRel(dx,dy)

def one_finger_dont_move(mouv):
    marge = 10
    if (mouv.nbrDoigt==1 ):
        x = mouv.tabMouvementDoigts[0][0][0]
        y = mouv.tabMouvementDoigts[0][0][1]
        for pos in mouv.tabMouvementDoigts[0]:
            if ( (x-marge <=pos[0] and x+marge >= pos[0]) and (y-marge <=pos[1] and y+marge >= pos[1]) ):
                continue
            else:
                return False
    else:
        return False

    return True



def click(mouv):
    x=0
    y=0
    for pos in mouv.tabMouvementDoigts[0]:
        x+=pos[0]/len(mouv.tabMouvementDoigts[0])
        y+=pos[1]/len(mouv.tabMouvementDoigts[0])
    print "click",x,y
    pyautogui.click(x=x,y=y)
