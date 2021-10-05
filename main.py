import tkinter as tk
from tkinter import *


def create_window():
    root = tk.Tk()
    root.title('Software Inventory Tool')

    mainWindow = tk.Label(
                background = "#2a3439",
                width = 192,
                height = 64
    )

    """
    button = tk.Button(
        text="Click me!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
    )
    """
    mainWindow.pack()
    #button.pack()


if __name__ == '__main__':
    create_window()
    main=mainloop()
