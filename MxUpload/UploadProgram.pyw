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
        global dropDown_var,drive,search_var,studentsList_var
        self.__init__()
        self.TypeName = dropDown_var.get()
        self.TypeID,dummy = drive._GetFolderInfo(self.TypeName,drive.ids.StudentFolder)
        #print(self.TypeID)
        self.clearSearch(None)
        studentsList_var.set("Select Student Name")
        search_var.set("Enter name...")
        resultText_var.set("Selected Student: " + self.Name)
        self.getStudentNames()
        search_obj['state'] = 'normal'
        selectStudent['state']='normal'
        studentList_obj['state']='normal'
    def getStudentNames(self):
        global drive,studentList_obj
        self.studentNamesIds = drive.GetFolders(self.TypeID)
        self.studentNamesLocal = sorted(self.studentNamesIds.keys())
        studentList_obj['values'] = self.studentNamesLocal
        
##        studentList_obj.delete(0,END)
##        
##        for thing in self.studentNamesLocal:
##            if(not "_" in thing):
##                if(self.searchTerm == "" or self.searchTerm in thing):
##                    studentList_obj.insert(END,thing)
    def updateStudentNames(self):
        global studentList_obj,studentsList_var
        studentList_obj.delete(0,END)
        self.searchResults = []
        listToShow = []
        if(self.searchTerm != ""):
            for thing in self.studentNamesLocal:
                if(not "_" in thing):
                    if(self.searchTerm == "" or self.searchTerm.lower() in thing.lower()):
                        #studentList_obj.insert(END,thing)
                        listToShow.append(thing)
                        self.searchResults.append(thing)
        else:
            listToShow = self.studentNamesLocal
        studentList_obj['values'] = listToShow
        if(len(listToShow) > 0):
            studentsList_var.set(listToShow[0])
    def search(self,event):
        global search_var
        if(self.searchTerm == ""):
            search_var.set("")
            
        if(self.TypeID != ""):
            if(not event.keycode in [8]):
                if(event.keycode != 13):
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
        global drive, handlers,studentList_obj,studentsList_var,resultText_var,studLvl_objs,studLvl_var
        if(self.TypeID != ""):
            if(self.searchTerm == ""):
                self.searchResults = self.studentNamesLocal
            index = studentList_obj.current()
            if(event != None):
                self.Name = self.searchResults[index]
            else:
                self.Name = studentList_obj.get()

            #ui.root.config(cursor = "wait")
            #ui.root.update()
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
            studLvl_objs,studLvl_var = ui.drawRadioButtons (studentLevelFrame,radiobuttons,c = handlers.RadioSelect,turnOn = True)
            self.LevelID = studLvl_var.get()
            self.studentProjectsLocal = self.studentProjects[studLvl_var.get()]
            self.currentCodeFolder = self.codeFolders[studLvl_var.get()]
            studentprojects = sorted(self.studentProjectsLocal,key=lambda x: self.studentProjectsLocal[x][1],reverse=True)
            projList_obj.delete(0,END)
            i = 0
            for thing in studentprojects:
                projList_obj.insert(END,thing)
                if( i % 2 == 0):
                    projList_obj.itemconfigure(i, background='#f0f0ff')
                i += 1
            #ui.root.config(cursor = "")
            #ui.root.update()
            uploadButton['state']='normal'
            downloadButton['state']='normal'
            techreportButton['state']='normal'
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
        global ui, handlers, drive
        if(self.currentCodeFolder != ""):
            self.IsUploadMenu = True
            self.uploadWindow = Toplevel(ui.root)
            self.uploadWindow.wm_title("Upload Window")
            self.uploadbox = ui.drawLabelFrame(self.uploadWindow,"Select File(s) to Upload")
            self.filepath_obj,self.filepath_var = ui.drawTextBox(self.uploadbox,"path to file ...",False)
            self.filepath_obj.pack(side = LEFT,padx = (20,0),pady = 20)

            dialog_box = ui.drawButton(self.uploadbox,"Browse...",handlers.DiagBox,specialWidth = 15)
            dialog_box.pack(side = LEFT,padx = (0,20),pady = 20)

            self.frame1 = Frame(self.uploadWindow)
            self.frame1.pack()
            submit_box = ui.drawButton(self.frame1," Upload ",handlers.UploadBatch,specialWidth = 15)
            submit_box.pack(side = BOTTOM,padx = 10,pady = 20)
                                                                    
            dnd = TkDND(self.uploadbox)
            dnd.bindtarget(self.filepath_obj, handlers.parseDragNDrop,"text/uri-list")

            filesFrame = Frame(self.uploadWindow)
            filesFrame.pack()
            dummy,self.totalFiles_var = ui.drawMessage(filesFrame,"0 File(s)")
            dummy.pack(side = RIGHT)
            
            m1Dummy, m2DummyVar = ui.drawMessage(filesFrame,"Files to Upload: ")
            m1Dummy.pack(side = RIGHT)
            files2Frame = Frame(self.uploadWindow)
            files2Frame.pack()
            m2Dummy, self.SelectedFiles = ui.drawMessage(files2Frame,"",color="black",fontSize= 10)
            m2Dummy.pack()
            
    def DiagBox(self):
        global ui,handlers
        class dummy():
            def __init__(self):
                self.data = ""
        paths = ui.drawDialogBox(self.uploadbox,"Select File")
        print(paths)
        togo = dummy()
        for path in paths:#ui.root.tk.splitlist(paths):
            if " " in path:
                togo.data += "{"+path+"} "
            else:
                togo.data+= path+" "
        handlers.parseDragNDrop(togo)
    def UploadBatch(self):
        global drive,handlers
        if(len(self.pathData) > 0 and self.currentCodeFolder != ""):
           
            for files in self.pathData:
                print(self.currentCodeFolder,self.pathData[files],files)
                drive.UploadFile(self.currentCodeFolder,self.pathData[files],files)
            if(self.IsUploadMenu):
                self.uploadWindow.destroy()
            self.IsUploadMenu = False
            handlers.ChooseStudent(None)
            self.IsUploadMenu = False
            ui.alertBox("Sucess","Upload Complete!")
    def parseDragNDrop(self,event):
        
        global ui, handlers
        if(self.currentCodeFolder == ""):
            return
        print("data")
        print(event.data)
        files = ui.root.tk.splitlist(event.data)
        self.pathData ={}
        toshow = ""
        displayFiles = ""
        if(self.IsUploadMenu):
            self.totalFiles_var.set(str(len(files)) + " File(s):")
        print(files)
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
            useros = platform.system()
            if(useros== "Windows"):
                userhome = os.path.expanduser('~')
                
                desktop = userhome + '\\Desktop\\'
            else:
                desktop = "/home/pi/Desktop/"
            print(desktop)
            if os.path.exists(desktop+fileName):
                os.remove(desktop+fileName)
            shutil.move(fileName,desktop)
            ui.alertBox("Sucess","Download Complete \n Look for it on the Desktop")
    def TechnicalReport(self):
        global projList_obj,drive,studLvl_var
        if(self.currentCodeFolder != "" and len(projList_obj.curselection()) > 0):
            print("Opening TechReport")
            fileName = projList_obj.get(ACTIVE)
            fileName = fileName.split(".")[0] + " Report"
            TechFolder = drive.GetFolders(studLvl_var.get())["Documents"]
            url,TechId = drive.CopyTechnicalReport(TechFolder,self.TypeName,fileName)
            url = url.encode('ascii','ignore')
            
            useros = platform.system()
            if(useros== "Windows"):
                answer = webbrowser.open(url)
                ui.alertBox("Sucess","Now Opening")
            else:
                drive.DownloadTechnicalReport(TechId,fileName)
                filename = fileName.encode('ascii','ignore')+".odt"
                desktop = "/home/pi/Desktop/"
                if os.path.exists(desktop+filename):
                    os.remove(desktop+filename)
                shutil.move(filename,desktop)
                os.system("libreoffice --writer {}".format(filename))
                
                
            print("done ")
    def TestHook(self,*args):
        print(args) 
