from functools import partial
from tkinter import END, Tk, Toplevel, Label, Frame, Text, SUNKEN, Button
from tkinter.filedialog import askdirectory
import exporter


def openFolderDialog(window, folderPath):
    files = askdirectory(parent=window, title='Choose a file')
    folderPath.insert(END, files)

def prepareExport(folderPathText, fileNameText, importer, dialect, isCSV = True):
    dataframe = importer.getDataFrame()
    folderPath = folderPathText.get("1.0", "end-1c")
    fileName = fileNameText.get("1.0", "end-1c")
    filePath = folderPath + "/" + fileName
    if (isCSV):
        exporter.exportToCSV(filePath, dataframe, dialect)
    else:
        exporter.exportToXML(filePath, dataframe, dialect)

def initExportDialog(root: Tk, importer, dialect):
    importer = importer
    window = Toplevel(root)
    h1 = Label(window, text="Table export", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")

    folderFrame = Frame(window)
    folderPathText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    folderPathText.grid(row=0, column=1)
    openFolder_btn = Button(folderFrame, text="Select Folder", command=partial(openFolderDialog, window, folderPathText), width=20, padx=0)
    openFolder_btn.grid(row=0, column=0)

    Label(folderFrame, text="File Name:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
    fileNameText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    fileNameText.grid(row=1, column=1)
    fileNameText.insert(1.0, "filename")

    exportCSVBtn = Button(folderFrame, text="Export to CSV", command=partial(prepareExport, folderPathText, fileNameText, importer, dialect), width=20, padx=0)
    exportCSVBtn.grid(row=2, column=0)
    exportXMLBtn = Button(folderFrame, text="Export to XML", command=partial(prepareExport, folderPathText, fileNameText, importer, dialect, False), width=20, padx=0, anchor="e")
    exportXMLBtn.grid(row=2, column=1)
    folderFrame.pack(padx=5)
