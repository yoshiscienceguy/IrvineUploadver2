from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import platform, os
#SFID  Source Folder Id
SFID = "0B5wtxWXBa7L8S2dYaEtJMXMxeUk"
#Technical Report Id
TechID = "16grOWcXkxrjt1JundUKUQoGlPZigPBsOzExyKozcpD8"

def Connect():


    print("Authenticating")
    gauth = GoogleAuth()

    CurrentOS = platform.platform().split('-')[0]

    if(CurrentOS != "Windows"):
        gauth.LoadCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.LoadCredentialsFile("./credentials/mycreds.txt")
        
    if( gauth.credentials is None):
        gauth.LocalWebserverAuth()
    elif( gauth.access_token_expired):
        gauth.Refresh()
    else:
        gauth.Authorize()
           

    if(CurrentOS != "Windows"):
        gauth.SaveCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.SaveCredentialsFile("./mycreds.txt")
        
    print("Done Authenticating")

    drive = GoogleDrive(gauth)
    return drive
def CopyTechnicalReport(drive,parent,name = "Technical Report"):
    file_list = drive.ListFile({"q":"'"+parent+"' in parents and trashed = false"}).GetList()
    found = False
    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == name):
                found = True
                    
    if(not found):
        drive.auth.service.files().copy(fileId = TechID, body={"parents":[{"kind": "drive#fileLink",
                                                                   "id": parent}], 'title': name}).execute()
   
def GetFileURL(drive,ProjectName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == ProjectName):
                return file1['alternateLink']
def GetFileID(drive,FileName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == FileName):
                return file1['id']
    return None
def GetFiles(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Files = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            Files[file1["title"]] = file1["id"]
    return Files   
def GetFolders(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Folders = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(file1['mimeType'] == "application/vnd.google-apps.folder"):
            Folders[file1["title"]] = file1["id"]
    return Folders
def DownloadFile(drive,FileId,FileName):
    file1 = drive.CreateFile({'id':FileId})
    file1.GetContentFile(FileName)
def UploadFile(drive,ParentId,FilePath,FileName):
    Id = GetFileID(drive,FileName,ParentId)
    if(Id ==None):
        file2Upload = drive.CreateFile({"parents":[{"id" : ParentId}]})
    else:
        file2Upload = drive.CreateFile({'id':Id})
    file2Upload.SetContentFile(FilePath)
    file2Upload["title"] = FileName
    file2Upload.Upload()


def CreateFolder(drive,FolderName,ParentId):
    newFolder = drive.CreateFile({"title":FolderName,
                                  "mimeType": "application/vnd.google-apps.folder",
                                  "parents" : [{"id" : ParentId}]})
    newFolder.Upload()
    return newFolder['id']

drive = Connect()
file_list = drive.ListFile({"q":"'"+SFID+"' in parents and trashed = false"}).GetList()
print("hello")
for file1 in file_list:
    print(file1['title'])
    if(file1['mimeType'] == "application/vnd.google-apps.folder" and not file1["title"] in ["Summer Camps","Gamologie","Buildologie","K-12 STEM Club","Camps"]):
        sublist = drive.ListFile({"q":"'"+file1["id"]+"' in parents and trashed = false"}).GetList()
        for file2 in sublist:

            
            if(file2["title"] != "" and not "_" in file2["title"]):
                print(file2["title"])
                sublist = drive.ListFile({"q":"'"+file2["id"]+"' in parents and trashed = false"}).GetList()
                Codefound = False
                Docfound = False
                Mediafound = False
                
                exists = False
                existsID = file2['id']
                for file3 in sublist:
                    print(file3["title"])
                    if(file3["title"] in ["Codologie I - (Intro)","Codologie II - (Intermediate)","Codologie III - (Advanced)","Codologie I (Intro)","Codologie II (Intermediate)","Codologie III (Advanced)"]):
                        exists = True
                        existsID = file3["id"]
                        break
                if(exists):
                    sublist = drive.ListFile({"q":"'"+existsID+"' in parents and trashed = false"}).GetList()
                for file3 in sublist:
                    if( file3["title"].lower() == "code"):
                        Codefound = True
                    if( file3["title"].lower() == "document" or file3["title"].lower() == "documents" or file3["title"].lower() == "technical report"):
                        if(file3["title"].lower() == "technical report"):
                            file3["title"] = "Documents"
                            file3.Upload()
                        Docfound = True
                    if( file3["title"].lower() == "media" or file3["title"].lower() == "presentation"):
                        if(file3["title"].lower() == "presentation"):
                            file3["title"] = "Media"
                            file3.Upload()
                        Mediafound = True
                        
                        #file4 = drive.CreateFile({'title': "Codologie II (Intermediate)", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
                        #file4.Upload()
                        
                print(exists)

                
                if(not Codefound):
                    filec = drive.CreateFile({'title': "Code", "parents":  [{"id": existsID}], "mimeType": "application/vnd.google-apps.folder"})
                    filec.Upload()
                if(not Docfound):
                    fileb = drive.CreateFile({'title': "Document", "parents":  [{"id": existsID}], "mimeType": "application/vnd.google-apps.folder"})
                    fileb.Upload()
                if(not Mediafound):
                    filea = drive.CreateFile({'title': "Media", "parents":  [{"id": existsID}], "mimeType": "application/vnd.google-apps.folder"})
                    filea.Upload()
                if(not exists):
                    file4 = drive.CreateFile({'title': "Codologie II - (Intermediate)", "parents":  [{"id": existsID}], "mimeType": "application/vnd.google-apps.folder"})
                    file4.Upload()
                    Main = file4["id"]
                    print("made")
                else:
                    Main = existsID

                sublist = drive.ListFile({"q":"'"+Main+"' in parents and trashed = false"}).GetList()

                
                    
                for file3 in sublist:
                    if(file3["title"].lower() == "code"):
                        CodeId = file3["id"]
                        break
                for file3 in sublist:
                    if(file3["title"].lower() in ["document","documents"]):
                        DocId = file3["id"]
                        break
                for file3 in sublist:
                    if(file3["title"].lower() == "media"):
                        MediaId = file3["id"]
                        break

                for file3 in sublist:
                    if(file3["mimeType"] in ["application/vnd.google-apps.document","application/vnd.google-apps.spreadsheet","application/vnd.google-apps.presentation"]):
                        file3["parents"]= [{"id": DocId}]
                        file3.Upload()
                    name = file3['title']
                    ext = name.split(".")[-1].lower()
                    if(ext in ["py","ino","txt","jar","java","rbt","sb2"]):
                        file3["parents"]= [{"id": CodeId}]
                        file3.Upload()
                    if(ext in ["jpg","png","gif","tiff","bmp"]):
                        file3["parents"]= [{"id": MediaId}]
                        file3.Upload()
                    
                sublist = drive.ListFile({"q":"'"+file2["id"]+"' in parents and trashed = false"}).GetList()
                for file3 in sublist:
                    if( file3["title"].lower() in ["code","document","media", "documents"]):
                        file3["parents"]= [{"id": Main}]
                        file3.Upload()

    
##DRIVE = Connect()
##Ids = GetSchoolFolderIDs(DRIVE)
##cD = time.strftime("%A")
##DayId = GetClassFolderID(DRIVE,Ids['Ponderosa'],cD)
##p = "C:\\Users\\Fernando\\Desktop\\Anaheim GoogleDrive\\test.txt"
##ClassId = GetTeacherID(DRIVE,DayId[cD],"Vasquez")
##Upload(DRIVE,ClassId["Vasquez"],"Code",p,"test")
