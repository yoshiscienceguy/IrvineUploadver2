from gdrive import *
from Tkinter import *

def TestConnection():
    try:
        response = urllib2.urlopen("http://www.google.com",timeout=1)
    except:
        print("You Don't Have an Active Internet Connection")
        print("Please ask a Mentor for HELP")
        quit()
def TestHook(*args):
    print(args)
class Menu():
    def __init__(self):
        self.root = Tk()
        self.root.iconbitmap("icons\logo.ico")
        self.root.minsize(400,200)
        self.root.maxsize(400,700)
        self.root.title("Google Drive Upload")
        
    def drawDropDown(self,frame,functionName,listDisplay):
        AssociatedVariable = StringVar(frame)
        AssociatedVariable.set("Select One")
        AssociatedVariable.trace("w",eval(functionName))
        DropDown = apply(OptionMenu,(frame,AssociatedVariable)+tuple(listDisplay))
        DropDown.pack(pady=(10,0))

        return DropDown , AssociatedVariable
    
menu = Menu()
menu.drawDropDown(menu.root,"TestHook",["hi","bye","yolo"])

menu.root.mainloop()
