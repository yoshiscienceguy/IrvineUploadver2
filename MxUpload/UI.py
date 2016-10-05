from gdrive import *
from Tkinter import *
from tkMessageBox import *
import ttk
import tkFileDialog
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
        try:
            self.root.iconbitmap("icons\logo.ico")
        except:
##            icon = PhotoImage(file = "icons//logo.ico")
##            self.root.tk.call("wm","iconphoto",self.root._w,icon)
            pass
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
        submit = ttk.Button(frame, text = toSay,command = functionName,width= specialWidth)
        #,borderwidth = 2,relief =RAISED,width= specialWidth)
        
        if(picName):
            photo = PhotoImage (file="ICONS//"+picName+".gif")
            submit.config(image = photo)
            return submit,photo

        else: 
            return submit
    def drawRadioButtons(self,frame,options,c = None,excluded = None,turnOn = False):
        
        var = StringVar()
        Buttons = []
        if len(options) >0:
            if(excluded == None):
                for texts, option in options:
                    rb = ttk.Radiobutton(frame, text = texts, variable = var, value = option, command = c)
                    rb.pack(side = LEFT, anchor = W,padx = 10)
                    if(not turnOn):
                        rb.selected = "Off"
                        rb['state'] = "disabled"
                    Buttons.append(rb)
                var.set(options[0][1])
                #Buttons[0].selected = "current"
            else:

                for texts, option in options:
                    if(option in excluded):
                        rb = Radiobutton(frame, text = texts, variable = var, value = option,state = "disabled")
                    else:
                        rb = Radiobutton(frame, text = texts, variable = var, value = option, command = c)
                    
                    rb.pack(side = LEFT, anchor = W,padx = 10)
                    rb.selected = "Off"
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
    def drawTextBox (self,frame,textToDisplay,bind= True):
        self.userinput = StringVar()
        self.entry = Entry(frame,textvariable = self.userinput,width = 30,justify =LEFT)
        if(bind):
            self.entry.bind("<Button-1>", lambda clicked : self.userinput.set(""))
        self.userinput.set(textToDisplay)
        return self.entry , self.userinput
    def drawDialogBox(self,frame,title):
        options = {}
        options['defaultextension'] = '.py'
        options['filetypes'] = [('Programming Files', '.py .io .txt .sb2'),('All Files', '.*')]
        osType = platform.system()
        if(osType == "Linux"):
            options['initialdir'] = "/home/pi/"
        else:
            options['initialdir'] = os.path.expanduser("~")+"/Desktop/"
        
        print(os.path.expanduser("~")+"/Desktop/")
        options['parent'] = frame
        options['title'] = 'Select file to Upload'
        
        path = tkFileDialog.askopenfilenames(**options)
        return path
    def drawComboBox(self,frame):
        varSelection = StringVar()
        comboBox = ttk.Combobox(frame,textvariable = varSelection,state = "readonly")
        return varSelection,comboBox
    def alertBox(self,title,msg):
        showinfo(title,msg)
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
