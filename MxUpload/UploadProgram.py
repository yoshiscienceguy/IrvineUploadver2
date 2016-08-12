from UI import *
class Handlers():
    def __init__(self):
        self.TypeID = ""
        self.TypeName = ""
        self.ID = ""
        self.Name = ""
        self.LevelID = ""
        self.LevelName = ""
        self.searchTerm = ""
        self.studentNamesIds = {}
        self.studentNamesLocal = []
    def defineStudentType(self,*args):
        global dropDown_var,drive,search_var
        self.TypeName = dropDown_var.get()
        self.TypeID,dummy = drive._GetFolderInfo(self.TypeName,drive.ids.StudentFolder)
        #print(self.TypeID)
        self.clearSearch(None)
        search_var.set("Search...")
        self.getStudentNames()
    def getStudentNames(self):
        global drive,studentList_obj
        self.studentNamesIds = drive.GetFolders(self.TypeID)
        self.studentNamesLocal = sorted(self.studentNamesIds.keys())
        studentList_obj.delete(0,END)
        
        for thing in self.studentNamesLocal:
            if(not "_" in thing):
                if(self.searchTerm == "" or self.searchTerm in thing):
                    studentList_obj.insert(END,thing)
    def updateStudentNames(self):
        global studentList_obj
        studentList_obj.delete(0,END)
        for thing in self.studentNamesLocal:
            if(not "_" in thing):
                if(self.searchTerm == "" or self.searchTerm.lower() in thing.lower()):
                    studentList_obj.insert(END,thing)
    def search(self,event):
        global search_var
        if(self.searchTerm == ""):
            search_var.set("")
        if(self.TypeID != ""):
            if(not event.keycode in [8]):
                self.searchTerm += str(event.char)
            else:
                self.searchTerm = self.searchTerm[:-1]
            print(self.searchTerm)
            self.updateStudentNames()
        
            
    def clearSearch(self,event):
        global search_var
        search_var.set("")
        self.searchTerm = ""
    def TestHook(self,*args):
        print(args) 
#programNames = ["Codologie","Buildologie","Gamologie","K-12 STEM Club","Camps"]

drive = Drive()
menu = Menu()
handlers = Handlers()

topPart = Frame(menu.root,width = 300)
topPart.pack()
middlePart = Frame(menu.root,width = 300)
middlePart.pack(fill = BOTH,padx = 20, pady = 20)
bottomPart = Frame(menu.root,width = 300)
bottomPart.pack()

menu.drawMessage(topPart,"Welcome to MxUpload Program",fontSize = 20)

#Get Official Names on Drive
programNames = drive.GetFolders(drive.ids.StudentFolder).keys()

#First Frame
studentType = menu.drawLabelFrame(middlePart,"Student Type")
textBox_obj,textBox_var = menu.drawMessage(studentType,"Type: ",color = "black")
textBox_obj.pack(side = LEFT,padx = 20)
dropDown_obj,dropDown_var = menu.drawDropDown(studentType,handlers.defineStudentType,programNames)
dropDown_obj.pack(side = LEFT,padx = (20,5), pady = 20)


#Second Frame
studentNames = menu.drawLabelFrame(middlePart,"Student Names")
searchFrame = Frame(studentNames)

searchFrame.pack(fill = BOTH)
search_obj, search_var = menu.drawTextBox(searchFrame,"Search...")
#search_obj.focus_set()
search_obj.bind("<Key>",handlers.search)
search_obj.bind("<Button-1>",handlers.clearSearch)
search_obj.pack(side = RIGHT,padx = 20)
studentNamesFrame = Frame(studentNames)
studentNamesFrame.pack(fill = BOTH)
students_frame,studentList_obj = menu.drawMenu(studentNamesFrame,[],NewOption=True)
students_frame.pack(fill = BOTH,padx = 20,pady = 20)            

#Get Avaliable Levels

#Third Frame
studentInfo = menu.drawLabelFrame(middlePart,"Student Information")
studentLevelFrame = Frame(studentInfo)
studLvl_obj,studLvl = menu.drawRadioButtons (studentLevelFrame,[("Beginner I","Beginner I"),
                                                                 ("Intermediate II","Intermediate II"),
                                                                ("Advanced III","Advanced III")])
studentLevelFrame.pack()

#Fourth Frame
action = menu.drawLabelFrame(middlePart,"What do you want to do?")
uploadButton = menu.drawButton(action,"Upload",handlers.TestHook)
uploadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10)
downloadButton = menu.drawButton(action,"Download",handlers.TestHook)
downloadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10)
techreportButton = menu.drawButton(action,"Technical Report",handlers.TestHook,specialWidth= 15)
techreportButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10)
menu.root.mainloop()
