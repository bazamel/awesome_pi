import pyautogui
from Mouvement import Mouvements
from gestionAction import gestionAction

def one_finger(mouv):
    return (mouv.nbrDoigt==1 and len(mouv.tabMouvementDoigts[0])>1)


def edit_mous_pos(mouv):
    dx = mouv.tabMouvementDoigts[0][-1][0]-mouv.tabMouvementDoigts[0][0][0]
    dy = mouv.tabMouvementDoigts[0][-1][1]-mouv.tabMouvementDoigts[0][0][1]
    dx= dx
    dy= dy
    pyautogui.moveRel(dx,dy)
