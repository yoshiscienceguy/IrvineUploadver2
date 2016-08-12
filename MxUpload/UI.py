from gdrive import *
from Tkinter import *

def TestConnection():
    try:
        response = urllib2.urlopen("http://www.google.com",timeout=1)
    except:
        print("You Don't Have an Active Internet Connection")
        print("Please ask a Mentor for HELP")
        quit()

class Menu():
    def __init__(self):
        self.root = Tk()
        #self.handlers = Handlers()
        self.root.iconbitmap("icons\logo.ico")
        self.root.minsize(400,200)
        self.root.maxsize(600,900)
        self.root.title("Google Drive Upload")
        
    def drawDropDown(self,frame,functionName,listDisplay):
        AssociatedVariable = StringVar(frame)
        AssociatedVariable.set("Select One")
        AssociatedVariable.trace("w",functionName)
        DropDown = apply(OptionMenu,(frame,AssociatedVariable)+tuple(listDisplay))

        #DropDown.pack(pady=(10,0))

        return DropDown , AssociatedVariable
    
    def drawButton(self,frame,toSay,functionName,specialWidth = 5,picName = None):
        submit = Button(frame, text = toSay,command = functionName,borderwidth = 2,relief =RAISED,width= specialWidth)
        
        if(picName):
            photo = PhotoImage (file="ICONS//"+picName+".gif")
            submit.config(image = photo)
            return submit,photo

        else: 
            return submit
    def drawRadioButtons(self,frame,options,c = None,excluded = None):
        
        var = StringVar()
        Buttons = []
        if len(options) >0:
            if(excluded == None):
                for texts, option in options:
                    rb = Radiobutton(frame, text = texts, variable = var, value = option, command = c)
                    rb.pack(side = LEFT, anchor = W,padx = 10)
                    rb.deselect()
                    Buttons.append(rb)
                var.set(options[1][1])
            else:

                for texts, option in options:
                    if(option in excluded):
                        rb = Radiobutton(frame, text = texts, variable = var, value = option,state = "disabled")
                    else:
                        rb = Radiobutton(frame, text = texts, variable = var, value = option, command = c)
                    
                    rb.pack(side = LEFT, anchor = W,padx = 10)
                    rb.deselect()
                    Buttons.append(rb)
                var.set(options[0][1])
        
        
        return Buttons , var
    def drawMenu(self,frame,listDisplay,NewOption = False):
        f = Frame(frame,bd = 2, relief = SUNKEN)
        scrollbar = Scrollbar(f,orient = VERTICAL)
        listbox = Listbox(f,yscrollcommand = scrollbar.set,width = 30)
        scrollbar.config(command = listbox.yview)
        

        if(NewOption):
            listbox.insert(END,"(create New)")
        for item in listDisplay:
            listbox.insert(END,item)
        
        scrollbar.pack(side = RIGHT, fill = Y)
        listbox.pack(fill = BOTH)
        return (f,listbox)
    def drawLabelFrame(self,frame,toSay):
        labelframe = LabelFrame(frame, text = toSay)
        labelframe.pack(fill = "both",expand = "yes")
        return labelframe
    def drawMessage(self,frame,toSay,color = "red",fontSize = 10):
        vartoSay = StringVar()
        textbox = Label(frame,textvariable = vartoSay, fg = color,font = ("Helvetica",fontSize))
        vartoSay.set(toSay)

        #textbox.pack(pady = 10,)
        return textbox,vartoSay
    def drawTextBox (self,frame,textToDisplay):
        self.userinput = StringVar()
        self.entry = Entry(frame,textvariable = self.userinput,width = 30,justify =LEFT)
        self.entry.bind("<Button-1>", lambda clicked : self.userinput.set(""))
        self.userinput.set(textToDisplay)
        return self.entry , self.userinput
 
##menu = Menu()
##handlers = Handlers()
##menu.drawDropDown(menu.root,"handlers.TestHook",["hi","bye","yolo"])
##menu.drawButton(menu.root,"testing","handlers.TestHook")
##menu.drawRadioButtons(menu.root,[("juan","mexico"),("tito","cuba"),("pancho","panama")])
##menu.drawMenu(menu.root,["California","Nevada","New York"])
##menu.drawMessage(menu.root,"lol")
##menu.drawTextBox(menu.root,"Enter Something")
##
##menu.root.mainloop()
