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
    LoginPage().init(root)

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

    # Create Login Button
    login_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                      fg_color="#1F262A",
                                      hover_color="#2a3439",
                                      text_font="Bold, 14",
                                      text="Login",
                                      text_color="white",
                                      corner_radius=0,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: LoginPage().init(root))
    login_button.pack(side=LEFT, padx=5)

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


class LoginPage():

    def init(self, root):
        root.configure(background="#2a3439")
        login_style = ttk.Style()
        login_style.configure('Login.TFrame', background="#2a3439", foreground="white")
        login_style.configure('Login.TLabel', background="#2a3439", foreground="white")

        login_frame = Frame(root, bg='#1F262A')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        login_frame.config(height=300, width=500)
        login_frame.config(relief=RAISED)

        login_page_label = Label(login_frame, text='Login Page', font="Bold, 20", bg='#1F262A', fg="white")
        login_page_label.place(relx=0.5, rely=0.15, anchor='center')

        login_options_frame = ttk.Frame(login_frame, style='Login.TFrame')
        login_options_frame.place(relx=0.5, rely=0.5, anchor='center')
        #login_options_frame.config(relief=RAISED)
        login_options_frame.config(padding=(90, 45))

        username_label = ttk.Label(login_options_frame, text='Username', style='Login.TLabel')
        username_label.grid(row=0, column=0)
        set2_label = ttk.Label(login_options_frame, text='', style='Login.TLabel')
        set2_label.grid(row=1, column=0)
        token_label = ttk.Label(login_options_frame, text='RSA Token', style='Login.TLabel')
        token_label.grid(row=2, column=0)


        login_button = TkinterCustomButton( bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 10",
                                          text="Login",
                                          text_color="white",
                                          corner_radius=0,
                                          width=50,
                                          height=20,
                                          hover=True,
                                          command=lambda: LoginPage().init(root))
        login_button.place(relx=0.45, rely=0.65, anchor='center')

        register_button = TkinterCustomButton( bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 10",
                                          text="Register",
                                          text_color="white",
                                          corner_radius=0,
                                          width=55,
                                          height=20,
                                          hover=True,
                                          command=lambda: LoginPage().init(root))
        register_button.place(relx=0.55, rely=0.65, anchor='center')


if __name__ == '__main__':
    create_window()
    #main = mainloop()