#programNames = ["Codologie","Buildologie","Gamologie","K-12 STEM Club","Camps"]

drive = Drive()
ui = UI()
handlers = Handlers()

startLevels = [("Beginner I","Beginner I"),("Intermediate II","Intermediate II"),("Advanced III","Advanced III")]
topPart = Frame(ui.root,width = 300)
topPart.pack()
middlePart = Frame(ui.root,width = 300)
middlePart.pack(fill = BOTH,padx = 20, pady = 20)
bottomPart = Frame(ui.root,width = 300)
bottomPart.pack()

ui.drawMessage(topPart,"Welcome to MxUpload Program",fontSize = 20)

#Get Official Names on Drive
programNames = drive.GetFolders(drive.ids.StudentFolder).keys()

#Menu
def hello():
    ui.alertBox("Sucess","None yet")
    
#MenuBar
menubar = Menu(topPart)



filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label="Preferences", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=ui.root.destroy)

editmenu = Menu(menubar,tearoff=0)
editmenu.add_command(label="Update Program", command=hello)
editmenu.add_separator()
editmenu.add_command(label="Create Student", command=ui.root.quit)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
ui.root.config(menu=menubar)

#First Frame
studentType = ui.drawLabelFrame(middlePart,"Student Type")
textBox_obj,textBox_var = ui.drawMessage(studentType,"Type: ",color = "black")
textBox_obj.pack(side = LEFT,padx = 20)
#dropDown_obj,dropDown_var = ui.drawDropDown(studentType,handlers.defineStudentType,programNames)
dropDown_var,dropDown_obj = ui.drawComboBox(studentType)
dropDown_var.set("Select Student Type")
dropDown_obj.bind('<<ComboboxSelected>>',handlers.defineStudentType)
dropDown_obj['values'] = programNames
dropDown_obj.pack(side = LEFT,padx = (20,5), pady = 20)


