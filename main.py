from tkinter import *
from importer import Importer
from tkinter.filedialog import askopenfilenames
from pandastable import Table

importer = Importer()
importer.importCSV()

root = Tk()
root.title("Tabelle importieren")

def openFileDialog():
    selectedFiles.insert(END, (list(askopenfilenames(parent=root, title='Choose a file'))))

def deleteSelectedFiles():
    selectedFiles.delete(1.0, END)

def getSelectedFiles():
    return selectedFiles.get(1.0, END)

frame1 = Frame(root)
frame2 = Frame(root)

h1 = Label(frame1, text="Datendateien")
h1.pack()
open_btn = Button(frame1, text="Datendateien öffnen", command=openFileDialog)
open_btn.pack(padx=5, pady=10, side=LEFT)
deleteAll_btn = Button(frame1, text="Alle entfernen", command=deleteSelectedFiles)
deleteAll_btn.pack(padx=5, pady=10, side=LEFT)
selectedFiles = Text(frame1, height=5)
selectedFiles.config(bg='grey')
selectedFiles.pack()
frame1.pack(pady=10, padx=5)


vorschau = Label(root, text="Vorschau")
vorschau.pack()
dataframe = importer.getDataFrame()
pt = Table(frame2, dataframe=dataframe)
pt.show()
frame2.pack(side=LEFT)

if __name__ == '__main__':
    root.mainloop()

