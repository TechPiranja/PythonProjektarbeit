from tkinter import END, Tk, Label, Frame, Text, SUNKEN, Button, TRUE, TOP
from tkinter.filedialog import askopenfilenames
from pandastable import Table, TableModel
import detector
import exporter_GUI
from importer import Importer

importer = Importer()


class ImporterGUI:
    def __init__(self, root: Tk):
        self.root = root
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.pt = Table(self.frame2)

        h1 = Label(self.root, text="Datendateien", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        # Dialog Frame
        dialogFrame = Frame(self.root)

        open_btn = Button(dialogFrame, text="Datendateien öffnen", command=self.openFileDialog, width=20, padx=0)
        open_btn.grid(row=0, column=0)
        deleteAll_btn = Button(dialogFrame, text="Alle entfernen", command=self.deleteSelectedFiles, width=20, padx=0)
        deleteAll_btn.grid(row=1, column=0)
        self.selectedFiles = Text(dialogFrame, height=4, borderwidth=2, relief=SUNKEN)
        self.selectedFiles.grid(row=0, column=1, rowspan=2)
        dialogFrame.pack(fill="x", padx=5)

        # Detector Frame
        h1 = Label(root, text="Detector", bg="#eee")
        h1.pack(padx=5, pady=5, fill="x")

        detectorFrame = Frame(root)

        Label(detectorFrame, text="CSV-Zeichenkodierung:", width=20, anchor="w", justify="left", padx=0).grid(row=0,
                                                                                                              column=0)
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
        vorschau = Label(root, text="Vorschau", bg="#eee")
        vorschau.pack(expand=TRUE, fill="x", padx=5, side=TOP)
        self.pt.show()
        self.frame2.pack(pady=10, padx=5, fill="both", side=TOP)

        exportBtn = Button(root, text="Exportieren", command=self.export, width=20, padx=0)
        exportBtn.pack(fill="x", padx=10, pady=10)

    def openFileDialog(self):
        files = list(askopenfilenames(parent=self.root, title='Choose a file'))
        self.updateDf(files)

    def deleteSelectedFiles(self):
        self.selectedFiles.delete(1.0, END)

    def getSelectedFiles(self):
        return self.selectedFiles.get(1.0, END)

    def export(self):
        exporter_GUI.initExportDialog(self.root, self.pt)

    def updateDf(self, files: list):
        # TODO: Sniffer can only be used on csv?!
        if files[0].endswith(".csv"):
            dialect = detector.Dialect()
            dialect.guessDialectCSV(files[0])

            importer.importCSV(files[0], dialect)
            updatedDataframe = importer.getDataFrame()
            self.pt.updateModel(TableModel(updatedDataframe))
            self.pt.redraw()

            # TODO use CSV Merge Method ( not implemented yet )
            self.selectedFiles.insert(END, files)  # TODO: import without {} brackets
            self.encodingText.insert(1.0, dialect.encoding)
            self.hasHeaderText.insert(1.0, dialect.hasHeader)
            self.seperatorText.insert(1.0, dialect.delimiter)
            self.quoteCharText.insert(1.0, dialect.quotechar)
        elif files[0].endswith(".xml") or files[0].endswith(".xsl"):
            self.selectedFiles.insert(END, files)
            xmlFile = files[0]
            xslFile = files[1]
            dialect = importer.importXML(xmlFile, xslFile)
            self.hasHeaderText.insert(1.0, dialect.hasHeader)
            self.seperatorText.insert(1.0, dialect.delimiter)
            self.quoteCharText.insert(1.0, dialect.quotechar)
            self.encodingText.insert(1.0, "XSLT")
            updatedDataframe = importer.getDataFrame()
            self.pt.updateModel(TableModel(updatedDataframe))
            self.pt.redraw()
