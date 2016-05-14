import importlib

imp="pyautogui"
test=importlib.import_module(imp)
print test.position()
