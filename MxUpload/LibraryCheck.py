import os, shutil
def CheckDnDWrapper(filepath = "C:/Python27/tcl/"):
    filePresent = False
    for directory in os.listdir(filepath):
        if("dnd" in directory):
            filePresent = True
            print("Dnd Library Present")
            break
    if(not filePresent):
        os.makedirs("C:/Python27/tcl/tkdnd2.8")
        for files in os.listdir("libs/tkdnd2.8"):
            
            shutil.copy("libs/tkdnd2.8/"+files,"C:/Python27/tcl/tkdnd2.8")
        print("Copied DnD library")

def CheckExternalLibraries(filepath = "C:/Python27/Lib/site-packages/"):
    libraries = os.listdir("libs")
    existingLibraries = os.listdir(filepath)
    for library in libraries:
        if(library not in existingLibraries):
            print(library + " not present, copying")
            try:
                shutil.copytree("libs/"+library,filepath+library)
            except:
                shutil.copy("libs/"+library,filepath+library)
        else:
            print(library+ " exists")
            
CheckDnDWrapper()
CheckExternalLibraries()
