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
    updateDf(files)

def updateDf(files: list):
    # TODO use CSV Merge Method ( not implemented yet )
    selectedFiles.insert(END, files)  # TODO: import without {} brackets
    encodingText.insert(1.0, detector.detectEncoding(files[0]))

    importer.importCSV(files[0])
    updatedDataframe = importer.getDataFrame()
    print("has Header: " + str(detector.detectHeader(files[0])))
    pt.updateModel(TableModel(updatedDataframe))
    pt.redraw()

def deleteSelectedFiles():
    selectedFiles.delete(1.0, END)

def getSelectedFiles():
    return selectedFiles.get(1.0, END)


h1 = Label(frame1, text="Datendateien", bg="#eee")
h1.pack(expand=TRUE, fill="x")

#Dialog Frame
dialogFrame = Frame(root)

open_btn = Button(dialogFrame, text="Datendateien öffnen", command=openFileDialog, width=20, padx=0).grid(row=0, column=0)
deleteAll_btn = Button(dialogFrame, text="Alle entfernen", command=deleteSelectedFiles, width=20, padx=0).grid(row=1, column=0)

selectedFiles = Text(dialogFrame, height=4, borderwidth=2, relief=SUNKEN).grid(row=0, column=1, rowspan=2)

dialogFrame.pack(fill="x", padx=5)

#Detector Frame
detectorFrame = Frame(root)

encoding = Label(detectorFrame, text="CSV-Zeichenkodierung:", width=20, anchor="w", justify="left", padx=0).grid(row=0, column=0)
encodingText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN).grid(row=0, column=1)

hasHeaderLabel = Label(detectorFrame, text="Has Header:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
hasHeaderText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN).grid(row=1, column=1)

detectorFrame.pack(fill="x", padx=5)

#Vorschau und Pandastable
vorschau = Label(root, text="Vorschau", bg="#eee")
vorschau.pack(expand=TRUE, fill="x", padx=5, side=TOP)
pt.show()
frame2.pack(pady=10, padx=5, fill="both", side=TOP)

if __name__ == '__main__':
    root.mainloop()

