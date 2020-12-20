from tkinter import *
from pandastable import Table
import exporter

def initExporterDialog(root: Tk, pt: Table):
    window = Toplevel(root)

    h1 = Label(window, text="Tabelle exportieren", bg="#eee")
    h1.pack(padx=5, pady=5, fill="x")
    exportBtn = Button(window, text="Exportieren", command=exporter.exportToCSV(pt), width=20, padx=0)
    exportBtn.pack(fill="x", padx=10, pady=10)