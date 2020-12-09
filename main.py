from tkinter import *
from importer import Importer

importer = Importer()

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def gui():
    root = Tk()
    root.title("Tabelle importieren")

    h1 = Label(root, text="Datendateien")
    h1.pack()
    open_btn = Button(root, text="Datendateien öffnen")
    open_btn.pack(padx=5, pady=10, side=LEFT)
    delete_btn = Button(root, text="Auswahl entfernen")
    delete_btn.pack(padx=5, pady=10, side=LEFT)
    deleteAll_btn = Button(root, text="Alle entfernen")
    deleteAll_btn.pack(padx=5, pady=10, side=LEFT)

if __name__ == '__main__':
    importer.importCSV()
    importer.convertToPandasDF()
    # root.mainloop()

