from tkinter import *
from importer import Importer
from tkinter.filedialog import askopenfilenames
from pandastable import Table, TableModel
import detector

importer = Importer()

root = Tk()
root.title("Tabelle importieren")
frame1 = Frame(root)
detectorFrame = Frame(root)
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

buttonFrame = Frame(frame1)
open_btn = Button(buttonFrame, text="Datendateien öffnen", command=openFileDialog)
open_btn.pack(padx=5, side=TOP, fill="x")
deleteAll_btn = Button(buttonFrame, text="Alle entfernen", command=deleteSelectedFiles)
deleteAll_btn.pack(padx=5, side=BOTTOM, fill="x")
buttonFrame.pack(side=LEFT)

dialogFrame = Frame(frame1)
selectedFiles = Text(dialogFrame, height=4)
selectedFiles.config(bg='#eee')
selectedFiles.pack(fill="y")
frame1.pack(pady=10, padx=5, fill="x")
dialogFrame.pack(expand=True, fill="x")

encoding = Label(detectorFrame, text="CSV-Zeichenkodierung:")
encoding.pack(side=LEFT, padx=5)
encodingText = Text(detectorFrame, height=1)
encodingText.pack(side=LEFT, fill="both", expand=TRUE)
detectorFrame.pack(fill="x")

vorschau = Label(root, text="Vorschau", bg="#eee")
vorschau.pack(expand=TRUE, fill="x", padx=5, side=TOP)
pt.show()
frame2.pack(pady=10, padx=5, fill="both", side=TOP)

if __name__ == '__main__':
    root.mainloop()

