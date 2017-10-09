import os, sys, re, time
from item_object import Item
from spooky_logs import log
from error_handling import Error
from ui import GUI_INTERFACE

class Ghost(object, GUI_INTERFACE):
    def __init__(self, ocr_key):
        self.METHODS = {}
        self.currentresults = []
        self.ocr_key = ocr_key

        directory = './'+sys.argv[0]+'/imgs' # the ./ may be a problem?
        names = os.listdir(directory)
        self.Items = {
            re.sub('(\.PNG)', '', name): Item(directory+"/"+name, self.ocr_key)
            for name in names
        }

    def __getitem__(self, key):
        return self.Items[key]

    def new_method(self):
        def wrapper(fn):
            self.METHODS[fn.__name__] = fn
            return fn
        return wrapper

    def start(self, obj, cmd):
        raise NotImplementedError("start(obj, cmd) must be implemented.")

    def fail(self, msg):
        raise Error(msg)

    def failed(self, e, obj, cmd):
        raise NotImplementedError("failed(e, obj, cmd) must be implemented")

    def completed(self, obj, cmd):
        raise NotImplementedError("completed(obj, cmd) must be implemented")

    def wait(self, interval):
        time.sleep(interval)
    @log
    def click_all(self, *args):
        for i in args:
            self[i].click()

    @log
    def wait_for_all(self, *args, **kwargs):
        theres = []
        print(theres)
        while theres != [True]*len(args):
            theres = []
            for i in args:
                theres.append(self[i].found)
            print(theres)
            print([True]*len(args))
            self.keywrite(*kwargs.get("typewrite_between", []))

    def run(self, obj=None, cmd=None, cmd_args=(), cmd_kwargs={}):
        try:
            self.start(obj, cmd)
            self.currentresults = self.METHODS[cmd](*cmd_args, **cmd_kwargs)
        except Error as e:
            self.failed(e, obj, cmd)
            self.currentresults = []
        else:
            self.completed(obj, cmd)
            self.currentresults = []

    # def run_all(filename="commands.csv", model=[]):
    #     self.
