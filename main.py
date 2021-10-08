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

    # Initialize Main Window
    MainWindow().init(root)

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
                                          command=lambda: MainWindow().init(root))
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
                                      command=lambda: SettingsPage().init(root))
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
                                      command=lambda: HelpPage().init(root))
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

    # Create Express Scan Button
    expressScanButton = tk.Button(root, text="Express Scan")
    expressScanButton.place(relx=0.65, rely=0.85)

    root.mainloop()

class ResultsPage():

    def init(self, root):
        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#fff000")


class HelpPage():

    def init(self, root):
        # root.geometry("600x600")
        # root.minsize(750, 600)
        root.configure(background="#fff000")


class SettingsPage():

    def init(self, root):
        settings_frame = ttk.Frame(root)
        settings_frame.place(relx=0.5, rely=0.5, anchor='center')
        settings_frame.config(height=500, width=700)
        settings_frame.config(relief=RIDGE)

        settings_page_label = ttk.Label(settings_frame, text='Settings Page')
        settings_page_label.place(relx=0.5, rely=0.15, anchor='center')

        set_options_frame = ttk.Frame(settings_frame)
        set_options_frame.place(relx=0.5, rely=0.5, anchor='center')
        set_options_frame.config(height=300, width=500)
        set_options_frame.config(relief=RIDGE)
        set_options_frame.config(padding=(30, 15))

        set_1_label = ttk.Label(set_options_frame, text='Text size')
        set_1_label.grid(row=0, column=0, padx=50, pady=30)
        decrease_txt_size_button = ttk.Button(set_options_frame, text='-')
        decrease_txt_size_button.grid(row=0, column=1)
        txt_size_entry = ttk.Entry(set_options_frame, width=5)
        txt_size_entry.grid(row=0, column=2)
        txt_size_entry.insert(0, '12')
        increase_txt_size_button = ttk.Button(set_options_frame, text='+')
        increase_txt_size_button.grid(row=0, column=3)

        set_2_label = ttk.Label(set_options_frame, text='Sort scan results...')
        set_2_label.grid(row=1, column=0, padx=50)
        sort_order = StringVar()
        set_2_button_1 = ttk.Radiobutton(set_options_frame, text='By severity', variable = sort_order, value = 'severity')
        set_2_button_1.grid(row=1, column=2)
        set_2_button_2 = ttk.Radiobutton(set_options_frame, text='In order discovered', variable = sort_order, value = 'discovered')
        set_2_button_2.grid(row=2, column=2)

        set_3_label = ttk.Label(set_options_frame, text='Choose directories to ignore:')
        set_3_label.grid(row=3, column=0, padx=50, pady=30)
        set_3_button = ttk.Button(set_options_frame, text='Browse...')
        set_3_button.grid(row=3, column=2)

        set_4_label = ttk.Label(set_options_frame, text='When scan finishes...')
        set_4_label.grid(row=4, column=0, padx=50)
        after_scan = StringVar()
        set_4_button_1 = ttk.Radiobutton(set_options_frame, text='Do Nothing', variable = after_scan, value = 'nothing')
        set_4_button_1.grid(row=4, column=2)
        set_4_button_2 = ttk.Radiobutton(set_options_frame, text='Close the program', variable = after_scan, value = 'close')
        set_4_button_2.grid(row=5, column=2)
        set_4_button_3 = ttk.Radiobutton(set_options_frame, text='Shut down computer', variable = after_scan, value = 'shut_down')
        set_4_button_3.grid(row=6, column=2)

        set_5_label = ttk.Label(set_options_frame, text='Reset Default Settings')
        set_5_label.grid(row=7, column=0, padx=50, pady=30)
        set_5_button = ttk.Button(set_options_frame, text='Reset')
        set_5_button.grid(row=7, column=2)

        apply_button = ttk.Button(settings_frame, text = 'Apply')
        apply_button.place(relx=0.5, rely=0.95, anchor='center')


if __name__ == '__main__':
    create_window()
    #main = mainloop()