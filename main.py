import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter_custom_button import TkinterCustomButton


class MainWindow:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#2a3439")


class ResultsPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#2a3439")


class HelpPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#2a3439")


class SettingsPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        settings_frame = tk.Frame(root)
        settings_frame.place(relx=0.5, rely=0.5, anchor='center')
        settings_frame.config(height=300, width=500)
        settings_frame.config(relief=RIDGE)

        settings_page_label = ttk.Label(settings_frame, text='Settings Page')
        settings_page_label.place(relx=0.5, rely=0.15, anchor='center')

        set_options_frame = ttk.Frame(settings_frame)
        set_options_frame.place(relx=0.5, rely=0.5, anchor='center')
        set_options_frame.config(height=300, width=500)
        set_options_frame.config(relief=RIDGE)
        set_options_frame.config(padding=(30, 15))

        set1_label = ttk.Label(set_options_frame, text='Setting 1')
        set1_label.grid(row=0, column=0)
        set2_label = ttk.Label(set_options_frame, text='Setting 2')
        set2_label.grid(row=1, column=0)
        set3_label = ttk.Label(set_options_frame, text='Setting 3')
        set3_label.grid(row=2, column=0)


root = tk.Tk()


def create_window():
    # root = tk.Tk()

    # Initialize the first window
    MainWindow()

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
    home_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 14",
                                          text="Home",
                                          text_color="white",
                                          corner_radius=0,
                                          width=75,
                                          height=40,
                                          hover=True,
                                          command=lambda: MainWindow())
    home_button.pack(side=LEFT, padx=5)

    # Results Button here

    # Create Settings Button
    settings_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                      fg_color="#1F262A",
                                      hover_color="#2a3439",
                                      text_font="Bold, 14",
                                      text="Settings",
                                      text_color="white",
                                      corner_radius=0,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: SettingsPage())
    settings_button.pack(side=LEFT, padx=5)

    # Create Help Button
    help_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                      fg_color="#1F262A",
                                      hover_color="#2a3439",
                                      text_font="Bold, 14",
                                      text="Help",
                                      text_color="white",
                                      corner_radius=0,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: HelpPage())
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


if __name__ == '__main__':
    create_window()
    #main = mainloop()