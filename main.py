from tkinter import Tk
from importer_GUI import ImporterGUI

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tabelle importieren")
        ImporterGUI(self.root)
        self.root.mainloop()

if __name__ == '__main__':
    Main()


