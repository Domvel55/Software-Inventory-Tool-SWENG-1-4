'''
    This is the main.py class for the Software Inventory Tool Project
    This is the main file that will generate the whole of the GUI
    This file imports from the PageClasses.py and tkinter_custom_button files
    This file was entirely made by the Puffins Team
    Version:10.20.2021
'''
import PageClasses
from PageClasses import *
from PageClasses import root as root

# Window background color
root.configure(background="#2a3439")

# Scaling UI to user's screen
app_width = 1064
app_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

root.resizable(True, True)

# Changes the default tkinter to our Sieve logo when minimized
root.iconbitmap('logo.ico')

# Change the text after minimizing the tool to task bar
root.title("Sieve")

# Removes title bar
root.overrideredirect(True)
root.update_idletasks()
root.minimized = False  # only to know if root is minimized
root.maximized = False  # only to know if root is maximized

# Create New Title Bar


# 'Binding the title bar
PageClasses.title_bar.bind("<Map>", frame_mapped)

close_button = Button(title_bar, text='  ×  ', command=root.destroy, bg="#1f262A", padx=2, pady=2,
                      font=("calibre", 13),
                      bd=0, fg='white', highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', bg="#1f262A", padx=2, pady=2, bd=0, fg='white',
                       font=("calibre", 13), highlightthickness=0)
minimize_button = Button(title_bar, text=' — ', bg="#1f262A", padx=2, pady=2, bd=0, fg='white',
                         font=("calibre", 13), highlightthickness=0)
title_bar_title = Label(title_bar, text="Software Inventory Tool", bg="#1f262A", bd=0, fg='white',
                        font=("helvetica", 15),
                        highlightthickness=0)

root_sizegrip = ttk.Sizegrip(master=root)
minimize_button.bind("<Button-1>", minimizer)
expand_button.bind("<Button-1>", maximize_me)

# Packing the title_bar with all the buttons
title_bar.pack(fill=X)
close_button.pack(side=RIGHT, ipadx=7, ipady=1)
expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
title_bar_title.pack(side=RIGHT, padx=220)
#Maybe scale using title_bar.winfo_width()?

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


def init_data():
    CVEDataFrame().create_metadata()


def call_main():
    init_data()
    LoginPage()


if __name__ == '__main__':
    call_main()
    read_config()
    root.mainloop()
    write_config()
