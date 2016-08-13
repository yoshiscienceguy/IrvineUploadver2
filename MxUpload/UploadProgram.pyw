#1:40 PM 8/13/2016
from UI import *
import webbrowser, os, shutil
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
        self.codeFolders = {}
        self.currentCodeFolder = ""
        self.studentLevels = {}
        self.studentProjects = {}
        self.pathData = {}
        self.IsUploadMenu = False
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
            self.updateStudentNames()
    def clearSearch(self,event):
        global search_var
        search_var.set("")
        self.searchTerm = ""
    def ChooseStudentButton(self):
        global handlers
        handlers.ChooseStudent(None)
    def ChooseStudent(self,event):
        global drive, handlers,studentList_obj,resultText_var,studLvl_objs,studLvl_var
        if(self.TypeID != ""):
            print(self.searchTerm)
            index = studentList_obj.curselection()
            if(event != None):
                self.Name = self.searchResults[index[0]]
            self.ID,dummy = drive._GetFolderInfo(self.Name,self.TypeID)
            resultText_var.set("Selected Student: " + self.Name)
            self.studentLevels = drive.GetFolders(self.ID)
            levels = sorted(self.studentLevels)
            radiobuttons = []
            for level in levels:
                radiobuttons.append((level,self.studentLevels[level]))
                codeFolder = drive.GetFolders(self.studentLevels[level])["Code"]
                self.codeFolders [self.studentLevels[level]] = codeFolder
                self.studentProjects[self.studentLevels[level]] = drive.GetAllTypes(codeFolder)
            for level in studLvl_objs:
                level.pack_forget()
            studLvl_objs,studLvl_var = menu.drawRadioButtons (studentLevelFrame,radiobuttons,c = handlers.RadioSelect)
            self.LevelID = studLvl_var.get()
            self.studentProjectsLocal = self.studentProjects[studLvl_var.get()]
            self.currentCodeFolder = self.codeFolders[studLvl_var.get()]
            studentprojects = sorted(self.studentProjectsLocal,key=lambda x: self.studentProjectsLocal[x][1],reverse=True)
            projList_obj.delete(0,END)
            
            for thing in studentprojects:
                projList_obj.insert(END,thing)
    def RadioSelect(self):
        global studLvl_var,projList_obj
        self.LevelID = studLvl_var.get()
        projList_obj.delete(0,END)
        self.currentCodeFolder = self.codeFolders[studLvl_var.get()]
        self.studentProjectsLocal = self.studentProjects[studLvl_var.get()]
        studentprojects = sorted(self.studentProjectsLocal,key=lambda x: self.studentProjectsLocal[x][1],reverse=True)
        for thing in studentprojects:
            projList_obj.insert(END,thing)
    def Upload(self):
        global menu, handlers, drive
        if(self.currentCodeFolder != ""):
            self.IsUploadMenu = True
            self.uploadWindow = Toplevel(menu.root)
            self.uploadWindow.wm_title("Upload Window")
            self.uploadbox = menu.drawLabelFrame(self.uploadWindow,"Select File(s) to Upload")
            self.filepath_obj,self.filepath_var = menu.drawTextBox(self.uploadbox,"path to file ...",False)
            self.filepath_obj.pack(side = LEFT,padx = 20,pady = 20)

            dialog_box = menu.drawButton(self.uploadbox,"...",handlers.DiagBox)
            dialog_box.pack(side = LEFT,padx = (0,10),pady = 20)
            submit_box = menu.drawButton(self.uploadbox," Upload ",handlers.UploadBatch,specialWidth = 10)
            submit_box.pack(side = LEFT,padx = 10,pady = 20)
                                                                    
            dnd = TkDND(self.uploadbox)
            dnd.bindtarget(self.filepath_obj, handlers.parseDragNDrop,"text/uri-list")

            filesFrame = Frame(self.uploadWindow)
            filesFrame.pack()
            dummy,self.totalFiles_var = menu.drawMessage(filesFrame,"0 File(s)")
            dummy.pack(side = RIGHT)
            
            m1Dummy, m2DummyVar = menu.drawMessage(filesFrame,"Files to Upload: ")
            m1Dummy.pack(side = RIGHT)
            files2Frame = Frame(self.uploadWindow)
            files2Frame.pack()
            m2Dummy, self.SelectedFiles = menu.drawMessage(files2Frame,"",color="black",fontSize= 10)
            m2Dummy.pack()
    def DiagBox(self):
        global menu,handlers
        class dummy():
            def __init__(self):
                self.data = ""
        paths = menu.drawDialogBox(self.uploadbox,"Select File")
        togo = dummy()
        for path in menu.root.tk.splitlist(paths):
            togo.data += path + " "
        handlers.parseDragNDrop(togo)
    def UploadBatch(self):
        global drive,handlers
        if(len(self.pathData) > 0 and self.currentCodeFolder != ""):
            print("Uploading")
            for files in self.pathData:
                print(self.currentCodeFolder,self.pathData[files],files)
                drive.UploadFile(self.currentCodeFolder,self.pathData[files],files)
            print("success")
            if(self.IsUploadMenu):
                self.uploadWindow.destroy()
            self.IsUploadMenu = False
            handlers.ChooseStudent(None)
            self.IsUploadMenu = False
    def parseDragNDrop(self,event):
        
        global menu, handlers
        print("hi")
        if(self.currentCodeFolder == ""):
            return
        print("yo")
        files = menu.root.tk.splitlist(event.data)
        self.pathData ={}
        toshow = ""
        displayFiles = ""
        if(self.IsUploadMenu):
            self.totalFiles_var.set(str(len(files)) + " File(s):")
        for filename in files:
            filename2 = filename.split("/")[-2:]
            self.pathData[filename2[1]] = filename
            filename = ".../"+filename2[0]+"/"+filename2[1]
            toshow += filename + " ,"
            displayFiles += filename + "\n\n"
        if(self.IsUploadMenu):
            self.SelectedFiles.set(displayFiles)
            self.filepath_var.set(toshow)
        else:
            handlers.UploadBatch()
        
    def DownloadClick(self,event):
        global handlers
        handlers.Download()
    def Download(self):
        global projList_obj,drive
        if(self.currentCodeFolder != "" and len(projList_obj.curselection()) > 0):
            print("downloading")
            fileName = projList_obj.get(ACTIVE)
            fileID,fileStamp = self.studentProjects[self.LevelID][fileName]
            drive.DownloadFile (fileID,fileName)
            userhome = os.path.expanduser('~')
            desktop = userhome + '\\Desktop\\'
            if os.path.exists(desktop+fileName):
                os.remove(desktop+fileName)
            shutil.move(fileName,desktop)
    def TechnicalReport(self):
        global projList_obj,drive,studLvl_var
        if(self.currentCodeFolder != "" and len(projList_obj.curselection()) > 0):
            print("Opening TechReport")
            fileName = projList_obj.get(ACTIVE)
            fileName = fileName.split(".")[0] + " Report"
            TechFolder = drive.GetFolders(studLvl_var.get())["Documents"]
            url = drive.CopyTechnicalReport(TechFolder,self.TypeName,fileName)
            webbrowser.open(url)
            
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
       
selectStudent = menu.drawButton(studentNamesFrame,"Select",handlers.ChooseStudentButton)
selectStudent.pack(side = RIGHT,pady = (0,5),padx = 20)

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
projList_obj.bind("<Double-Button-1>",handlers.DownloadClick)
projects_frame.pack(fill = BOTH,padx = 20,pady = 20) 
dnd = TkDND(projects_frame)
dnd.bindtarget(projList_obj, handlers.parseDragNDrop,"text/uri-list")
 
#Fifth Frame
action = menu.drawLabelFrame(middlePart,"What do you want to do?")
ButtonsFrame = Frame(action)
ButtonsFrame.pack(fill = BOTH,expand = 1)
uploadButton = menu.drawButton(ButtonsFrame,"Upload",handlers.Upload)
uploadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10,anchor = W,expand = 1)
downloadButton = menu.drawButton(ButtonsFrame,"Download",handlers.Download)
downloadButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10,expand = 1)
techreportButton = menu.drawButton(ButtonsFrame,"Technical Report",handlers.TechnicalReport,specialWidth= 15)
techreportButton.pack(side = LEFT,padx = 20, pady = 10,ipadx = 10, anchor = E,expand = 1)
menu.root.mainloop()
