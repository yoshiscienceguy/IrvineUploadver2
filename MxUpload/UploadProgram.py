from UI import *
from libs.tkdndWrapper import TkDND
class Handlers():
    def __init__(self):
        self.TypeID = ""
        self.TypeName = ""
        self.ID = ""
        self.Name = ""

        self.LevelID = ""
        
        self.studentNamesIds = {}
        
        self.searchTerm = ""
        self.searchTermProj = ""

        self.studentNamesLocal = []
        self.studentProjectsLocal = []
        
        self.searchResults = []
        
        self.studentLevels = {}
        self.studentProjects = {}
        
    def defineStudentType(self,*args):
        global dropDown_var,drive,search_var
        self.TypeName = dropDown_var.get()
        self.TypeID,dummy = drive._GetFolderInfo(self.TypeName,drive.ids.StudentFolder)
        #print(self.TypeID)
        self.clearSearch(None)
        search_var.set("Enter name...")
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
        self.searchResults = []
        for thing in self.studentNamesLocal:
            if(not "_" in thing):
                if(self.searchTerm == "" or self.searchTerm.lower() in thing.lower()):
                    studentList_obj.insert(END,thing)
                    self.searchResults.append(thing)
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
    def ChooseStudent(self,event):
        global drive, handlers,studentList_obj,resultText_var,studLvl_objs,studLvl_var
        if(self.TypeID != ""):
            index = studentList_obj.curselection()
            self.Name = self.searchResults[index[0]]
            self.ID,dummy = drive._GetFolderInfo(self.Name,self.TypeID)
            resultText_var.set("Selected Student: " + self.Name)
            self.studentLevels = drive.GetFolders(self.ID)
            levels = sorted(self.studentLevels)
            radiobuttons = []
            for level in levels:
                radiobuttons.append((level,self.studentLevels[level]))
                codeFolder = drive.GetFolders(self.studentLevels[level])["Code"]
                self.studentProjects[self.studentLevels[level]] = drive.GetAllTypes(codeFolder)

            for level in studLvl_objs:
                level.pack_forget()
            studLvl_objs,studLvl_var = menu.drawRadioButtons (studentLevelFrame,radiobuttons,c = handlers.RadioSelect)
            self.LevelID = studLvl_var.get()
            self.studentProjectsLocal = self.studentProjects[studLvl_var.get()]
            studentprojects = sorted(self.studentProjectsLocal,key=lambda x: self.studentProjectsLocal[x][1],reverse=True)
            projList_obj.delete(0,END)
            
            for thing in studentprojects:
                projList_obj.insert(END,thing)
    def RadioSelect(self):
        global studLvl_var,projList_obj
        self.LevelID = studLvl_var.get()
        projList_obj.delete(0,END)
        self.studentProjectsLocal = self.studentProjects[studLvl_var.get()]
        studentprojects = sorted(self.studentProjectsLocal,key=lambda x: self.studentProjectsLocal[x][1],reverse=True)
        for thing in studentprojects:
            projList_obj.insert(END,thing)
    def Upload(self):
        global menu, handlers
        uploadWindow = Toplevel(menu.root)
        uploadWindow.wm_title("Upload Window")
        lb = Listbox(uploadWindow,width = 50)
        lb.pack(fill="both", expand = 1)

        dnd = TkDND(uploadWindow)
        dnd.bindtarget(lb, handlers.TestHook,"text/uri-list")
    def Download(self):
        global projList_obj
        if(self.LevelID != "" and len(projList_obj.curselection()) > 0):
            print("downloading")
    def TestHook(self,*args):
        print(args) 
#programNames = ["Codologie","Buildologie","Gamologie","K-12 STEM Club","Camps"]

drive = Drive()
menu = Menu()
handlers = Handlers()

startLevels = [("Beginner I","Beginner I"),("Intermediate II","Intermediate II"),("Advanced III","Advanced III")]
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
searchFrame.pack(fill = BOTH,pady=(20,0))

search_obj, search_var = menu.drawTextBox(searchFrame,"Enter name...")
#search_obj.focus_set()
search_obj.bind("<Key>",handlers.search)
search_obj.bind("<Button-1>",handlers.clearSearch)
search_obj.pack(side = RIGHT,padx = (5,20))

searchText_obj,searchText_var = menu.drawMessage(searchFrame,"Search Name: ",color ="black")
searchText_obj.pack(side=RIGHT)

resultFrame = Frame(studentNames)
resultFrame.pack(fill = BOTH,pady=(20,0))
resultText_obj,resultText_var = menu.drawMessage(resultFrame,"Selected Student: ")
resultText_obj.pack(side = LEFT,padx = 20)

studentNamesFrame = Frame(studentNames)
studentNamesFrame.pack(fill = BOTH)

students_frame,studentList_obj = menu.drawMenu(studentNamesFrame,[])
studentList_obj.bind("<Double-Button-1>",handlers.ChooseStudent)
students_frame.pack(fill = BOTH,padx = 20,pady = 20)            


#Third Frame
studentInfo = menu.drawLabelFrame(middlePart,"Student Information")
studentLevelFrame = Frame(studentInfo)
studLvl_objs,studLvl_var = menu.drawRadioButtons (studentLevelFrame,startLevels,c = handlers.RadioSelect)
studentLevelFrame.pack()
#Fourth Frame
projects = menu.drawLabelFrame(middlePart,"Select Project")

projectNamesFrame = Frame(projects)
projectNamesFrame.pack(fill = BOTH)

projects_frame,projList_obj = menu.drawMenu(projectNamesFrame,[])
projList_obj.bind("<Double-Button-1>",handlers.TestHook)
projects_frame.pack(fill = BOTH,padx = 20,pady = 20) 

#Fifth Frame
action = menu.drawLabelFrame(middlePart,"What do you want to do?")
ButtonsFrame = Frame(action)
ButtonsFrame.pack(fill = BOTH,expand = 1)
uploadButton = menu.drawButton(ButtonsFrame,"Upload",handlers.Upload)
uploadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10,anchor = W,expand = 1)
downloadButton = menu.drawButton(ButtonsFrame,"Download",handlers.Download)
downloadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10,expand = 1)
techreportButton = menu.drawButton(ButtonsFrame,"Technical Report",handlers.TestHook,specialWidth= 15)
techreportButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10, anchor = E,expand = 1)
menu.root.mainloop()
