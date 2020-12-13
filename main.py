from tkinter import *
from importer import Importer
from tkinter.filedialog import askopenfilenames

importer = Importer()

root = Tk()
root.title("Tabelle importieren")

def openFileDialog():
    selectedFiles.insert(END, (list(askopenfilenames(parent=root, title='Choose a file'))))
    test = selectedFiles.get(1.0, END)
    print(test)

def deleteSelectedFiles():
    selectedFiles.delete(1.0, END)

h1 = Label(root, text="Datendateien")
h1.pack()
open_btn = Button(root, text="Datendateien öffnen", command=openFileDialog)
open_btn.pack(padx=5, pady=10, side=LEFT)
delete_btn = Button(root, text="Auswahl entfernen")
delete_btn.pack(padx=5, pady=10, side=LEFT)
deleteAll_btn = Button(root, text="Alle entfernen", command=deleteSelectedFiles)
deleteAll_btn.pack(padx=5, pady=10, side=LEFT)

selectedFiles = Text(root)
selectedFiles.pack()

if __name__ == '__main__':
    root.mainloop()

