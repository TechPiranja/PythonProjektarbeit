from tkinter import *
from importer import Importer
from tkinter.filedialog import askopenfilenames
from pandastable import Table, TableModel
import detector

importer = Importer()

root = Tk()
root.title("Tabelle importieren")
frame1 = Frame(root)
frame2 = Frame(root)
pt = Table(frame2)

def openFileDialog():
    files = list(askopenfilenames(parent=root, title='Choose a file'))
    selectedFiles.insert(END, files) # TODO: import without {} brackets
    updateDf(files)

def updateDf(files: list):
    # TODO use CSV Merge Method ( not implemented yet )
    importer.importCSV(files[0])
    updatedDataframe = importer.getDataFrame()
    print("has Header: " + str(detector.detectHeader(files[0])))
    print("Encoding: " + str(detector.detectEncoding(files[0])))
    pt.updateModel(TableModel(updatedDataframe))
    pt.redraw()

def deleteSelectedFiles():
    selectedFiles.delete(1.0, END)

def getSelectedFiles():
    return selectedFiles.get(1.0, END)


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
pt.show()
frame2.pack(side=LEFT)

if __name__ == '__main__':
    root.mainloop()

