import pyautogui as gi
import time, os, ocr, logging, sys, re
from error_handling import *
from spooky_logs import log
from functools import partial

# needed to allow silent failing chains
class Empty:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, name):
        return self

class Item(object):
    def __init__(self, picturename, ocr_key):
        self.picturename = picturename
        self.url = picturename
        self.result = None
        self.ocr_key = ocr_key

    @log
    def __click(self, after=0.2, offx=0, offy=0):
        time.sleep(after)
        pos = gi.locateCenterOnScreen(self.url)
        print pos
        if pos:
            gi.moveTo(pos[0]+offx, pos[1]+offy)
            gi.click()
            logging.info("Clicked on %s" % self.picturename)
            return self
        else:
            logging.warning("Could not click on %s" % self.picturename)
            raise ItemNotThere(self)

    @log
    def run_when_present(self, func, *args, **kwargs):
        for _ in range(10):
            logging.info("Calling run_when_present, looking for %s",
                          self.picturename)
            if gi.locateCenterOnScreen(self.url) == None:
                logging.info("Did not find image in run_when_present. Will try again.")
                time.sleep(3)
                continue
            logging.info("Found image %s in run_when_present call.",
                         self.picturename)
            logging.info("Executing function %s in run_when_present call for %s",
                         func.__name__, self.picturename)
            self.result = func(*args, **kwargs)
            return self
        logging.warning("Never found %s in run_when_present call.", self.picturename)
        raise ItemNeverAppeared(self, self.run_when_present.__name__)

    @log
    def click(self, offx=0, offy=0):
        return self.run_when_present(self.__click, after=0.2, offx=offx, offy=offy)


    @log
    def drag_by(self, x=0, y=0):
        # to implement #
        pass

    @property
    @log
    def found(self):
        if gi.locateCenterOnScreen(self.url):
            logging.info("Found %s", self.picturename)
            return True
        else:
            logging.info("Did not find %s", self.picturename)
            return False

    @log
    def if_found(self, plus=True, errormsg=''):
        if self.found and plus:
            logging.info("%s was found and plus was true", self.picturename)
            return self
        else:
            logging.info("%s was not found or plus wasn't true.")
        if not errormsg:
            logging.info("no error message. Returning empty.")
            return Empty()
        else:
            logging.info("There is an error message. Raising exception.")
        raise Error(errormsg)

    @log
    def if_not_found(self, plus=True, errormsg=''):
        if not self.found and plus:
            logging.info("%s was not found and plus was true.", self.picturename)
            return self
        else:
            logging.info("%s was found or plus was not true.", self.picturename)
        if not errormsg:
            logging.info("no error message. Returning empty.")
            return Empty()
        else:
            logging.info("There is an error message. Raising exception.")
        raise Error(errormsg)

    @log
    def fail(self, errormsg, finishing=[]):
        raise Error(errormsg, finishing=finishing)

    @log
    def keywrite(self, *args):
        gi.typewrite(list(args),interval=0.2)
        return self

    @log
    def write(self, sentence):
        gi.typewrite(sentence, interval=0.2)
        return self

    @log
    def wait(self, interval):
        time.sleep(interval)
        return self

    @log
    def screenshot(self, offset=None, width=100, height=100):
        start = gi.locateOnScreen(self.url)
        x, y = start[0] + offset[0], start[1] + offset[1]
        logging.info("Final x and y is %d, %d", x, y)
        return gi.screenshot("../screen.png", region=(x, y, width, height))

    @log
    def read(self, offset=(0,0), width=100, height=100):
        img = self.screenshot(offset=offset, width=width, height=height)
        recg = str(ocr.make_recognition(img, self.ocr_key).rstrip())
        return recg
