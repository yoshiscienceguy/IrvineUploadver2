import LibraryCheck
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import platform, os
###SFID  Source Folder Id
##SFID = "0B5wtxWXBa7L8S2dYaEtJMXMxeUk"
###Codologie
##Codologie = "0B2a5Zc1PcnIRQjZCc2ZjSGlfU2M"
###Buildologie
##Buildologie = "0B5wtxWXBa7L8ZUhLZWc0akpJajA"
###Gameologie
##Gameologie = "0B5wtxWXBa7L8eEYxQTZCX0JKZ3M"
###K-12 Stem Club
##KStemClub = "0B-OKkANrBIvUWkVpX19aRkVScFE"
###Docs & Templates
##DT = "0B5wtxWXBa7L8a1VjU0tGNElmdVk"
###Technical Report Id
##TechID = "16grOWcXkxrjt1JundUKUQoGlPZigPBsOzExyKozcpD8"
class IDs():
    def __init__(self):
        self.StudentFolder = "0B5wtxWXBa7L8S2dYaEtJMXMxeUk"
        self.Codologie = "0B2a5Zc1PcnIRQjZCc2ZjSGlfU2M"
        self.Buildologie = "0B5wtxWXBa7L8ZUhLZWc0akpJajA"
        self.Gamologie = "0B5wtxWXBa7L8eEYxQTZCX0JKZ3M"
        self.KStemClub = "0B-OKkANrBIvUWkVpX19aRkVScFE"
        self.DocTemplates = "0B5wtxWXBa7L8a1VjU0tGNElmdVk"
        self.CTechnicalReport = "1Bx-_MCr9jqiVTkm7UcSDwHnwKmWk-1YitOgRctbpDzw"
        self.BTechnicalReport = "1p81KbPvAioTTcPtsypfTVm6gNcvrnZuaD5Uz8iuHrsc"
    
class Drive():
    def __init__(self):
        self.ids = IDs()
        self.drive = None
        self.currentDirectory = ""
        #self.getDirectory()
        self.Connect()
        
    def getDirectory(self):
        CurrentDirectory = os.getcwd()
        parts = CurrentDirectory.split("\\")
        place = parts.index("Users")
        path = ""
        for part in parts[:place+1]:
            path += part + "\\"
        path += parts[place+1]+"\\IrvineUploadProgram\\src\\MxPiDrive\\"
        os.chdir (path)
        
    def Connect(self):
        print("Authenticating")
        gauth = GoogleAuth()

        CurrentOS = platform.platform().split('-')[0]

        if(CurrentOS != "Windows"):
            gauth.LoadCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
        else:
            gauth.LoadCredentialsFile("credentials/mycreds.txt")
            
        if( gauth.credentials is None):
            gauth.LocalWebserverAuth()
        elif( gauth.access_token_expired):
            gauth.Refresh()
        else:
            gauth.Authorize()
        if(CurrentOS != "Windows"):
            gauth.SaveCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
        else:
            gauth.SaveCredentialsFile("credentials/mycreds.txt")
            
        print("Done Authenticating")

        self.drive = GoogleDrive(gauth)
        #self._updateIDs()
    def _updateIDs(self):
        folders = self.GetFolders()
        for folder in folders:
            if("Codologie" in folder):
                self.ids.Codologie = folders[folder]
            if("K-12 STEM Club" in folder):
                self.ids.KStemClub = folders[folder]
            if("Camps" in folder):
                self.ids.Camps = folders[folder]
            if("Gameologie" in folder):
                self.ids.Gameologie = folders[folder]
            if("Buildologie" in folder):
                self.ids.Buildologie = folders[folder]
        folders = self.GetFolders(self.ids.Codologie)
        for folder in folders:
            if("Template" in folder):
                self.ids.DocTemplates = folders[folder]
        files = self.GetFiles(self.ids.DocTemplates)
        for file1 in files:
            if("Codologie" in file1):
                self.ids.CTechnicalReport = folders[folder]
            if("Buildologie" in file1):
                self.ids.BTechnicalReport = folders[folder]
    def _GetFileInfo(self,FileName,ParentId = None):
        if(not ParentId):
            ParentId = self.ids.StudentFolder
        file_list = self.drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
        for file1 in file_list:
            if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
                if(file1['title'] == FileName):
                    toreturn = (file1['id'], file1['alternateLink'])
                    
                    return toreturn
        return None
    def _GetFolderInfo(self,FileName,ParentId = None):
        if(not ParentId):
            ParentId = self.ids.StudentFolder
        file_list = self.drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
        for file1 in file_list:
            if(file1['mimeType'] == "application/vnd.google-apps.folder"):
                if(file1['title'] == FileName):
                    toreturn = (file1['id'], file1['alternateLink'])
                    
                    return toreturn
        return None
    def GetFolders(self,ParentId = None):
        if(not ParentId):
            ParentId = self.ids.StudentFolder
        file_list = self.drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
        Folders = {}
        for file1 in file_list:
            #print(file1['alternateLink'])
            if(file1['mimeType'] == "application/vnd.google-apps.folder"):
                Folders[file1["title"]] = file1["id"]
        #print(Folders)
        return Folders
    def GetFiles(self,ParentId = None):
        if(not ParentId):
            ParentId = self.ids.StudentFolder
        file_list = self.drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
        Files = {}
        for file1 in file_list:
            #print(file1['alternateLink'])
            if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
                Files[file1["title"]] = file1["id"]
        print(Files)
        return Files 
    def CopyTechnicalReport(self,studentFolder,name = "Technical Report"):
        file_list = self.drive.ListFile({"q":"'"+studentFolder+"' in parents and trashed = false"}).GetList()
        found = False
        for file1 in file_list:
            if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
                if(name == file1['title']):
                    found = True
                        
        if(not found):
            self.drive.auth.service.files().copy(fileId = self.ids.CTechnicalReport, body={"parents":[{"kind": "drive#fileLink",
                                                                                                       "id": studentFolder}], 'title': name}).execute()
    def DownloadFile(self,FileId,FileName):
        file1 = self.drive.CreateFile({'id':FileId})
        file1.GetContentFile(FileName)
    def UploadFile(self,ParentId,FilePath,FileName):
        
        returned = self._GetFileInfo(FileName,ParentId)
        if(returned ==None):
            file2Upload = self.drive.CreateFile({"parents":[{"id" : ParentId}]})
        else:
            Id,Link = returned
            file2Upload = self.drive.CreateFile({'id':Id})
        file2Upload.SetContentFile(FilePath)
        file2Upload["title"] = FileName
        file2Upload.Upload()
    def CreateFolder(self,ParentId,FolderName):
        returned = self._GetFolderInfo(FolderName,ParentId)
        idtoReturn = ""
        if(returned == None):
            newFolder = self.drive.CreateFile({"title":FolderName,
                                          "mimeType": "application/vnd.google-apps.folder",
                                          "parents" : [{"id" : ParentId}]})
            newFolder.Upload()
            idtoReturn = newFolder['id']
        else:
            idtoReturn,Link = returned
        return idtoReturn  
#gd = Drive()
#gd.CreateFolder(gd.ids.DocTemplates,"testingFolder")
#gd.GetFiles(gd.ids.DocTemplates)
#gd.CopyTechnicalReport("0B5wtxWXBa7L8S0s1dUxXX0pmNTQ","Yolo")
#gd.UploadFile(gd.ids.DocTemplates,"dummy.txt","dummy.txt")
#gd.DownloadFile("0B5wtxWXBa7L8WWxodUJ4bmtUZTQ","test.txt")
