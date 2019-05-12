import Tkinter
from untested_tkdnd_wrapper import TkDND


def handle(event):
    files = root.tk.splitlist(event.data)

    for filename in files:
        event.widget.insert('end', filename)


root = Tkinter.Tk()    
lb   = Tkinter.Listbox(root, width=50)
lb.pack(fill='both', expand=1)

dnd = TkDND(root)
dnd.bindtarget(lb, handle, 'text/uri-list')

root.mainloop()
