from tkinter import END, Tk, Label, Frame, Text, SUNKEN, Button, TRUE, TOP, Listbox, SINGLE, Scrollbar, Entry
from tkinter.filedialog import askopenfilenames
from pandastable import Table, TableModel
import detector
import exporter_GUI
from importer import Importer
from merger import Merger

importer = Importer()
merger = Merger()

class ImporterGUI:
    def __init__(self, root: Tk):
        self.root = root
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.pt = Table(self.frame2)
        self.dialect = detector.Dialect()

        h1 = Label(self.root, text="Imported Files", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        # Dialog Frame
        dialogFrame = Frame(self.root)
        dialogFrame.grid_columnconfigure(1, weight=1)
        open_btn = Button(dialogFrame, text="Import Files", command=self.openFileDialog, width=20)
        open_btn.grid(row=0, column=0)
        open_btn = Button(dialogFrame, text="Delete selected File", command=self.deleteSelectedFile, width=20)
        open_btn.grid(row=1, column=0)
        deleteAll_btn = Button(dialogFrame, text="Delete all", command=self.deleteAllFiles, width=20)
        deleteAll_btn.grid(row=2, column=0)

        listbox_border = Frame(dialogFrame, bd=2, relief="sunken", background="white")
        listbox_border.grid(row=0, column=1, rowspan=3, padx=3, sticky="nsew")

        self.selectedFiles = Listbox(listbox_border, selectmode=SINGLE, height=4, borderwidth=0, highlightthickness=0, relief=SUNKEN, background="white")

        def selectionChanged(event):
            selection = event.widget.curselection()
            if selection:
                data = event.widget.get(selection[0])
                if data.endswith(".xml"):
                    self.importXSL_btn["state"] = "normal"
                    if any(data in x for x in self.XMLList):
                        x = [x for x in self.XMLList if data in x][0]
                        self.XSLPath_text.insert(1.0, self.XMLList[self.XMLList.index(x)][1])
                    else:
                        self.XSLPath_text.insert(1.0, "please import a XSL File!")
                else:
                    self.importXSL_btn["state"] = "disabled"
                    self.XSLPath_text.delete(1.0, END)

        self.selectedFiles.bind("<<ListboxSelect>>", selectionChanged)

        vsb = Scrollbar(listbox_border, orient="vertical", command=self.selectedFiles.yview)
        self.selectedFiles.configure(yscrollcommand=vsb)
        vsb.pack(side="right", fill="y")
        self.selectedFiles.pack(padx=2, pady=2, fill="both", expand=True)

        dialogFrame.pack(fill="x", padx=5)

        # XML XLS Frame
        h1 = Label(root, text="XSL File", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        xmlFrame = Frame(root)

        self.importXSL_btn = Button(xmlFrame, state=DISABLED, text="Import XSL File", command=self.openXSLFileDialog, width=20)
        self.importXSL_btn.grid(row=0, column=0)
        self.XSLPath_text = Text(xmlFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.XSLPath_text.grid(row=0, column=1)

        xmlFrame.pack(fill="x", padx=5, pady=5)

        # Detector Frame
        h1 = Label(root, text="Detector", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        detectorFrame = Frame(root)

        Label(detectorFrame, text="Encoding:", width=20, anchor="w", justify="left", padx=0).grid(row=0, column=0)
        self.encodingText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.encodingText.grid(row=0, column=1)

        Label(detectorFrame, text="Has Header:", width=20, anchor="w", justify="left", padx=0).grid(row=1, column=0)
        self.hasHeaderText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.hasHeaderText.grid(row=1, column=1)

        Label(detectorFrame, text="Seperator:", width=20, anchor="w", justify="left", padx=0).grid(row=2, column=0)
        self.seperatorText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.seperatorText.grid(row=2, column=1)

        Label(detectorFrame, text="Quote Char:", width=20, anchor="w", justify="left", padx=0).grid(row=3, column=0)
        self.quoteCharText = Text(detectorFrame, height=1, borderwidth=2, relief=SUNKEN)
        self.quoteCharText.grid(row=3, column=1)

        detectorFrame.pack(fill="x", padx=5, pady=5)

        # Vorschau und Pandastable
        vorschau = Label(root, text="Preview", bg="#eee")
        vorschau.pack(expand=TRUE, fill="x", padx=5, side=TOP)
        self.pt.show()
        self.frame2.pack(pady=10, padx=5, fill="both", side=TOP)

        exportBtn = Button(root, text="Export", command=self.export, width=20, padx=0)
        exportBtn.pack(fill="x", padx=10, pady=10)

    def openFileDialog(self):
        files = list(askopenfilenames(parent=self.root, title='Choose a file'))
        self.updateSelectedFiles(files)
        self.updateDf(self.getSelectedFiles())

    #TODO: finish this
    def deleteSelectedFile(self):
        path = self.selectedFiles.get(self.selectedFiles.curselection())
        index = self.selectedFiles.get(0, END).index(path)
        self.selectedFiles.delete(index)
        self.updateDf(self.getSelectedFiles())

    def deleteAllFiles(self):
        self.selectedFiles.delete(0, END)

    def getSelectedFiles(self):
        return self.selectedFiles.get(0, END)

    def updateSelectedFiles(self, files):
        startIndex = self.selectedFiles.size()
        for index, file in enumerate(files):
            self.selectedFiles.insert(index + startIndex, file)

    def export(self):
        #get updated df if changes where made in the pandastable
        importer.setDataFrame(self.pt.model.df)
        exporter_GUI.initExportDialog(self.root, importer, self.dialect)

    def updateDf(self, files: list):
        if files[0].endswith(".xml") and files[1].endswith(".xsl"):
            xmlFile = files[0]
            xslFile = files[1]
            importer.importXML(xmlFile, xslFile)
            self.dialect = importer.dialect

            self.hasHeaderText.delete(1.0, END)
            self.hasHeaderText.insert(1.0, self.dialect.hasHeader)

            self.seperatorText.delete(1.0, END)
            self.seperatorText.insert(1.0, self.dialect.delimiter)

            self.quoteCharText.delete(1.0, END)
            self.quoteCharText.insert(1.0, self.dialect.quotechar)
            self.encodingText.insert(1.0, "XSLT")
            updatedDataframe = importer.getDataFrame()
            self.pt.updateModel(TableModel(updatedDataframe))
            self.pt.redraw()

        elif len(files) > 1:
            #MERGE FILES
            #TODO: merge xml mit csv
            canMerge = merger.isMergePossible(files)
            if canMerge:
                newDataFrame = merger.mergeCSVFiles(files)
                importer.setDataFrame(newDataFrame)
                self.pt.updateModel(TableModel(newDataFrame))
                self.pt.redraw()
            else:
                self.deleteAllFiles()

        elif files[0].endswith(".csv"):
            self.dialect.guessDialectCSV(files[0])

            importer.importCSV(files[0], self.dialect)
            updatedDataframe = importer.getDataFrame()
            self.pt.updateModel(TableModel(updatedDataframe))
            self.pt.redraw()

            # TODO use CSV Merge Method ( not implemented yet )
            self.encodingText.delete(1.0, END)
            self.encodingText.insert(1.0, self.dialect.encoding)

            self.hasHeaderText.delete(1.0, END)
            self.hasHeaderText.insert(1.0, self.dialect.hasHeader)

            self.seperatorText.delete(1.0, END)
            self.seperatorText.insert(1.0, self.dialect.delimiter)

            self.quoteCharText.delete(1.0, END)
            self.quoteCharText.insert(1.0, self.dialect.quotechar)
