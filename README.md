
# SpookyAction
SpookyAction is a **Python** framework for desktop automation - it takes a configuration-based approach to utilising the PyAutoGUI. At the core of the framework is the `Item` class. It uses the concept of silent chaining to make writing automated flows quick and simple. 

SpookyAction is currently in early alpha, with a huge number of features to be written, things to be refactored and issues to be squashed. The ultimate goal is to create a simplistic, high level way to automate flows across both desktop interactions, API calls and Headless browser usage.

For the moment it is strongly advised that you **do not use this in real world projects.**.


### Basic Usage 
1. Create a directory with the following structure:
   ```
   __main__.py
   helpers.py
   methods.py
   imgs/
   ```
2. In `imgs/` put all your image files to be turned into Item's.
3. In `helpers.py` you want to define functions to be used by your code, but not directly by the user. 
4. In `methods.py` you want to define and then register functions to be used by your user. You must also registrer START, COMPLETED, and FAILED functions. Trival Example of registering a command:
    ```
    from spookyaction import *
    from helpers import *
    @new_method("bake-pie")
    def make_a_pie(acceptETC=False):
      menu_select(6, 9, errormsg='we ran out of pie') # a helper function defined in helpers.py
      Items["BakePieButton"].click()
      Items["TextMSGField"].click().write("We made your pie.").typewrite("tab","shift","enter")
      return ["Pie was created successfully"]
    ```
5. In `__main__.py` write your custom logic for invoking `spookyaction.run()`.


### Basic Item API 
Bare in mind I can make no guarantees as to if any of those works correctly while spookyaction is below v0.1.0
```python 
clickbox = Item("path/to/clickbox.png")

# a lag tolerant way to locate and then click on the Item's center with optional offsets.
clickbox.click(offx=0, offy=0)

# execute a given function when the Item is found on screen. 
# Lags out after roughly a minute, give or take a bit.
clickbox.run_when_present(given_function, arg1, arg2, kwarg1=None, kwarg2="Hi")

# a static method to execute click on all given Item names sequentially. 
# Works from the spookyaction-specific Items dictionary. 
Item.click_all("clickbox", "userprofile", "deletebutton")

# a property that returns whether an Item is on screen or not. 
clickbox.found # => True or False, dynamically computed. 

# silent-chaining function. best described by the source code. 
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
    
# silent-chaining function that works in the exact reverse of if_found
clickbox.if_not_found().fail("Oh F****")

# automatically raises the custom Error exception used for failure handling in spookyaction. 
clickbox("Error Message")

# type individual keys in
clickbox.typewrite("tab", "enter", "shift")

# write a sentence as a whole 
clickbox.write("how are you today?")

# take a screenshot and save it. 
clickbox.screenshot(offset=(5,10), width=50, height=100)

# read using the Google Cloud OCR. Not working currently.
clickbox.read(offset=(50,100), width=100, height=50) # => returns a string of the characters read off the screenshot.

```
