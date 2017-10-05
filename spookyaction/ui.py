import pyautogui

class GUI_INTERFACE():
    def __init__(self):
        pass

    def keywrite(self, *args):
        pyautogui.keywrite(list(args))
