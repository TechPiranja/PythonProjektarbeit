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

h1 = Label(root, text="Datendateien", bg="#eee")
h1.pack(padx=5, pady=5, fill="x")

def openFileDialog():
    files = list(askopenfilenames(parent=root, title='Choose a file'))
    updateDf(files)

def deleteSelectedFiles():
    selectedFiles.delete(1.0, END)

def getSelectedFiles():
    return selectedFiles.get(1.0, END)

def exportToCSV():
    pt.doExport("./testFiles/testfile.csv")
    print("Test")

def export():
    window = Toplevel(root)
    h1 = Label(window, text="Tabelle exportieren", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")

    exportBtn = Button(window, text="Exportieren", command=exportToCSV, width=20, padx=0)
    exportBtn.pack(fill="x", padx=10, pady=10)

#Dialog Frame
dialogFrame = Frame(root)

open_btn = Button(dialogFrame, text="Datendateien öffnen", command=openFileDialog, width=20, padx=0)
open_btn.grid(row=0, column=0)
deleteAll_btn = Button(dialogFrame, text="Alle entfernen", command=deleteSelectedFiles, width=20, padx=0)
deleteAll_btn.grid(row=1, column=0)
selectedFiles = Text(dialogFrame, height=4, borderwidth=2, relief=SUNKEN)
selectedFiles.grid(row=0, column=1, rowspan=2)
dialogFrame.pack(fill="x", padx=5)

#Detector Frame
h1 = Label(root, text="Detector", bg="#eee")
h1.pack(padx=5, pady=5, fill="x")

detectorFrame = Frame(root)

Label(detectorFrame, text="CSV-Zeichenkodierung:", width=20, anchor="w", justify="left", padx=0).grid(row=0, column=0)
encodingText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
encodingText.grid(row=0, column=1)

Label(detectorFrame, text="Has Header:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
hasHeaderText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
hasHeaderText.grid(row=1, column=1)

Label(detectorFrame, text="Seperator:", width=20, anchor="w", justify="left", padx=0).grid(row=2, column=0)
seperatorText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
seperatorText.grid(row=2, column=1)

Label(detectorFrame, text="Quote Char:", width=20, anchor="w", justify="left", padx=0).grid(row=3, column=0)
quoteCharText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
quoteCharText.grid(row=3, column=1)

detectorFrame.pack(fill="x", padx=5, pady=5)

#Vorschau und Pandastable
vorschau = Label(root, text="Vorschau", bg="#eee")
vorschau.pack(expand=TRUE, fill="x", padx=5, side=TOP)
pt.show()
frame2.pack(pady=10, padx=5, fill="both", side=TOP)

exportBtn = Button(root, text="Exportieren", command=export, width=20, padx=0)
exportBtn.pack(fill="x", padx=10, pady=10)
def updateDf(files: list):
    #TODO: Sniffer can only be used on csv?!
    if files[0].endswith(".csv"):
        dialect = detector.Dialect()
        dialect.guessDialectCSV(files[0])

        importer.importCSV(files[0], dialect)
        updatedDataframe = importer.getDataFrame()
        pt.updateModel(TableModel(updatedDataframe))
        pt.redraw()

        # TODO use CSV Merge Method ( not implemented yet )
        selectedFiles.insert(END, files)  # TODO: import without {} brackets
        encodingText.insert(1.0, dialect.encoding)
        hasHeaderText.insert(1.0, dialect.hasHeader)
        seperatorText.insert(1.0, dialect.delimiter)
        quoteCharText.insert(1.0, dialect.quotechar)
    elif files[0].endswith(".xml") or files[0].endswith(".xsl"):
        selectedFiles.insert(END, files)
        xmlFile = files[0]
        xslFile = files[1]
        dialect = importer.importXML(xmlFile, xslFile)
        hasHeaderText.insert(1.0, dialect.hasHeader)
        seperatorText.insert(1.0, dialect.delimiter)
        quoteCharText.insert(1.0, dialect.quotechar)
        encodingText.insert(1.0, "XSLT")
        updatedDataframe = importer.getDataFrame()
        pt.updateModel(TableModel(updatedDataframe))
        pt.redraw()

if __name__ == '__main__':
    root.mainloop()

