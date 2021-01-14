from functools import partial
from tkinter import END, Tk, Toplevel, Label, Frame, Text, SUNKEN, Button, BooleanVar, Checkbutton
from tkinter.filedialog import askdirectory
import exporter


def openFolderDialog(window, folderPathText):
    """
    opens the folder dialog for the desired export destination

    :param window: the window root
    :param folderPathText: the folderPath text widget
    """
    files = askdirectory(parent=window, title='Choose a file')
    folderPathText.insert(END, files)


def prepareExport(folderPathText, fileNameText, importer, dialect, isCSV=True):
    """
    prepares the export by combining the filePath out of the folder and filename
    gets the dataframe from the importer class and chooses the right export function by "isCSV"

    :param folderPathText: the folderpath destination
    :param fileNameText: the choosen filename for the export
    :param importer: the importer class (singelton)
    :param dialect: the dialect for the export method
    :param isCSV: boolean if the dataframe should be exported into csv or xml
    """
    dataframe = importer.getDataFrame()
    folderPath = folderPathText.get("1.0", "end-1c")
    fileName = fileNameText.get("1.0", "end-1c")
    filePath = folderPath + "/" + fileName
    if isCSV:
        exporter.exportToCSV(filePath, dataframe, dialect)
    else:
        exporter.exportToXML(filePath, dataframe, dialect)


def initExportDialog(root: Tk, importer, dialect):
    """
    initalizing the export dialog (contains the gui elements)

    :param root: the root object
    :param importer: the importer class (singelton)
    :param dialect: the dialect for the exported file
    """
    importer = importer
    window = Toplevel(root)
    hasHeaderVar = BooleanVar()

    h1 = Label(window, text="Table export", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")

    # Folder Frame
    folderFrame = Frame(window)
    folderPathText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    folderPathText.grid(row=0, column=1)
    openFolder_btn = Button(folderFrame, text="Select Folder", command=partial(openFolderDialog, window, folderPathText), width=20, padx=0)
    openFolder_btn.grid(row=0, column=0)

    Label(folderFrame, text="File Name:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
    fileNameText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
    fileNameText.grid(row=1, column=1)
    fileNameText.insert(1.0, "filename")
    folderFrame.pack(padx=5)

    # Dialect Frame
    dialectFrame = Frame(window)
    dialectFrame.grid_columnconfigure(0, weight=1)
    dialectFrame.grid_columnconfigure(1, weight=1)
    csvFrame = Frame(dialectFrame, borderwidth=1, relief="sunken")
    xmlFrame = Frame(dialectFrame, borderwidth=1, relief="sunken")

    h1 = Label(window, text="Export Options", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")

    # csv Frame
    Label(csvFrame, text="Encoding:", width=20, anchor="w", justify="left", padx=5, pady=5).grid(row=0)
    encodingCSVText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
    encodingCSVText.grid(row=0, column=1)

    Label(csvFrame, text="Has Header:", width=20, anchor="w", justify="left").grid(row=1)
    hasHeaderCheckbutton = Checkbutton(csvFrame, var=hasHeaderVar, onvalue=1, offvalue=0)
    hasHeaderCheckbutton.grid(sticky="w", row=1, column=1)

    Label(csvFrame, text="Seperator:", width=20, anchor="w", justify="left").grid(row=2)
    seperatorText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
    seperatorText.grid(row=2, column=1)

    Label(csvFrame, text="Quote Char:", width=20, anchor="w", justify="left", pady=5).grid(row=3)
    quoteCharText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
    quoteCharText.grid(row=3, column=1)
    csvFrame.grid(column=0, row=0, padx=5, sticky="nsew")

    # xml Frame
    Label(xmlFrame, text="Encoding:", width=20, anchor="w", justify="left", padx=5, pady=5).grid(column=0, row=0)
    encodingXMLText = Text(xmlFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
    encodingXMLText.grid(row=0, column=1)
    xmlFrame.grid(column=1, row=0, rowspan=4, padx=5, sticky="nsew")

    dialectFrame.pack(padx=5, pady=5, fill="x")

    # Button Frame
    buttonFrame = Frame(window)
    buttonFrame.grid_columnconfigure(0, weight=1)
    buttonFrame.grid_columnconfigure(1, weight=1)

    Button(buttonFrame, text="Export to CSV", command=partial(prepareExport, folderPathText, fileNameText, importer,
           dialect), width=20, padx=10, anchor="center").grid(column=0, row=0)
    Button(buttonFrame, text="Export to XML", command=partial(prepareExport, folderPathText, fileNameText, importer,
           dialect, False), width=20, padx=10).grid(column=1, row=0)
    buttonFrame.pack(padx=5, fill="x", pady=10)
