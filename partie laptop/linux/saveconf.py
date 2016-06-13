import default
from gestionAction import gestionAction

GA = gestionAction({},{default.one_finger_dont_move: default.click})
GA.save_to_file("EcrTactDefault.conf")
