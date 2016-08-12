#import LibraryCheck
from TkinterDnD2 import *
from Tkinter import *

root = TkinterDnD.Tk()

l = Listbox(root)
l.pack(fill='both', expand=1)
root.update()

# make the listbox a drop target
l.drop_target_register('*')

def drop(event):
    print 'Dropped file(s):', event.data
    if event.data:
        try:
            files = event.data.split()
            for f in files:
                l.insert('end', f)
        except:
            pass
    return COPY
root.mainloop()
