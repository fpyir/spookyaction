import logging
from functools import wraps
from error_handling import *

logging.basicConfig(filename='loglines.txt',level=logging.INFO)

def log(fn):
    @wraps(fn)
    def logged_function(*args, **kwargs):
        name = fn.__name__
        arglist = "%s, " * len(args)
        kwargslist = ["{}=%s, ".format(key) for key in kwargs.keys()]
        kwargsvals = [val for val in kwargs.values()]
        formatted = ("Called {name}("+arglist+''.join(kwargslist)+")").format(name=name)

        format_list = list(args) + list(kwargsvals)
        logging.info(formatted, *format_list)
        return fn(*args, **kwargs)
    return logged_function
