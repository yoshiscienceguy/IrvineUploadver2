import os, shutil, platform
def CheckDnDWrapper(filepath = "C:/Python27/tcl/"):
    filePresent = False
    initFile = False
    for directory in os.listdir(filepath):
        if("dnd" in directory):
            filePresent = True
            print("Dnd Library Present")
        if("__init__" in directory):
            initFile = True
    if(not initFile):
        shutil.copy("libs/__init__.py",filepath)
        print("Copying __init__.py")
    if(not filePresent):
        os.makedirs(filepath+"tkdnd2.8")
        for files in os.listdir("libs/tkdnd2.8"):
            
            shutil.copy("libs/tkdnd2.8/"+files,filepath+"tkdnd2.8")
        print("Copied DnD library")

def CheckExternalLibraries(filepath = "C:/Python27/Lib/site-packages/"):
    try:
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
    except:
        print("error copying libs")
            
useros = platform.system()
if(useros== "Linux"):
    import subprocess
    pathhome = os.getcwd()
    os.chdir(pathhome+"/libs/")
    subprocess.call(['python', 'setup.py', 'install'])
    os.chdir(pathhome)
else:
    CheckDnDWrapper()
    CheckExternalLibraries()
