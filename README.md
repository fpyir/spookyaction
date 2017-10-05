
# SpookyAction
SpookyAction is a **Python** framework for desktop automation - it takes a configuration-based approach to utilising the PyAutoGUI. At the core of the framework is the `Item` class. It uses the concept of silent chaining to make writing automated flows quick and simple. 

SpookyAction is currently in early alpha, with a huge number of features to be written, things to be refactored and issues to be squashed. The ultimate goal is to create a simplistic, high level way to automate flows across both desktop interactions, API calls and Headless browser usage.

For the moment it is strongly advised that you **do not use this in real world projects.**.


### Basic Usage 
1. Create a directory with the following structure:
   ```
   __main__.py
   ghost.py
   methods.py
   imgs/
   ```
2. In `imgs/` put all your image files to be turned into Item's.
3. In `ghost.py` you want to define and initialise your subset of the `Ghost` class.
4. In `methods.py` you want to define and then register functions to be used by your user, plus your own helper functions.
    ```
    from ghost import MyGhost
    @MyGhost.new_method()
    def make_a_pie(acceptETC=False):
      menu_select(6, 9, errormsg='we ran out of pie') # a helper function defined in helpers.py
      MyGhost["BakePieButton"].click()
      MyGhost["TextMSGField"].click().write("We made your pie.").typewrite("tab","shift","enter")
      return ["Pie was created successfully"]
    ```
5. In `__main__.py` write your custom logic for invoking `MyGhost.run()`.

## Basic Ghost API
```
from spookyaction import Ghost
class MyGhostClass(Ghost):
   def start(self, obj, cmd):
      ...
      
   def failed(self, e, obj, cmd):
      ...
   
   def completed(obj, cmd):
      ...

MyGhost = MyGhostClass(ocr_key="........") # needs an OCR engine key from Google Cloud if you want to use .read()
MyGhost["piebutton"] # => Item("piebutton")
MGhost.click_all("piebutton", ...) # => clicks all
MyGhost.wait_on("pieloading", ...) # => waits for all 
MyGhost.typewrite("enter") # the Ghost class is a subclass of the UIInterface class, and can be used to access pyautogui.
```

### Basic Item API 
Bear in mind I can make no guarantees as to if any of those works correctly while spookyaction is below v0.1.0
```python 
clickbox = Item("path/to/clickbox.png")

# a lag tolerant way to locate and then click on the Item's center with optional offsets.
clickbox.click(offx=0, offy=0)

# execute a given function when the Item is found on screen. 
# Lags out after roughly a minute, give or take a bit.
clickbox.run_when_present(given_function, arg1, arg2, kwarg1=None, kwarg2="Hi")

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
## Roadmap
| Feature Name         | Feature Description                                                | Status        | Version Number |
| -------------------  | ------------------------------------------------------------------ | ------------: | -------------: |
| Push out v0.1.0      | Make sure all Item methods work as well as the MVP framework.      | COMPLETED     | V0.1.0         |
| Get OCR Working      | Implement capturing of your Google Cloud Key -> .read() will work. | COMPLETED     | V0.2.0         | 
| Run from CSV         | Add a method for running the automator based off a CSV + Model.    | IN THE FUTURE | V0.3.0         |
| Static Items         | Support for marking items as static, and caching their positions.  | IN THE FUTURE | V0.4.0         |
| Full PyAutoGUI Args  | Ability to use all PyAutoGUI keyword arguments conveniently.       | IN THE FUTURE | V0.5.0         |
| Specific Error.      | Extensive support for a variety of errors + better error handling  | IN THE FUTURE | V0.6.0         |
| Raw PyAutoGUI Wrapper| Turn ui class into a complete convienence wrapper for pyautogui    | IN THE FUTURE | V0.7.0         |
