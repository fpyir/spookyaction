import pyautogui


class GUI_INTERFACE():
    def __init__(self):
        pass

    def keywrite(self, *args, **kwargs):
        pyautogui.typewrite(list(args), interval=kwargs.get("delay", 0.1))

    def write(self, msg):
        pyautogui.typewrite(msg)
