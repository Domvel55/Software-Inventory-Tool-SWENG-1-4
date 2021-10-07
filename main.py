import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter_custom_button import TkinterCustomButton


class MainWindow():
    def init(self, root):
        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#2a3439")


def create_window():
    root = tk.Tk()

    # Initialize all windows
    MainWindow().init(root)
    HelpPage().init(root)
    SettingsPage().init(root)

    # Window background color
    root.configure(background="#2a3439")

    # Not sure really
    # frame = tk.Frame(root)
    # frame.pack()

    # Scaling UI to user's screen
    app_width = 1000
    app_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    # remove title bar
    root.overrideredirect(True)

    #
    def move_app(e):
        root.geometry(f'+{e.x_root}+{e.y_root}')

    #
    def quitter(e):
        root.quit()
        root.destroy()

    #
    def minimizer(e):
        root.overrideredirect(0)
        root.iconify()

    # Create New Title Bar
    title_bar = Frame(root, bg="#1F262A", relief="raised", bd=1)
    title_bar.pack(fill=X)

    # 'Binding the title bar
    title_bar.bind("<B1-Motion>", move_app)

    # Navigation Buttons
    home_button = tk.Button(title_bar, text='Home', command=lambda: MainWindow().init(root))
    home_button.pack(side=LEFT, padx=5)

    # Results Button here

    # Create Settings Button
    settingsButton = tk.Button(title_bar, text="Settings", command=lambda: SettingsPage().init(root))
    settingsButton.pack(side=LEFT, padx=5)

    # Future version
    # help_button = TkinterCustomButton(title_bar, text='Help', command=lambda: HelpPage().init(root))

    help_button = tk.Button(title_bar, text='Help', command=lambda: HelpPage().init(root))
    help_button.pack(side=LEFT, padx=5)

    # Will need to fix where the label is placed (there is not center align ugh)
    # Create Title Text
    title_label = Label(title_bar, text="Software Inventory Tool", bg="#1F262A", fg="white")
    title_label.pack(side=LEFT, pady=4, padx=100)

    # Create close button
    close_label = Label(title_bar, text="X", bg="#1f262A", fg="white", font=("", 16), relief="raised", bd=0)
    close_label.pack(side=RIGHT, padx=4, pady=4)
    close_label.bind("<Button-1>", quitter)

    # Create Minimize button
    minimize_label = Label(title_bar, text="─", bg="#1f262A", fg="white", font=("", 16), relief="raised", bd=0)
    minimize_label.pack(side=RIGHT, pady=4)
    minimize_label.bind("<Button-1>", minimizer)

    root.mainloop()


class HelpPage():

    def init(self, root):
        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#fff000")


class SettingsPage():

    def init(self, root):
        settingsFrame = ttk.Frame(root)
        settingsFrame.place(relx=0.5, rely=0.5, anchor='center')
        settingsFrame.config(height=300, width=500)
        settingsFrame.config(relief=RIDGE)

        settingsPageLabel = ttk.Label(settingsFrame, text='Settings Page')
        settingsPageLabel.place(relx=0.5, rely=0.15, anchor='center')

        setOptionsFrame = ttk.Frame(settingsFrame)
        setOptionsFrame.place(relx=0.5, rely=0.5, anchor='center')
        setOptionsFrame.config(height=300, width=500)
        setOptionsFrame.config(relief=RIDGE)
        setOptionsFrame.config(padding=(30, 15))

        set1label = ttk.Label(setOptionsFrame, text='Setting 1')
        set1label.grid(row=0, column=0)
        set2label = ttk.Label(setOptionsFrame, text='Setting 2')
        set2label.grid(row=1, column=0)
        set3label = ttk.Label(setOptionsFrame, text='Setting 3')
        set3label.grid(row=2, column=0)


if __name__ == '__main__':
    create_window()
    #main = mainloop()
