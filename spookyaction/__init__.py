import pyautogui
import os, sys
from item_object import Item, Items
from functools import wraps
from error_handling import Error

METHODS = { }
currentresults = []
names = os.listdir('./'+sys.argv[0]+'/imgs')
Items = {name: Item(name) for name in names}

class GUI_INTERFACE():
    def __init__(self):
        pass

    def keywrite(self, *args):
        pyautogui.keywrite(list(args))

ui = GUI_INTERFACE()

def new_method(name):
    def new_method_wrapper(fn):
        METHODS[name] = fn
        @wraps(fn)
        def wrapped_method(*args, **kwargs):
            fn(*args, **kwargs)
        return wrapped_method
    return new_method_wrapper


def run(obj=None, cmd=None, cmd_args=None, cmd_kwargs=None):
    METHODS["START"](obj, cmd)
    try:
        currentresults = METHODS[cmd](*cmd_args, **cmd_kwargs)
    except Error as e:
        METHODS["FAILED"](e, obj, cmd)
    else:
        METHODS["COMPLETED"](obj, cmd)
