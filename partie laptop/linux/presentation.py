import pyautogui

def fleche_droite():
    pyautogui.press('right')

def fleche_gauche():
    pyautogui.press('left')

def unDoigt(mouv):
    return mouv.nbrDoigt==1
