"""
    This is the PageClasses.py class for the Software Inventory Tool Project
    This is the file that contains all the different functions to create/destroy the different
    windows that generate from clicking buttons on the GUI
    This file was entirely made by the Puffins Team
    Version:10.20.2021
"""

from tkinter import *
from tkinter import ttk
from tkinter_custom_button import TkinterCustomButton
from Database import *
from tkinter import filedialog


root = Tk()


def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')


def quitter(e):
    root.quit()


def minimizer(e):
    root.update_idletasks()
    root.overrideredirect(False)
    root.state('iconic')


def maximize_me(e):
    if not root.maximized:  # if the window was not maximized
        root.normal_size = root.geometry()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized
        # now it's maximized

    else:  # if the window was maximized
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized


def frame_mapped(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')


class MainWindow:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        main_frame = Frame(root, bg="#2a3439")
        main_frame.place(relx=0.5, rely=0.1, anchor="n")
        main_frame.config(height=root.winfo_height(), width=root.winfo_width())

        # <editor-fold desc="Results Buttons">
        scan_button = TkinterCustomButton(master=main_frame,
                                          bg_color="#2a3439",
                                          fg_color="#1F262A",
                                          hover_color="#AAA9AD",
                                          text_font="Bold, 14",
                                          text="Full Scan",
                                          text_color="white",
                                          corner_radius=10,
                                          width=90,
                                          height=40,
                                          hover=True,
                                          command=lambda: FullScanConfirmPage())
        scan_button.place(relx=.01)

        express_scan_button = TkinterCustomButton(master=main_frame,
                                                  bg_color="#2a3439",
                                                  fg_color="#1F262A",
                                                  hover_color="#AAA9AD",
                                                  text_font="Bold, 14",
                                                  text="Express Scan",
                                                  text_color="white",
                                                  corner_radius=10,
                                                  width=130,
                                                  height=40,
                                                  hover=True,
                                                  command=lambda: ExpressScanConfirmPage())
        express_scan_button.place(relx=.12)

        schedule_scan_button = TkinterCustomButton(master=main_frame,
                                                  bg_color="#2a3439",
                                                  fg_color="#1F262A",
                                                  hover_color="#AAA9AD",
                                                  text_font="Bold, 14",
                                                  text="Schedule Scan",
                                                  text_color="white",
                                                  corner_radius=10,
                                                  width=130,
                                                  height=40,
                                                  hover=True,
                                                  command=lambda: ResultsPage())
        schedule_scan_button.place(relx=.27)
        # </editor-fold>

class FullScanConfirmPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        # Frame for scan confirmation dialog box
        scan_confirm_frame = tk.Frame(root, bg="#2a3439")
        scan_confirm_frame.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_frame.config(height=root.winfo_height(), width=root.winfo_width())

        scan_confirm_label = tk.Label(scan_confirm_frame, text='What will be scanned:', font=14, bg="#2a3439",
                                      fg="white")
        scan_confirm_label.place(relx=0.05, rely=0.05, anchor="w")

        # Container for confirmation dialog
        scan_confirm_container = tk.Frame(scan_confirm_frame, bg="#1F262A", borderwidth=2)
        scan_confirm_container.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_container.config(relief=RIDGE, height=250, width=700)

        full_scan_dialog = tk.Label(scan_confirm_container, text='Full Scan: All Program Files Will Be Scanned.',
                                      font=14, bg="#2a3439", fg="white")
        full_scan_dialog.place(relx=0.5, rely=0.5, anchor="center")

        continue_button = TkinterCustomButton(master=scan_confirm_frame,
                                                fg_color="#848689",
                                                hover_color="#1F262A",
                                                text_font="Bold, 14",
                                                text="Continue",
                                                text_color="white",
                                                corner_radius=10,
                                                width=200,
                                                height=75,
                                                hover=True,
                                                command=lambda: ResultsPage())
        continue_button.place(relx=0.25, rely=0.8, anchor="center")

        cancel_button = TkinterCustomButton(master=scan_confirm_frame,
                                            fg_color="#5F4866",
                                            hover_color="#1F262A",
                                            text_font="Bold, 14",
                                            text="Cancel",
                                            text_color="white",
                                            corner_radius=10,
                                            width=100,
                                            height=50,
                                            hover=True,
                                            command=lambda: MainWindow())
        cancel_button.place(relx=0.70, rely=0.8, anchor="center")

class ExpressScanConfirmPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        # Function for opening the
        # file explorer window
        def browseFiles():
            filenames = filedialog.askopenfilenames(initialdir="C:\Program Files",
                                                  title="Select Files",
                                                  filetypes=(("all files",
                                                              "*.*"),
                                                            ("Text files",
                                                              "*.txt*")))
            files_list = list(filenames)
            ctr = 0

            for file in files_list:
                file_block = tk.Frame(scan_confirm_container, bg="#2a3439")
                file_block.place(relx=0.5, rely=0.02, anchor="n")
                file_block.config(height=50, width=860)
                file_label = tk.Label(file_block, text=files_list[ctr], font=14, bg="#2a3439", fg="white",
                                      wraplength=845, justify='left')
                file_label.place(relx=0.01, rely=0.5, anchor="w")
                file_block.grid(row=ctr, column=0, padx=10, pady=5)

                ctr = ctr + 1

            if ctr > 6:
                scan_confirim_sb = ttk.Scrollbar(scan_confirm_canvas, orient="vertical",
                                                     command=scan_confirm_canvas.yview)
                scan_confirim_sb.place(relx=0.98, height = 350)
                scan_confirm_canvas.configure(yscrollcommand=scan_confirim_sb.set)


        root.configure(background="#2a3439")

        # Frame for scan confirmation dialog box
        scan_confirm_frame = tk.Frame(root, bg="#2a3439")
        scan_confirm_frame.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_frame.config(height=root.winfo_height(), width=root.winfo_width())

        scan_confirm_label = tk.Label(scan_confirm_frame, text='What will be scanned:', font=14, bg="#2a3439", fg="white")
        scan_confirm_label.place(relx=0.05, rely=0.05, anchor="w")

        scan_confirm_canvas = tk.Canvas(scan_confirm_frame, height=350, width=900, bg="#2a3439")
        scan_confirm_canvas.place(relx=0.5, rely=0.1, anchor="n")

        # Container for files to be scanned
        scan_confirm_container = tk.Frame(scan_confirm_canvas, bg="#1F262A", borderwidth=2)
        scan_confirm_container.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_container.config(relief=RIDGE, height=350, width=900)
        scan_confirm_container.bind(
            "<Configure>",
            lambda e: scan_confirm_canvas.configure(
                scrollregion=scan_confirm_canvas.bbox("all")
            )
        )
        scan_confirm_canvas.create_window((0, 0), window=scan_confirm_container, anchor="nw")


        continue_button = TkinterCustomButton(master=scan_confirm_frame,
                                                fg_color="#848689",
                                                hover_color="#1F262A",
                                                text_font="Bold, 14",
                                                text="Continue",
                                                text_color="white",
                                                corner_radius=10,
                                                width=200,
                                                height=75,
                                                hover=True,
                                                command=lambda: ResultsPage())
        continue_button.place(relx=0.25, rely=0.8, anchor="center")

        add_files_button = TkinterCustomButton(master=scan_confirm_frame,
                                                     fg_color="#8797AF",
                                                     hover_color="#1F262A",
                                                     text_font="Bold, 14",
                                                     text="Add Files",
                                                     text_color="white",
                                                     corner_radius=10,
                                                     width=200,
                                                     height=75,
                                                     hover=True,
                                                     command=lambda: browseFiles())
        add_files_button.place(relx=0.5, rely=0.8, anchor="center")

        cancel_button = TkinterCustomButton(master=scan_confirm_frame,
                                            fg_color="#5F4866",
                                            hover_color="#1F262A",
                                            text_font="Bold, 14",
                                            text="Cancel",
                                            text_color="white",
                                            corner_radius=10,
                                            width=100,
                                            height=50,
                                            hover=True,
                                            command=lambda: MainWindow())
        cancel_button.place(relx=0.70, rely=0.8, anchor="center")


class ResultsPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        # <editor-fold desc="Results GUI">
        # Frame for whole results page
        results_frame = Frame(root, bg="#2a3439")
        results_frame.place(relx=0.5, rely=0.1, anchor="n")
        results_frame.config(height=root.winfo_height(), width=root.winfo_width())

        # Container for results
        results_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
        results_container.place(relx=0.5, rely=0.1, anchor="n")
        results_container.config(relief=RIDGE)

        # Result examples
        results_example1 = Frame(results_container, bg="#2a3439")
        results_example1.place(relx=0.5, rely=0.02, anchor="n")
        results_example1.config(height=50, width=900)
        results_example1_label = Label(results_example1, text='Software 1', font=14, bg="#2a3439", fg="#5B676D")
        results_example1_label.place(relx=0.01, rely=0.5, anchor="w")

        results_example2 = Frame(results_container, bg="#2a3439")
        results_example2.place(relx=0.5, rely=0.02, anchor="n")
        results_example2.config(height=50, width=900)
        results_example2_label = Label(results_example2, text='Software 2', font=14, bg="#2a3439", fg="#5B676D")
        results_example2_label.place(relx=0.01, rely=0.5, anchor="w")

        results_example3 = Frame(results_container, bg="#2a3439")
        results_example3.place(relx=0.5, rely=0.02, anchor="n")
        results_example3.config(height=50, width=900)
        results_example3_label = Label(results_example3, text='Software 3', font=14, bg="#2a3439", fg="#5B676D")
        results_example3_label.place(relx=0.01, rely=0.5, anchor="w")

        results_example4 = Frame(results_container, bg="#2a3439")
        results_example4.place(relx=0.5, rely=0.02, anchor="n")
        results_example4.config(height=50, width=900)
        results_example4_label = Label(results_example4, text='Software 4', font=14, bg="#2a3439", fg="#5B676D")
        results_example4_label.place(relx=0.01, rely=0.5, anchor="w")

        results_example5 = Frame(results_container, bg="#2a3439")
        results_example5.place(relx=0.5, rely=0.02, anchor="n")
        results_example5.config(height=50, width=900)
        results_example5_label = Label(results_example5, text='Software 5', font=14, bg="#2a3439", fg="#5B676D")
        results_example5_label.place(relx=0.01, rely=0.5, anchor="w")

        results_example6 = Frame(results_container, bg="#2a3439")
        results_example6.place(relx=0.5, rely=0.02, anchor="n")
        results_example6.config(height=50, width=900)
        results_example6_label = Label(results_example6, text='Software 6', font=14, bg="#2a3439", fg="#5B676D")
        results_example6_label.place(relx=0.01, rely=0.5, anchor="w")

        # Align results in a grid
        results_example1.grid(row=0, column=0, padx=10, pady=5)
        results_example2.grid(row=1, column=0, padx=10, pady=5)
        results_example3.grid(row=2, column=0, padx=10, pady=5)
        results_example4.grid(row=3, column=0, padx=10, pady=5)
        results_example5.grid(row=4, column=0, padx=10, pady=5)
        results_example6.grid(row=5, column=0, padx=10, pady=5)
        # </editor-fold>

        # <editor-fold desc="Results Buttons">
        update_all_button = TkinterCustomButton(master=results_frame,
                                                fg_color="#848689",
                                                hover_color="#1F262A",
                                                text_font="Bold, 14",
                                                text="Update All",
                                                text_color="white",
                                                corner_radius=10,
                                                width=200,
                                                height=75,
                                                hover=True,
                                                command=lambda: None)
        update_all_button.place(relx=0.25, rely=0.8, anchor="center")

        update_selected_button = TkinterCustomButton(master=results_frame,
                                                     fg_color="#8797AF",
                                                     hover_color="#1F262A",
                                                     text_font="Bold, 14",
                                                     text="Update Selected",
                                                     text_color="white",
                                                     corner_radius=10,
                                                     width=200,
                                                     height=75,
                                                     hover=True,
                                                     command=lambda: None)
        update_selected_button.place(relx=0.5, rely=0.8, anchor="center")

        cancel_button = TkinterCustomButton(master=results_frame,
                                            fg_color="#5F4866",
                                            hover_color="#1F262A",
                                            text_font="Bold, 14",
                                            text="Cancel",
                                            text_color="white",
                                            corner_radius=10,
                                            width=100,
                                            height=50,
                                            hover=True,
                                            command=lambda: None)
        cancel_button.place(relx=0.70, rely=0.8, anchor="center")
        # </editor-fold>


class HelpPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        # Everything Commented out is for adding a scroll bar

        root.configure(background="#2a3439")

        helper_frame = Frame(root, bg="#2a3439")
        helper_frame.pack(fill=BOTH, expand=1)

        helper_canvas = Canvas(helper_frame)
        helper_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        helper_scrollbar = ttk.Scrollbar(helper_frame, orient=VERTICAL, command=helper_canvas.yview)
        helper_scrollbar.pack(side=RIGHT, fill=Y)

        helper_canvas.configure(yscrollcommand=helper_scrollbar.set)
        helper_canvas.bind('<Configure>', lambda e: helper_canvas.configure(scrollregion=helper_canvas.bbox("all")))

        root.configure(background="#2a3439")

        # <editor-fold desc="Results GUI">
        # Frame for whole results page
        help_frame = Frame(helper_frame, bg="#2a3439")
        help_frame.place(relx=0.5, rely=0.1, anchor="n")
        help_frame.config(height=root.winfo_height(), width=root.winfo_width())

        helper_canvas.create_window((0, 0), window=help_frame)

        # Container for results
        help_container = Frame(help_frame, bg="#1F262A", borderwidth=2)
        help_container.place(relx=0.5, rely=0.1, anchor="n")
        help_container.config(relief=RIDGE)

        # Help tip examples
        help_example1 = Frame(help_container, bg="#2a3439")
        help_example1.place(relx=0.5, rely=0.02, anchor="n")
        help_example1.config(height=200, width=900)
        help_example1_header_label = Label(help_example1, text='How to use the program:', font=24, bg="#2a3439",
                                           fg="#FFFFFF")
        help_example1_header_label.place(relx=0.01, rely=0.1, anchor="nw")

        text1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.""" \
            .replace('\n', ' ').replace('                ', ' ')
        help_example1_body_label = Label(help_example1, text=text1, font=20, bg="#2a3439", fg="#FFFFFF",
                                         wraplength=880, justify="left")
        help_example1_body_label.place(relx=0.01, rely=0.25, anchor="nw")

        help_example2 = Frame(help_container, bg="#2a3439")
        help_example2.place(relx=0.5, rely=0.02, anchor="n")
        help_example2.config(height=200, width=900)
        help_example2_header_label = Label(help_example2, text='How the Vulnerabilities are scored:', font=24,
                                           bg="#2a3439", fg="#FFFFFF")
        help_example2_header_label.place(relx=0.01, rely=0.1, anchor="nw")

        text2 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.""" \
            .replace('\n', ' ').replace('                ', ' ')
        help_example2_body_label = Label(help_example2, text=text2, font=20, bg="#2a3439", fg="#FFFFFF",
                                         wraplength=880, justify="left")
        help_example2_body_label.place(relx=0.01, rely=0.25, anchor="nw")

        help_example3 = Frame(help_container, bg="#2a3439")
        help_example3.place(relx=0.5, rely=0.02, anchor="n")
        help_example3.config(height=200, width=900)
        help_example3_header_label = Label(help_example3, text="What databases we're checking against:", font=24,
                                           bg="#2a3439", fg="#FFFFFF")
        help_example3_header_label.place(relx=0.01, rely=0.1, anchor="nw")

        text3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque semper, neque vitae 
                placerat interdum, orci nisl hendrerit erat, vel iaculis tellus lacus a nibh. Mauris
                consequat nunc non est sollicitudin efficitur. Fusce vestibulum eget est id euismod. Duis
                egestas tellus ac lorem egestas, at elementum libero viverra. In volutpat rhoncus
                dapibus. Morbi eu cursus felis. Mauris vel enim neque. Duis posuere rutrum varius.
                Curabitur id vestibulum est, in scelerisque orci. Morbi vitae condimentum ante.""" \
            .replace('\n', ' ').replace('                ', ' ')
        help_example3_body_label = Label(help_example3, text=text3, font=20, bg="#2a3439", fg="#FFFFFF",
                                         wraplength=880, justify="left")
        help_example3_body_label.place(relx=0.01, rely=0.25, anchor="nw")
        # Align tips in a grid
        help_example1.grid(row=0, column=0, padx=10, pady=5)
        help_example2.grid(row=1, column=0, padx=10, pady=5)
        help_example3.grid(row=2, column=0, padx=10, pady=5)
        # </editor-fold>


class SettingsPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        settings_frame = tk.Frame(root)
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

        text_size_label = ttk.Label(set_options_frame, text='Text size')
        text_size_label.grid(row=0, column=0, padx=50, pady=30)
        decrease_txt_size_button = ttk.Button(set_options_frame, text='-')
        decrease_txt_size_button.grid(row=0, column=1)
        txt_size_entry = ttk.Entry(set_options_frame, width=5)
        txt_size_entry.grid(row=0, column=2)
        txt_size_entry.insert(0, '12')
        increase_txt_size_button = ttk.Button(set_options_frame, text='+')
        increase_txt_size_button.grid(row=0, column=3)

        ignore_directories_label = ttk.Label(set_options_frame, text='Choose directories to ignore:')
        ignore_directories_label.grid(row=1, column=0, padx=50, pady=30)
        browse_button = ttk.Button(set_options_frame, text='Browse...')
        browse_button.grid(row=1, column=2)

        set_3_label = ttk.Label(set_options_frame, text='When scan finishes...')
        set_3_label.grid(row=2, column=0, padx=50)
        after_scan = StringVar()
        set_3_button_1 = ttk.Radiobutton(set_options_frame, text='Do Nothing', variable=after_scan, value='nothing')
        set_3_button_1.grid(row=2, column=2)
        set_3_button_2 = ttk.Radiobutton(set_options_frame, text='Close the program', variable=after_scan,
                                         value='close')
        set_3_button_2.grid(row=3, column=2)
        set_3_button_3 = ttk.Radiobutton(set_options_frame, text='Shut down computer', variable=after_scan,
                                         value='shut_down')
        set_3_button_3.grid(row=4, column=2)

        reset_settings_label = ttk.Label(set_options_frame, text='Reset Default Settings')
        reset_settings_label.grid(row=5, column=0, padx=50, pady=30)
        reset_button = ttk.Button(set_options_frame, text='Reset')
        reset_button.grid(row=5, column=2)

        apply_button = ttk.Button(settings_frame, text='Apply')
        apply_button.place(relx=0.5, rely=0.95, anchor='center')


class LoginPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        # Login page outer frame
        login_outer_frame = Frame(root, bg='#1F262A')
        login_outer_frame.place(relx=0.5, rely=0.5, anchor='center')
        login_outer_frame.config(height=450, width=650)
        login_outer_frame.config(relief=RAISED)

        # Login page inner frame
        login_inner_frame = Frame(login_outer_frame, background="#2a3439")
        login_inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        login_inner_frame.config(height=300, width=500)

        # Login Page title
        login_page_label = Label(login_inner_frame, text='Login Page', font="Bold, 20", bg='#2a3439', fg="white")
        login_page_label.place(relx=0.5, rely=0.15, anchor='center')

        # Login username and RSA token labels and entries
        username_label = Label(login_inner_frame, text='Username', font=15, background="#2a3439", foreground="white")
        username_label.place(relx=0.5, rely=0.3, anchor="center")
        username_entry = Entry(login_inner_frame, background="#1F262A", foreground="white", font=15)
        username_entry.place(relx=0.5, rely=0.4, anchor='center')
        token_label = Label(login_inner_frame, text='RSA Token', font=15, background="#2a3439", foreground="white")
        token_label.place(relx=0.5, rely=0.53, anchor='center')
        token_entry = Entry(login_inner_frame, background="#1F262A", foreground="white", font=15)
        token_entry.place(relx=0.5, rely=0.63, anchor='center')

        # Login Button (sends you to home page)
        login_button = TkinterCustomButton(master=login_inner_frame,
                                           bg_color="#2a3439",
                                           fg_color="#56667A",
                                           hover_color="#AAA9AD",
                                           text_font="Bold, 12",
                                           text="Login",
                                           text_color="white",
                                           corner_radius=10,
                                           width=80,
                                           height=40,
                                           hover=True,
                                           command=lambda: None)
        login_button.place(relx=0.4, rely=0.85, anchor='center')

        # Registration Button (Sends you to register page)
        register_button = TkinterCustomButton(master=login_inner_frame,
                                              bg_color="#2a3439",
                                              fg_color="#56667A",
                                              hover_color="#AAA9AD",
                                              text_font="Bold, 12",
                                              text="Register",
                                              text_color="white",
                                              corner_radius=10,
                                              width=80,
                                              height=40,
                                              hover=True,
                                              command=lambda: RegisterPage())
        register_button.place(relx=0.6, rely=0.85, anchor='center')


class RegisterPage:

    def __init__(self):
        global root

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        root.configure(background="#2a3439")

        # Register page frame
        register_frame = Frame(root, bg='#1F262A')
        register_frame.place(relx=0.5, rely=0.5, anchor='center')
        register_frame.config(height=350, width=500)
        register_frame.config(relief=RAISED)

        # Register page entries and labels
        register_title = Label(register_frame, text="Register", background="#1F262A", foreground="white",
                               font="Bold, 25")
        register_title.place(relx=0.5, rely=.1, anchor='center')
        first_name = Label(register_frame, text="First Name", background="#1F262A", foreground="white", font=20)
        first_name.place(relx=.17, rely=.3)
        first_name_entry = Entry(register_frame, background="#2a3439", foreground="white", width=25, font=20)
        first_name_entry.place(relx=.4, rely=.3)
        last_name = Label(register_frame, text="Last Name", background="#1F262A", foreground="white", font=20)
        last_name.place(relx=.17, rely=.42)
        last_name_entry = Entry(register_frame, background="#2a3439", foreground="white", width=25, font=20)
        last_name_entry.place(relx=.4, rely=.42)
        username = Label(register_frame, text="Username", background="#1F262A", foreground="white", font=20)
        username.place(relx=.17, rely=.54)
        username_entry = Entry(register_frame, background="#2a3439", foreground="white", width=25, font=20)
        username_entry.place(relx=.4, rely=.54)
        phone = Label(register_frame, text="Phone Number", background="#1F262A", foreground="white", font=20)
        phone.place(relx=.17, rely=.66)
        phone_entry = Entry(register_frame, background="#2a3439", foreground="white", width=25, font=20)
        phone_entry.place(relx=.4, rely=.66)

        # Create Account Button (sends you to login page)
        create_button = TkinterCustomButton(master=register_frame,
                                            bg_color="#1F262A",
                                            fg_color="#56667A",
                                            hover_color="#AAA9AD",
                                            text_font=20,
                                            text="Create",
                                            text_color="white",
                                            corner_radius=10,
                                            width=100,
                                            height=30,
                                            hover=True,
                                            command=lambda: LoginPage())
        create_button.place(relx=0.5, rely=0.85, anchor='center')