#Second Frame
studentNames = ui.drawLabelFrame(middlePart,"Student Names")
searchFrame = Frame(studentNames)
searchFrame.pack(fill = BOTH,pady=(20,0))

search_obj, search_var = ui.drawTextBox(searchFrame,"Enter name...")
#search_obj.focus_set()
search_obj['state'] = 'disabled'
search_obj.bind("<Key>",handlers.search)
search_obj.bind("<Button-1>",handlers.clearSearch)
search_obj.pack(side = RIGHT,padx = (5,20))

searchText_obj,searchText_var = ui.drawMessage(searchFrame,"Search Name: ",color ="black")
searchText_obj.pack(side=RIGHT)

resultFrame = Frame(studentNames)
resultFrame.pack(fill = BOTH,pady=(20,0))
resultText_obj,resultText_var = ui.drawMessage(resultFrame,"Selected Student: ")
resultText_obj.pack(side = LEFT,padx = 20)


studentNamesFrame = Frame(studentNames)
studentNamesFrame.pack(fill = BOTH)

#students_frame,studentList_obj = ui.drawMenu(studentNamesFrame,[])
studentsList_var,studentList_obj = ui.drawComboBox(studentNamesFrame)
studentList_obj.bind('<<ComboboxSelected>>',handlers.ChooseStudent)
#studentList_obj.bind("<Double-Button-1>",handlers.ChooseStudent)
studentList_obj.pack(fill = BOTH,padx = 20,pady = 20)  
#students_frame.pack(fill = BOTH,padx = 20,pady = 20)            
studentList_obj['state']='disabled'

selectStudent = ui.drawButton(studentNamesFrame,"Select",handlers.ChooseStudentButton,specialWidth= 15)
selectStudent.pack(side = RIGHT,pady = (0,5),padx = 20)
selectStudent['state']='disabled'
#Third Frame
studentInfo = ui.drawLabelFrame(middlePart,"Student Information")
studentLevelFrame = Frame(studentInfo)
studLvl_objs,studLvl_var = ui.drawRadioButtons (studentLevelFrame,startLevels,c = handlers.RadioSelect)
studentLevelFrame.pack()
#Fourth Frame
projects = ui.drawLabelFrame(middlePart,"Select Project")

projectNamesFrame = Frame(projects)
projectNamesFrame.pack(fill = BOTH,side = LEFT)

projects_frame,projList_obj = ui.drawMenu(projectNamesFrame,[])
projList_obj.bind("<Double-Button-1>",handlers.DownloadClick)
projects_frame.pack(fill = BOTH,padx = 20,pady = 20) 
dnd = TkDND(projects_frame)
dnd.bindtarget(projList_obj, handlers.parseDragNDrop,"text/uri-list")
 
#Fifth Frame
#action = ui.drawLabelFrame(middlePart,"What do you want to do?")
action = Frame(projects)
action.pack(fill = BOTH,side = LEFT,pady=(30,0))
ButtonsFrame = Frame(action)
ButtonsFrame.pack(fill = BOTH,expand = 1)
uploadButton = ui.drawButton(ButtonsFrame,"Upload",handlers.Upload,specialWidth= 10)
uploadButton.pack(padx = 20, pady = 10,ipadx = 10)
downloadButton = ui.drawButton(ButtonsFrame,"Download",handlers.Download,specialWidth= 10)
downloadButton.pack(padx = 20, pady = 10,ipadx = 10)
techreportButton = ui.drawButton(ButtonsFrame,"Technical Report",handlers.TechnicalReport,specialWidth= 15)
techreportButton.pack(padx = 20, pady = 10,ipadx = 10)
uploadButton['state']='disabled'
downloadButton['state']='disabled'
techreportButton['state']='disabled'
ui.root.mainloop()
