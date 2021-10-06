import tkinter as tk
from tkinter import *


def create_window():
    root = tk.Tk()
    root.configure(bg="#2A3439")

    app_width = 1000
    app_height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)

    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    # remove title bar
    root.overrideredirect(True)

    def move_app(e):
        root.geometry(f'+{e.x_root}+{e.y_root}')

    def quitter(e):
        root.quit()
        root.destroy()

    def minimizer(e):
        root.overrideredirect(0)
        root.iconify()

    # Create New Title Bar
    title_bar = Frame(root, bg="#1F262A", relief="raised", bd=1)
    title_bar.pack(fill=X)
    # 'Binding the title bar
    title_bar.bind("<B1-Motion>", move_app)

    # Create Title Text
    title_lable = Label(title_bar, text="Software Inventory Tool", bg="#1F262A", fg="white")
    title_lable.pack(side=LEFT, pady=4, padx=425)

    # Create close button
    close_lable = Label(title_bar, text="X  ", bg="#1f262A", fg="white", relief="raised", bd=0)
    close_lable.pack(side=RIGHT, pady=4)
    close_lable.bind("<Button-1>", quitter)

    # Create Minimize button
    minimize_lable = Label(title_bar, text="---", bg="#1f262A", fg="white", relief="raised", bd=0)
    minimize_lable.pack(side=RIGHT, pady=4)
    minimize_lable.bind("<Button-1>", minimizer)

    root.mainloop()


if __name__ == '__main__':
    create_window()