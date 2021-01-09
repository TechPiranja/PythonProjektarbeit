from tkinter import Tk
from importer_GUI import ImporterGUI

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title("Table Importer")
        ImporterGUI(self.root)
        self.root.mainloop()

if __name__ == '__main__':
    Main()

#TODO: doxygen + graphviz
#  doxywizardinstallieren