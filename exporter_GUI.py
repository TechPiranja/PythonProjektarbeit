from functools import partial
from tkinter import END, Tk, Toplevel, Label, Frame, Text, SUNKEN, Button, BooleanVar, Checkbutton
from tkinter.filedialog import askdirectory
import exporter


class ExporterGUI:
    def __init__(self, root: Tk, importer, dialect):
        """
        initalizing the export dialog (contains the gui elements)

        :param root: the root object
        :param importer: the importer class (singelton)
        :param dialect: the dialect for the exported file
        """
        self.importer = importer
        self.window = Toplevel(root)
        self.dialect = dialect
        self.hasHeaderVar = BooleanVar()

        h1 = Label(self.window, text="Table export", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        # Folder Frame
        folderFrame = Frame(self.window)
        folderPathText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
        folderPathText.grid(row=0, column=1)
        openFolder_btn = Button(folderFrame, text="Select Folder",
                                command=partial(self.openFolderDialog, folderPathText), width=20, padx=0)
        openFolder_btn.grid(row=0, column=0)

        Label(folderFrame, text="File Name:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
        fileNameText = Text(folderFrame, height=1, borderwidth=2, relief=SUNKEN)
        fileNameText.grid(row=1, column=1)
        fileNameText.insert(1.0, "filename")
        folderFrame.pack(padx=5)

        # Dialect Frame
        dialectFrame = Frame(self.window)
        dialectFrame.grid_columnconfigure(0, weight=1)
        dialectFrame.grid_columnconfigure(1, weight=1)
        csvFrame = Frame(dialectFrame, borderwidth=1, relief="sunken")
        xmlFrame = Frame(dialectFrame, borderwidth=1, relief="sunken")

        h1 = Label(self.window, text="Export Options", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        # csv Frame
        Label(csvFrame, text="Encoding:", width=20, anchor="w", justify="left", padx=5, pady=5).grid(row=0)
        self.encodingCSVText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.encodingCSVText.grid(row=0, column=1)

        Label(csvFrame, text="Has Header:", width=20, anchor="w", justify="left").grid(row=1)
        self.hasHeaderCheckbutton = Checkbutton(csvFrame, var=self.hasHeaderVar, onvalue=1, offvalue=0)
        self.hasHeaderCheckbutton.grid(sticky="w", row=1, column=1)

        Label(csvFrame, text="Seperator:", width=20, anchor="w", justify="left").grid(row=2)
        self.seperatorText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.seperatorText.grid(row=2, column=1)

        Label(csvFrame, text="Quote Char:", width=20, anchor="w", justify="left", pady=5).grid(row=3)
        self.quoteCharText = Text(csvFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.quoteCharText.grid(row=3, column=1)
        csvFrame.grid(column=0, row=0, padx=5, sticky="nsew")

        # xml Frame
        Label(xmlFrame, text="Encoding:", width=20, anchor="w", justify="left", padx=5, pady=5).grid(column=0, row=0)
        self.encodingXMLText = Text(xmlFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.encodingXMLText.grid(row=0, column=1)
        xmlFrame.grid(column=1, row=0, rowspan=4, padx=5, sticky="nsew")

        dialectFrame.pack(padx=5, pady=5, fill="x")

        # Button Frame
        buttonFrame = Frame(self.window)
        buttonFrame.grid_columnconfigure(0, weight=1)
        buttonFrame.grid_columnconfigure(1, weight=1)

        Button(buttonFrame, text="Export to CSV", command=partial(self.prepareExport, folderPathText, fileNameText),
               width=20, padx=10, anchor="center").grid(column=0, row=0)
        Button(buttonFrame, text="Export to XML", command=partial(self.prepareExport, folderPathText, fileNameText,
                                                                  False), width=20, padx=10).grid(column=1, row=0)
        buttonFrame.pack(padx=5, fill="x", pady=10)

        # imports the dialect data from importer_GUI
        # csv side
        self.encodingCSVText.delete(1.0, END)
        self.encodingCSVText.insert(1.0, self.dialect.encoding)

        self.hasHeaderVar.set(self.dialect.hasHeader)

        self.seperatorText.delete(1.0, END)
        self.seperatorText.insert(1.0, self.dialect.delimiter)

        self.quoteCharText.delete(1.0, END)
        self.quoteCharText.insert(1.0, self.dialect.quoteChar)

        # xml side
        self.encodingXMLText.delete(1.0, END)
        self.encodingXMLText.insert(1.0, self.dialect.encoding)

    def openFolderDialog(self, folderPathText):
        """
        opens the folder dialog for the desired export destination

        :param window: the window root
        :param folderPathText: the folderPath text widget
        """
        files = askdirectory(parent=self.window, title='Choose a file')
        folderPathText.insert(END, files)

    def prepareExport(self, folderPathText, fileNameText, isCSV=True):
        """
        prepares the export by combining the filePath out of the folder and filename
        gets the dataframe from the importer class and chooses the right export function by "isCSV"

        :param folderPathText: the folderpath destination
        :param fileNameText: the choosen filename for the export
        :param importer: the importer class (singelton)
        :param dialect: the dialect for the export method
        :param isCSV: boolean if the dataframe should be exported into csv or xml
        """
        dataframe = self.importer.getDataFrame()
        folderPath = folderPathText.get("1.0", "end-1c")
        fileName = fileNameText.get("1.0", "end-1c")
        filePath = folderPath + "/" + fileName

        if isCSV:
            self.dialect.encoding = self.encodingCSVText.get(1.0, 'end-1c')
            self.dialect.hasHeader = self.hasHeaderVar.get()
            self.dialect.delimiter = self.seperatorText.get(1.0, 'end-1c')
            self.dialect.quoteChar = self.quoteCharText.get(1.0, 'end-1c')
            exporter.exportToCSV(filePath, dataframe, self.dialect)
        else:
            self.dialect.encoding = self.encodingXMLText.get(1.0, 'end-1c')
            exporter.exportToXML(filePath, dataframe, self.dialect.encoding)
