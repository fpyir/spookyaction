
class ItemNotThere(Exception):
    def __init__(self, itemobj):
        context = "Could not find item named {} with image {}".format(
            str(itemobj), itemobj.picturename
        )
        Exception.__init__(self, context)
        self.itemobj = itemobj

class ItemNeverAppeared(Exception):
    def __init__(self, itemobj, funcname):
        context = "Was going to activate function named {} from item {} with \
                   image {}, but it never appeared.".format(
            funcname, str(itemobj), itemobj.picturename
        )
        Exception.__init__(self, context)
        self.itemobj = itemobj

class Error(Exception):
    def __init__(self, errorlogs, finishing=[]):
        Exception.__init__(self, errorlogs)
        self.logs = errorlogs
        self.finishing = finishing
