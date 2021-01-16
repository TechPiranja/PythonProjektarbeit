from tkinter import END, Tk, Label, Frame, Text, SUNKEN, Button, TRUE, TOP, Listbox, SINGLE, Scrollbar, DISABLED, Checkbutton, BooleanVar
from tkinter.filedialog import askopenfilenames, askopenfilename
from pandastable import Table, TableModel
import detector
from exporter_GUI import ExporterGUI
from importer import Importer
from merger import Merger

importer = Importer()
merger = Merger(importer)


class ImporterGUI:
    """
    This class is the main gui and shows the import window, it also contains the main methods which uses other helper classes

    Attributes:
        root = the root tk
        previewFrame = the frame that shows the preview of the dataframe
        XMLList = the 2D list which holds the xml filepath on the index 0 and the xsl filepath on index 1
    """
    def __init__(self, root: Tk):
        self.root = root
        self.previewFrame = Frame(root)
        self.pt = Table(self.previewFrame)
        self.dialect = detector.Dialect()
        self.XMLList = []
        self.DialectList = []
        self.hasHeaderVar = BooleanVar()
        self.currentPath = ""

        h1 = Label(self.root, text="Imported Files", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        # Dialog Frame
        dialogFrame = Frame(self.root)
        dialogFrame.grid_columnconfigure(1, weight=1)
        Button(dialogFrame, text="Import Files", command=self.openFileDialog, width=20).grid(row=0, column=0)
        Button(dialogFrame, text="Delete selected File", command=self.deleteSelectedFile, width=20).grid(row=1, column=0)
        Button(dialogFrame, text="Delete all", command=self.deleteAllFiles, width=20).grid(row=2, column=0)

        # the outside frame for the files listbox (it holds the listbox and the scrollbar)
        listbox_border = Frame(dialogFrame, bd=2, relief="sunken", background="white")
        listbox_border.grid(row=0, column=1, rowspan=3, padx=3, sticky="nsew")

        # the actual listbox
        self.importedFiles = Listbox(listbox_border, selectmode=SINGLE, height=4, borderwidth=0, highlightthickness=0, relief=SUNKEN, background="white")
        self.importedFiles.bind("<<ListboxSelect>>", self.selectionChanged)

        # the scrollbar inside the listbox_border frame
        vsb = Scrollbar(listbox_border, orient="vertical", command=self.importedFiles.yview)
        self.importedFiles.configure(yscrollcommand=vsb)
        vsb.pack(side="right", fill="y")
        self.importedFiles.pack(padx=2, pady=2, fill="both", expand=True)
        dialogFrame.pack(fill="x", padx=10)

        # XSL File Frame (its disabled when a csv file is selected in the listbox,
        # and set to "normal" when a xml is selected
        h1 = Label(root, text="XSL File", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")
        xslFrame = Frame(root)
        self.importXSL_btn = Button(xslFrame, state=DISABLED, text="Import XSL File", command=self.openXSLFileDialog, width=20)
        self.importXSL_btn.grid(row=0, column=0)
        self.XSLPath_text = Text(xslFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.XSLPath_text.grid(row=0, column=1)
        xslFrame.pack(fill="x", padx=10, pady=5)

        # Detector Frame
        h1 = Label(root, text="Detector", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")
        detectorFrame = Frame(root)

        Label(detectorFrame, text="Encoding:", width=20, anchor="w", justify="left").grid(row=0)
        self.encodingText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.encodingText.grid(row=0, column=1)

        Label(detectorFrame, text="Has Header:", width=20, anchor="w", justify="left").grid(row=1)
        self.hasHeaderCheckbutton = Checkbutton(detectorFrame, var=self.hasHeaderVar, onvalue=1, offvalue=0)
        self.hasHeaderCheckbutton.grid(sticky="W", row=1, column=1)

        Label(detectorFrame, text="Seperator:", width=20, anchor="w", justify="left").grid(row=2)
        self.seperatorText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.seperatorText.grid(row=2, column=1)

        Label(detectorFrame, text="Quote Char:", width=20, anchor="w", justify="left").grid(row=3)
        self.quoteCharText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN, width=10)
        self.quoteCharText.grid(row=3, column=1)

        Button(detectorFrame, text="Save Dialect Changes", command=self.saveDialectChanges, width=20).grid(row=4, column=0)

        detectorFrame.pack(fill="x", padx=10, pady=5)

        # dataframe preview frame
        preview = Label(root, text="Preview", bg="#eee")
        preview.pack(expand=TRUE, fill="x", padx=5, side=TOP)
        self.pt.show()
        self.previewFrame.pack(pady=10, padx=10, fill="both", side=TOP)

        # the bottom most centered export button which leads to the export window
        exportBtn = Button(root, text="Export", command=self.export, width=20, padx=0)
        exportBtn.pack(fill="x", padx=10, pady=10)

    def saveDialectChanges(self):
        """
        saves the Dialect changes made by the user
        """
        dialect = detector.Dialect()
        dialect.encoding = self.encodingText.get(1.0, 'end-1c')
        dialect.hasHeader = self.hasHeaderVar.get()
        dialect.delimiter = self.seperatorText.get(1.0, 'end-1c')
        dialect.quoteChar = self.quoteCharText.get(1.0, 'end-1c')
        if not self.currentPath:
            files = self.getImportedFiles()
            self.currentPath = files[0]
        path = self.currentPath
        print(path)
        if not any(path in x for x in self.DialectList):
            self.DialectList.append([path, dialect])
        elif any(path in x for x in self.DialectList):
            x = [x for x in self.DialectList if path in x][0]
            self.DialectList[self.DialectList.index(x)][1] = dialect
        self.updateDf(self.getImportedFiles())

    def selectionChanged(self, event):
        """
        this is an event which is triggered by selection changed inside the listbox widget
        it checks if the selected file is a xml, if so it sets the textbox intractable for the user

        :param event: the event which called it
        """
        selection = event.widget.curselection()
        if selection:
            data = event.widget.get(selection[0])
            self.currentPath = data
            if data.endswith(".xml"):
                # disable encoding changes
                self.encodingText.delete(1.0, END)
                self.hasHeaderVar.set(False)
                self.seperatorText.delete(1.0, END)
                self.quoteCharText.delete(1.0, END)
                self.encodingText["state"] = "disabled"
                self.hasHeaderCheckbutton["state"] = "disabled"
                self.seperatorText["state"] = "disabled"
                self.quoteCharText["state"] = "disabled"
                self.importXSL_btn["state"] = "normal"

                if any(data in x for x in self.XMLList):
                    x = [x for x in self.XMLList if data in x][0]
                    self.XSLPath_text.delete(1.0, END)
                    self.XSLPath_text.insert(1.0, self.XMLList[self.XMLList.index(x)][1])
                else:
                    self.XSLPath_text.delete(1.0, END)
                    self.XSLPath_text.insert(1.0, "please import a XSL File!")
            else:
                self.encodingText.delete(1.0, END)
                self.hasHeaderVar.set(False)
                self.seperatorText.delete(1.0, END)
                self.quoteCharText.delete(1.0, END)
                self.encodingText["state"] = "normal"
                self.hasHeaderCheckbutton["state"] = "normal"
                self.seperatorText["state"] = "normal"
                self.quoteCharText["state"] = "normal"
                self.importXSL_btn["state"] = "disabled"
                self.XSLPath_text.delete(1.0, END)

                if any(data in x for x in self.DialectList):
                    x = [x for x in self.DialectList if data in x][0]
                    dialect = self.DialectList[self.DialectList.index(x)][1]
                    self.updateDialect(dialect)

    def openXSLFileDialog(self):
        """
        this function is called if the user wants to import a xsl file in the xsl file frame
        it opens the filedialog and appends the xsl to the according xml into the XMLList attribute
        after that, it try's to update the dataframe and its preview by calling the update function
        """
        file = askopenfilename(parent=self.root, title='Choose a file', filetypes=[
                ("Extensible Stylesheet Language", "*.xsl"),
                ("All files", "*.*")
            ])
        self.XMLList.append([self.importedFiles.get(self.importedFiles.curselection()), file])
        self.XSLPath_text.delete(1.0, END)
        self.XSLPath_text.insert(1.0, file)
        self.updateDf(self.getImportedFiles())

    def openFileDialog(self):
        """
        this function opens the file dialog and imports the selected filepaths into the listbox and also
        calls the update function to redraw the new dataframe
        """
        files = list(askopenfilenames(parent=self.root, title='Choose a file', filetypes=[
            ("Excel files", ".xml .csv")
            ]))
        self.updateSelectedFiles(files)
        self.updateDf(self.getImportedFiles())

    def deleteSelectedFile(self):
        """
        deletes the selected file from the listbox and redraws the dataframe since one of its source is deleted
        also if a xml file is deleted, it also deletes the corresponding xsl file from the XMLList
        """
        path = self.importedFiles.get(self.importedFiles.curselection())
        if path is self.currentPath:
            self.currentPath = ""
        # delete from dialect list
        if any(path in x for x in self.DialectList):
            x = [x for x in self.DialectList if path in x][0]
            self.DialectList.pop(self.DialectList.index(x))

        index = self.importedFiles.get(0, END).index(path)
        self.importedFiles.delete(index)

        # delete from xml list
        if path.endswith(".xml"):
            x = [x for x in self.XMLList if path in x][0]
            self.XMLList.pop(self.XMLList.index(x))
        self.updateDf(self.getImportedFiles())

    def deleteAllFiles(self):
        """
        deletes all imported filepaths from the listbox and also from the dataframe
        """
        self.importedFiles.delete(0, END)
        self.currentPath = ""
        self.XMLList = []
        self.DialectList = []

    def getImportedFiles(self):
        """
        :return: returns the selected filepath from the listbox
        """
        return self.importedFiles.get(0, END)

    def updateSelectedFiles(self, files):
        """
        after opening a file dialog, this method is called to pass the new imported filepaths into the listbox

        :param files: filespaths from the filedialog
        """
        startIndex = self.importedFiles.size()
        for index, file in enumerate(files):
            self.importedFiles.insert(index + startIndex, file)

    def export(self):
        """
        opens the export window and passes the dataframe from the preview frame
        """
        importer.setDataFrame(self.pt.model.df)
        ExporterGUI(self.root, importer, self.dialect)

    def updateDf(self, files: list):
        """
        checks if the dataframe can be updated by the newly imported filepaths
        calls the merge function if there is more than 1 file inside the filelist
        also udpates the detector frame (displaying dialect data)

        :param files: the whole filepath list
        """
        if len(files) > 1 or len(self.XMLList) > 0:
            canMerge = merger.prepareMerge(files, self.XMLList, self.DialectList)
            self.DialectList = merger.dialectList
            if canMerge:
                newDataFrame = merger.mergeFiles()
                importer.setDataFrame(newDataFrame)
                self.pt.updateModel(TableModel(newDataFrame))
                self.pt.redraw()
        elif len(files) > 0 and files[0].endswith(".csv"):
            if not any(files[0] in x for x in self.DialectList):
                self.dialect.guessDialectCSV(files[0])
                self.DialectList.append([files[0], self.dialect])
            else:
                x = [x for x in self.DialectList if files[0] in x][0]
                self.dialect = self.DialectList[self.DialectList.index(x)][1]
            importer.importCSV(files[0], self.dialect)
            updatedDataframe = importer.getDataFrame()
            self.pt.updateModel(TableModel(updatedDataframe))
            self.pt.redraw()
            self.updateDialect(self.dialect)

    def updateDialect(self, dialect: detector.Dialect):
        """
        updates the dialect text fields from the gui
        :param dialect: the new changed dialect
        """
        # updates the dialect data
        self.encodingText.delete(1.0, END)
        self.encodingText.insert(1.0, dialect.encoding)

        self.hasHeaderVar.set(dialect.hasHeader)

        self.seperatorText.delete(1.0, END)
        self.seperatorText.insert(1.0, dialect.delimiter)

        self.quoteCharText.delete(1.0, END)
        self.quoteCharText.insert(1.0, dialect.quoteChar)
