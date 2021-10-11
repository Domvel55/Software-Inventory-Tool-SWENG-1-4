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

    # Results Button here
    results_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                      fg_color="#1F262A",
                                      hover_color="#2a3439",
                                      text_font="Bold, 14",
                                      text="Results",
                                      text_color="white",
                                      corner_radius=0,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: ResultsPage().init(root))
    results_button.pack(side=LEFT, padx=5)

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

    # Create Scan
    scan_button = TkinterCustomButton(master=root, bg_color=None,
                                      fg_color="#1F262A",
                                      hover_color="#2a3439",
                                      text_font="Bold, 14",
                                      text="Scan",
                                      text_color="white",
                                      corner_radius=0,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: ResultsPage().init(root))
    scan_button.place(relx=.05, rely=.1)

    # Create Title Text
    title_label = Label(title_bar, text="Software Inventory Tool", font="Bold, 10", bg="#1F262A", fg="white")
    title_label.place(relx=.5, rely=.5, anchor="center")

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
        root.configure(background="#5B676D")


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

        login_outer_frame = Frame(root, bg='#1F262A')
        login_outer_frame.place(relx=0.5, rely=0.5, anchor='center')
        login_outer_frame.config(height=400, width=600)
        login_outer_frame.config(relief=RAISED)

        login_inner_frame = Frame(root, background="#2a3439")
        login_inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        login_inner_frame.config(height=300, width=500)

        login_page_label = Label(root, text='Login Page', font="Bold, 20", bg='#2a3439', fg="white")
        login_page_label.place(relx=0.5, rely=0.3, anchor='center')

        username_label = Label(root, text='Username', font=15, background="#2a3439", foreground="white")
        username_label.place(relx=0.5, rely=0.4, anchor="center")
        username_entry = Entry(root, background="#1F262A", foreground="white", font=15)
        username_entry.place(relx=0.5, rely=0.45, anchor='center')
        token_label = Label(root, text='RSA Token', font=15, background="#2a3439", foreground="white")
        token_label.place(relx=0.5, rely=0.515, anchor='center')
        token_entry = Entry(root, background="#1F262A", foreground="white", font=15)
        token_entry.place(relx=0.5, rely=0.565, anchor='center')

        #Login Button
        login_button = TkinterCustomButton( bg_color=None,
                                          fg_color="#56667A",
                                          hover_color="#AAA9AD",
                                          text_font="Bold, 12",
                                          text="Login",
                                          text_color="white",
                                          corner_radius=0,
                                          width=80,
                                          height=40,
                                          hover=True,
                                          command=lambda: MainWindow().init(root))
        login_button.place(relx=0.45, rely=0.65, anchor='center')

        #Registration Button
        register_button = TkinterCustomButton( bg_color=None,
                                          fg_color="#56667A",
                                          hover_color="#AAA9AD",
                                          text_font="Bold, 12",
                                          text="Register",
                                          text_color="white",
                                          corner_radius=0,
                                          width=80,
                                          height=40,
                                          hover=True,
                                          command=lambda: RegisterPage().init(root))
        register_button.place(relx=0.55, rely=0.65, anchor='center')

class RegisterPage():

    def init(self, root):
        root.configure(background="#2a3439")

        register_frame = Frame(root, bg='#1F262A')
        register_frame.place(relx=0.5, rely=0.5, anchor='center')
        register_frame.config(height=300, width=500)
        register_frame.config(relief=RAISED)

        register_title = Label(root, text="Register", background="#1F262A", foreground="white", font="Bold, 25")
        register_title.place(relx=0.5, rely=.3, anchor='center')
        first_name = Label(root, text="First Name", background="#1F262A", foreground="white", font=20)
        first_name.place(relx=.34, rely=.38)
        first_name_entry = Entry(root, background="#2a3439", foreground="white", width=25, font=20)
        first_name_entry.place(relx=.45, rely=.38)
        last_name = Label(root, text="Last Name", background="#1F262A", foreground="white", font=20)
        last_name.place(relx=.34, rely=.46)
        last_name_entry = Entry(root, background="#2a3439", foreground="white", width=25, font=20)
        last_name_entry.place(relx=.45, rely=.46)
        username = Label(root, text="Username", background="#1F262A", foreground="white", font=20)
        username.place(relx=.34, rely=.54)
        username_entry = Entry(root, background="#2a3439", foreground="white", width=25, font=20)
        username_entry.place(relx=.45, rely=.54)
        token = Label(root, text="RSA Token ID", background="#1F262A", foreground="white", font=20)
        token.place(relx=.34, rely=.62)
        token_entry = Entry(root, background="#2a3439", foreground="white", width=25, font=20)
        token_entry.place(relx=.45, rely=.62)

        login_button = TkinterCustomButton( bg_color=None,
                                          fg_color="#56667A",
                                          hover_color="#AAA9AD",
                                          text_font= 20,
                                          text="Create",
                                          text_color="white",
                                          corner_radius=0,
                                          width=100,
                                          height=30,
                                          hover=True,
                                          command=lambda: LoginPage().init(root))
        login_button.place(relx=0.5, rely=0.73, anchor='center')



if __name__ == '__main__':
    create_window()
    #main = mainloop()