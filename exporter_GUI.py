from functools import partial
from tkinter import *
from tkinter.filedialog import askdirectory
from pandastable import Table
import exporter


def openFolderDialog(window, folderPath):
    files = askdirectory(parent=window, title='Choose a file')
    folderPath.insert(END, files)

def initExportDialog(root: Tk, pt: Table):
    window = Toplevel(root)
    h1 = Label(window, text="Tabelle exportieren", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")

    folderFrame = Frame(window)
    folderPath = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    folderPath.grid(row=0, column=1)
    openFolder_btn = Button(folderFrame, text="Select Folder", command=partial(openFolderDialog, window, folderPath), width=20, padx=0)
    openFolder_btn.grid(row=0, column=0)

    Label(folderFrame, text="File Name:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
    fileName = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    fileName.grid(row=1, column=1)
    fileName.insert(1.0, "filename.csv")

    folderFrame.pack(padx=5)
    exportBtn = Button(window, text="Exportieren", command=exporter.exportToCSV(pt), width=20, padx=0)
    exportBtn.pack(fill="x", padx=10, pady=10)
