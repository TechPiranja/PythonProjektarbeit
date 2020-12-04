from tkinter import *

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


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
    root.mainloop()

