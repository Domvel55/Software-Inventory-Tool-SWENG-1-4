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
    root.minimized = False  # only to know if root is minimized
    root.maximized = False  # only to know if root is maximized

    # Create New Title Bar
    title_bar = Frame(root, bg="#1F262A", relief="raised", bd=1)
    title_bar.pack(fill=X)

    # 'Binding the title bar
    title_bar.bind("<Map>", frame_mapped)

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
                                      text="Full Scan",
                                      text_color="white",
                                      corner_radius=10,
                                      width=90,
                                      height=40,
                                      hover=True,
                                      command=lambda: ResultsPage())
    scan_button.place(relx=.04, rely=.1)

    # Create Express Scan Button
    express_scan_button = TkinterCustomButton(master=root, bg_color="#2a3439",
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
    express_scan_button.place(relx=.15, rely=.1)

    close_button = Button(title_bar, text='  ×  ', command=root.destroy, bg="#1f262A", padx=2, pady=2,
                          font=("calibre", 13),
                          bd=0, fg='white', highlightthickness=0)
    expand_button = Button(title_bar, text=' 🗖 ', bg="#1f262A", padx=2, pady=2, bd=0, fg='white',
                           font=("calibre", 13), highlightthickness=0)
    minimize_button = Button(title_bar, text=' — ', bg="#1f262A", padx=2, pady=2, bd=0, fg='white',
                             font=("calibre", 13), highlightthickness=0)
    title_bar_title = Label(title_bar, text="Software Inventory Tool", bg="#1f262A", bd=0, fg='white',
                            font=("helvetica", 10),
                            highlightthickness=0)
    minimize_button.bind("<Button-1>", minimizer)
    expand_button.bind("<Button-1>", maximize_me)

    # Packing the title_bar with all the buttons
    title_bar.pack(fill=X)
    close_button.pack(side=RIGHT, ipadx=7, ipady=1)
    expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
    minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
    title_bar_title.pack(side=LEFT, padx=10)

    # Functions to change the color of buttons when hovered over
    def changex_on_hovering(event):
        close_button.configure(bg="red")

    def returnx_to_normalstate(event):
        close_button.configure(bg="#1f262A")

    def change_size_on_hovering(event):
        expand_button.configure(bg="#2a3439")

    def return_size_on_hovering(event):
        expand_button.configure(bg="#1f262A")

    def changem_size_on_hovering(event):
        minimize_button.configure(bg="#2a3439")

    def returnm_size_on_hovering(event):
        minimize_button.configure(bg="#1f262A")

    def change_text_on_click(e):
        if expand_button.cget("text") == " 🗗 ":
            expand_button.configure(text=" 🗖 ")
        else:
            expand_button.configure(text=" 🗗 ")
        maximize_me(e)

    def get_pos(e):  # this is executed when the title bar is clicked to move the window

        if not root.maximized:

            xwin = root.winfo_x()
            ywin = root.winfo_y()
            startx = e.x_root
            starty = e.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(e):  # runs when window is dragged
                root.config(cursor="fleur")
                root.geometry(f'+{e.x_root + xwin}+{e.y_root + ywin}')

            def release_window(e):  # runs when window is released
                root.config(cursor="arrow")

            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)

        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized

    title_bar.bind('<Button-1>', get_pos)  # so you can drag the window from the title bar
    title_bar_title.bind('<Button-1>', get_pos)  # so you can drag the window from the title

    # Binding buttons to Function to change color if hovered over
    close_button.bind('<Enter>', changex_on_hovering)
    close_button.bind('<Leave>', returnx_to_normalstate)
    expand_button.bind('<Enter>', change_size_on_hovering)
    expand_button.bind('<Leave>', return_size_on_hovering)
    expand_button.bind('<Button-1>', change_text_on_click)
    minimize_button.bind('<Enter>', changem_size_on_hovering)
    minimize_button.bind('<Leave>', returnm_size_on_hovering)

    root.mainloop()


def call_main():
    MainWindow()
    create_window()


if __name__ == '__main__':
    MainWindow()
    create_window()