from PageClasses import *
from PageClasses import root as root


def create_window():

    # Window background color
    root.configure(background="#2a3439")

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
                                      command=lambda: call_main())
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
                                       command=lambda: LoginPage())
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
                                         command=lambda: ResultsPage())
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

    # Create Scan
    scan_button = TkinterCustomButton(master=root, bg_color="#2a3439",
                                      fg_color="#1F262A",
                                      hover_color="#AAA9AD",
                                      text_font="Bold, 14",
                                      text="Scan",
                                      text_color="white",
                                      corner_radius=10,
                                      width=75,
                                      height=40,
                                      hover=True,
                                      command=lambda: ResultsPage())
    scan_button.place(relx=.05, rely=.1)

    # Create Express Scan Button
    scan_button = TkinterCustomButton(master=root, bg_color="#2a3439",
                                      fg_color="#1F262A",
                                      hover_color="#AAA9AD",
                                      text_font="Bold, 14",
                                      text="Express Scan",
                                      text_color="white",
                                      corner_radius=10,
                                      width=130,
                                      height=40,
                                      hover=True,
                                      command=lambda: ResultsPage())
    scan_button.place(relx=.15, rely=.1)

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


def call_main():
    MainWindow()
    create_window()


if __name__ == '__main__':
    MainWindow()
    create_window()