import tkinter as tk
from tkinter import *


def create_window():
    root = tk.Tk()
    root.title('Software Inventory Tool')
    root.geometry("1000x800")
    root.configure(background="#2a3439")
    root.minsize(750,600)

    """
    button = tk.Button(
        text="Click me!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
    )
    """

    #button.pack()


if __name__ == '__main__':
    create_window()
    main=mainloop()
