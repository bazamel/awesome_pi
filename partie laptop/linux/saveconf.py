import default
from gestionAction import gestionAction

GA = gestionAction({},{default.one_finger: default.edit_mous_pos})
GA.save_to_file("tchDefault.conf")
