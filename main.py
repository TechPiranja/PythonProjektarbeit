from tkinter import Tk
from importer_GUI import ImporterGUI


class Main:
    """
    this is the main entrance of the table importer program, it creates the root tk and initializes the importer gui
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Table Importer")
        ImporterGUI(self.root)
        self.root.mainloop()


if __name__ == '__main__':
    Main()
