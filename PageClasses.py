"""
    This is the PageClasses.py class for the Software Inventory Tool Project
    This is the file that contains all the different functions to create/destroy the different
    windows that generate from clicking buttons on the GUI
    This file was entirely made by the Puffins Team
    Version:11.5.2021
"""

from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton
from Database import *
from tkinter import filedialog
import tkinter as tk
import os
import datetime
from plyer import notification

root = Tk()
global files_list
now = "Last Scanned: ----"
global last_page
last_page = ""
user_list = []

global logged_in
logged_in = False

title_bar = Frame(root, bg="#1F262A", relief="raised", bd=1)
title_bar.pack(fill=X)


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


def last_time_clicked():
    global now
    now = datetime.datetime.now().strftime("Last Scan: %b %d %Y, %I:%M:%S %p")


def frame_mapped(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')


# ToolTip class for making tips that appear after hovering mouse over button for 0.5 seconds
class ToolTip(object):

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    # Creates tip after 0.5 seconds
    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Makes frame for tip
        self.tw = Toplevel(self.widget)
        # Gets rid of the window for the frame for tip
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        # Tip customization
        label = ttk.Label(self.tw, text=self.text, justify='left',
                          background="#ffffff", relief='solid', borderwidth=1,
                          wraplength=self.wraplength)
        label.pack(ipadx=1)

    # Hides tip after taking mouse off the button
    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class MakeWindow:
    def nav_buttons(self):
        # Navigation Buttons
        home_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 12",
                                          text="Home",
                                          text_color="white",
                                          corner_radius=0,
                                          width=50,
                                          height=40,
                                          hover=True,
                                          command=lambda: MainWindow())
        home_button.pack(side=LEFT, padx=5)

        # Results Button here
        results_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                             fg_color="#1F262A",
                                             hover_color="#2a3439",
                                             text_font="Bold, 12",
                                             text="Results",
                                             text_color="white",
                                             corner_radius=0,
                                             width=65,
                                             height=40,
                                             hover=True,
                                             command=lambda: ResultsPage())
        results_button.pack(side=LEFT, padx=5)

        # Create Settings Button
        settings_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                              fg_color="#1F262A",
                                              hover_color="#2a3439",
                                              text_font="Bold, 12",
                                              text="Settings",
                                              text_color="white",
                                              corner_radius=0,
                                              width=70,
                                              height=40,
                                              hover=True,
                                              command=lambda: SettingsPage())
        settings_button.pack(side=LEFT, padx=5)

        # Create Help Button
        help_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 12",
                                          text="Help",
                                          text_color="white",
                                          corner_radius=0,
                                          width=40,
                                          height=40,
                                          hover=True,
                                          command=lambda: HelpPage())
        help_button.pack(side=LEFT, padx=5)


class MainWindow:

    def __init__(self):
        global root
        global now
        global last_page
        global title_bar

        if last_page != "HomePage":
            last_page = "HomePage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            root.configure(background="#2a3439")

            main_frame = Frame(root, bg="#2a3439")
            main_frame.place(relx=0.5, rely=0.1, anchor="n")
            main_frame.config(height=root.winfo_height(), width=root.winfo_width())

            style = ttk.Style(root)
            style.theme_use('classic')
            style.configure('Test.TSizegrip', background="#1F262A")
            root_size_grip = ttk.Sizegrip(root)

            root_size_grip.configure(style="Test.TSizegrip")
            root_size_grip.pack(side="right", anchor=SE)

            # LabelFrame that shows thew Last time some thing was scanned. Initialized as "Last Scanned: ----"
            scan_time_frame = LabelFrame(main_frame, bg="#2a3439", fg="white", font=10, text=now, relief=FLAT)
            scan_time_frame.place(relx=0.18, rely=0.1, anchor="n")
            scan_time_frame.config(height=40, width=350)

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
                                              command=lambda: ScanConfirmPage.make_full_scan_config(self))
            scan_button.place(relx=.01)
            ToolTip(scan_button, "Scans all the software files from list.")

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
                                                      command=lambda: ScanConfirmPage.make_express_config(self))
            express_scan_button.place(relx=.12)
            ToolTip(express_scan_button, "Scans the most important software files.")

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


# This class will create the scan page
# This will be different whether the full scan or express scan options were selected
# Picking one of the options will load up the proper buttons for that configuration
class ScanConfirmPage:
    global files_list
    files_list = []

    def __init__(self):
        global root
        global last_page

    # This will setup the button for the Full Scan configuration
    def make_full_scan_config(self):
        for widget in root.winfo_children()[1:]:
            widget.destroy()

            root.configure(background="#2a3439")

            # This lets scan() know whether to scan all program files or just selected files
            global scan_type
            scan_type = "Full Scan"

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
                                                  command=lambda: [last_time_clicked(), ScanConfirmPage.scan(self)])
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

    # This will setup the buttons for the Express Scan Function
    def make_express_config(self):
        global scan_type
        # This lets scan() know whether to scan all program files or just selected files
        scan_type = "Express Scan"

        def browse_files():
            global files_list
            filenames = filedialog.askopenfilenames(initialdir="C:\Program Files",
                                                    title="Select Files",
                                                    filetypes=(("all files",
                                                                "*.*"),
                                                               ("Executable files",
                                                                "*.exe*")))
            # Additional files selected after first selection will be appended to list
            files_list = files_list + list(filenames)
            ctr = 0

            # Display selected files on confirm page
            for file in files_list:
                file_block = tk.Frame(scan_confirm_container, bg="#2a3439")
                file_block.config(height=50, width=860)
                file_label = tk.Label(file_block, text=files_list[ctr], font=14, bg="#2a3439", fg="white",
                                      wraplength=845, justify='left')
                file_label.place(relx=0.01, rely=0.5, anchor="w")
                file_block.grid(row=ctr, column=0, padx=10, pady=5)

                ctr = ctr + 1

            # Scrollbar if more than 5 files are selected
            if ctr > 5:
                scan_confirm_sb = ttk.Scrollbar(scan_confirm_canvas, orient="vertical",
                                                command=scan_confirm_canvas.yview)
                scan_confirm_sb.place(relx=0.98, height=scan_confirm_canvas.winfo_height())
                scan_confirm_canvas.configure(yscrollcommand=scan_confirm_sb.set)

        root.configure(background="#2a3439")

        # Frame for scan confirmation dialog box
        scan_confirm_frame = Frame(root, bg="#2a3439")
        scan_confirm_frame.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_frame.config(height=root.winfo_height(), width=root.winfo_width())

        scan_confirm_label = Label(scan_confirm_frame, text='What will be scanned:', font=14, bg="#2a3439",
                                   fg="white")
        scan_confirm_label.place(relx=0.05, rely=0.05, anchor="w")

        scan_confirm_canvas = Canvas(scan_confirm_frame, height=300, width=900, bg="#2a3439")
        scan_confirm_canvas.place(relx=0.5, rely=0.1, anchor="n")

        # Container for files to be scanned
        scan_confirm_container = Frame(scan_confirm_canvas, bg="#1F262A", borderwidth=2)
        scan_confirm_container.place(relx=0.5, rely=0.1, anchor="n")
        scan_confirm_container.config(relief=RIDGE, height=350, width=900)
        # Bind scrollbar to container
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
                                              command=lambda: [last_time_clicked(), ScanConfirmPage.scan(self)])
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
                                               command=lambda: browse_files())
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

    # This will scan the Database
    # This function will be called no matter which config is decided on
    def scan(self):
        global files_list
        list_results = []
        cve = CVEDataFrame()
        # Makes a progress bar
        progressbar_style_element = ttk.Style()
        progressbar_style_element.theme_use('alt')
        progressbar_style_element.configure("red.Horizontal.TProgressbar", foreground='red', bg='red')
        results_progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate',
                                              style="red.Horizontal.TProgressbar")
        results_progressbar.place(relx=0.5, rely=0.8, anchor="center")

        if scan_type == "Full Scan":
            # Get all files from Start Menu folder
            for dirpath, dirnames, files in os.walk("C:\ProgramData\Microsoft\Windows\Start Menu"):
                for file in files:
                    files_list.append(os.path.join(dirpath, file))

        # This will remove the path extension for all of the selected applications
        # This will loop through all the Files, selected from the sub menu in Express Scan
        for record in files_list:
            # This will reduce the name to a Application.exe
            base = os.path.basename(record)
            # This will separate the Application.exe to a list of [Application, .exe]
            os.path.splitext(base)
            base = base[:-4]
            # This will actively update the progress bar an appropriate amount of times
            results_progressbar['value'] += (100 / len(files_list))
            root.update_idletasks()

            # This will not add an entry to the results list if nothing is found in the CVE Database
            if not cve.select_record_by_name(base):
                pass
            # This will add an entry to the results list with vulnerability from the CVE Database
            else:
                list_results.append(cve.select_record_by_name(base))

        results_progressbar.destroy()

        ResultsPage.print_results(self, list_results)
        title = 'A scan has been completed!'
        message = 'Please return to the Software Inventory Tool to view results.'
        notification.notify(title=title,
                            message=message,
                            app_icon='logo.ico',
                            timeout=10,
                            toast=False)


# This will create the results page
class ResultsPage:

    def __init__(self):
        global root
        global last_page

        # Does a check to see if the page we are currently on to not reload page
        if last_page != "ResultsPage":
            last_page = "ResultsPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            root.configure(background="#2a3439")

            results_frame = Frame(root, bg="#2a3439")
            results_frame.place(relx=0.5, rely=0.1, anchor="n")
            results_frame.config(height=root.winfo_height(), width=root.winfo_width())

            ResultsPage.create_update_buttons(results_frame)

            # Container for filter settings
            filter_settings_container = tk.Frame(results_frame, bg="#1F262A", borderwidth=2)
            filter_settings_container.place(relx=0.04, rely=0.0, anchor="nw")
            filter_settings_container.config(relief=RIDGE)

            # Container for results
            results_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
            results_container.place(relx=0.5, rely=0.1, anchor="n")
            results_container.config(relief=RIDGE)

            # Creating Filler Results
            # These will disappear once a scan happen
            # These will reappear if clicking off the  Results page and coming back
            results_files_frame = Frame(results_container, bg="#2a3439")
            results_files_frame.place(relx=0.5, rely=0.02, anchor="n")
            results_files_frame.config(height=50, width=900)

            for i in range(6):
                results_example = Frame(results_container, bg="#2a3439")
                results_example.config(height=50, width=900)
                results_example1_label = Label(results_example, text=f'Software {i}', font=14, bg="#2a3439",
                                               fg="#5B676D")
                results_example1_label.place(relx=0.01, rely=0.5, anchor="w")
                results_example.grid(row=i, column=0, padx=10, pady=5)
            # </editor-fold>

    # Function to create the update buttons before and after have results
    @staticmethod
    def create_update_buttons(results_frame):
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

        filter_settings_container = tk.Frame(results_frame, bg="#1F262A", borderwidth=2)
        filter_settings_container.place(relx=0.04, rely=0.0, anchor="nw")
        filter_settings_container.config(relief=RIDGE)

        sort_scan_label = tk.Label(filter_settings_container, text='Sort scan results...', font='2', bg='#2a3439',
                                   fg="white")

        style_element = ttk.Style()  # Creating style element
        style_element.configure('Sort.TRadiobutton',
                                # First argument is the name of style. Needs to end with: .TRadiobutton
                                background='#2a3439',  # Setting background to our specified color above
                                foreground='white')

        sort_scan_label.grid(row=1, column=0, padx=50)

        # Settings dropdown window
        option_list = [
            "By Severity",
            "By Time",
            "Alphabetically"
        ]
        global sort_variable
        sort_variable = tk.StringVar(filter_settings_container)
        # Default sorting is by severity
        sort_variable.set("By Severity")

        opt = tk.OptionMenu(filter_settings_container, sort_variable, *option_list)
        opt.config(background="#1F262A", foreground="white", width=15, font=('Bold', 12))
        opt.grid()

        style = ttk.Style(root)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(root)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)
        # </editor-fold>

    # This will take the software found from a scan
    # And print them to the results page
    def print_results(self, list_results):

        results_frame = Frame(root, bg="#2a3439")
        results_frame.place(relx=0.5, rely=0.1, anchor="n")
        results_frame.config(height=root.winfo_height(), width=root.winfo_width())
        # Calls function to put the update buttons back on the screen with the results
        ResultsPage.create_update_buttons(results_frame)

        results_canvas = Canvas(results_frame, height=300, width=900, bg="#2a3439")
        results_canvas.place(relx=0.5, rely=0.15, anchor="n")

        # Container for results
        results_container = Frame(results_canvas, bg="#1F262A", borderwidth=2)
        results_container.place(relx=0.5, rely=0.1, anchor="n")
        results_container.config(relief=RIDGE, height=350, width=900)

        # Bind scrollbar to container
        results_container.bind(
            "<Configure>",
            lambda e: results_canvas.configure(
                scrollregion=results_canvas.bbox("all")
            )
        )
        results_canvas.create_window((0, 0), window=results_container, anchor="nw")


        # This loop will run for the amount of items that are found to have vulnerabilities in the Database
        # It will send a Sting to the results page with the information
        # It will only run as many times as vulnerabilities found
        for i in range(len(list_results)):
            results_example = Frame(results_container, bg="#2a3439")
            results_example.config(height=50, width=860)
            results_example1_label = Label(results_example, text=str(list_results[i]), font=14, bg="#2a3439",
                                           fg="#5B676D")
            results_example1_label.place(relx=0.01, rely=0.5, anchor="w")
            results_example.grid(row=i, column=0, padx=10, pady=5)

        # Scrollbar if more than 5 results are displayed
            if len(list_results) > 5:
                results_sb = ttk.Scrollbar(results_canvas, orient="vertical", command=results_canvas.yview)
                results_sb.place(relx=0.98, height=results_canvas.winfo_height())
                results_canvas.configure(yscrollcommand=results_sb.set)


class HelpPage:

    def __init__(self):
        global root
        global last_page

        if last_page != "HelpPage":
            last_page = "HelpPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            style = ttk.Style(root)
            style.theme_use('classic')
            style.configure('Test.TSizegrip', background="#1F262A")
            root_size_grip = ttk.Sizegrip(root)

            root_size_grip.configure(style="Test.TSizegrip")
            root_size_grip.pack(side="right", anchor=SE)

            helper_frame = Frame(root, bg="#2a3439")
            helper_frame.pack(fill=BOTH, expand=1)

            help_canvas = Canvas(helper_frame, bg="#2a3439", highlightthickness=0)
            help_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            help_sb = ttk.Scrollbar(helper_frame, orient=VERTICAL, command=help_canvas.yview)
            help_sb.pack(side=RIGHT, fill=Y)

            help_canvas.configure(yscrollcommand=help_sb.set)
            help_canvas.bind('<Configure>',
                             lambda e: help_canvas.configure(scrollregion=help_canvas.bbox("all")))

            # <editor-fold desc="Results GUI">
            # Frame for whole results page
            help_frame = Frame(help_canvas)
            help_frame.configure(bg="#1F262A")
            help_canvas.create_window((0, 0), window=help_frame, anchor="nw")

            # Container for results
            help_container = Frame(help_frame, bg="#1F262A", borderwidth=2)
            help_container.place(relx=0.5, rely=0.1, anchor="n")
            help_container.config(relief=RIDGE)

            # Help tip examples
            help_example1 = Frame(help_frame, bg="#2a3439")
            help_example1.place(relx=0.5, rely=0.02, anchor="n")
            help_example1.config(height=285, width=900)
            help_example1_header_label = Label(help_example1, text='How to use the program:', font=24, bg="#2a3439",
                                               fg="#FFFFFF")
            help_example1_header_label.place(relx=0.01, rely=0.1, anchor="nw")

            text1 = """First after logging in, you have a choice of what to do. If choose to run a scan
                    this can be done clicking onto the home page. From here you have the choice of what kind
                    of scan you would like to run. Mousing over the options will give a brief description of 
                    the differences between them. From there you will be directed to the Results Page. Here
                    the applications that have vulnerabilities will be listed. If the user that is logged in
                    has the permissions, they will be able to update the application from here. Otherwise they 
                    will just be able to see the vulnerabilities. If instead the Results page is clicked, this will
                    display the results from the scan that was last run. And lastly if the Settings Page is selected, 
                    this will bring you to a page where you can change options such as font size and the way items are 
                    sorted to make the tool as easy to use as possible.""" \
                .replace('\n', ' ').replace('                    ', '')
            help_example1_body_label = Label(help_example1, text=text1, font=20, bg="#2a3439", fg="#FFFFFF",
                                             wraplength=880, justify="left")
            help_example1_body_label.place(relx=0.01, rely=0.25, anchor="nw")

            help_example2 = Frame(help_frame, bg="#2a3439")
            help_example2.place(relx=0.5, rely=0.02, anchor="n")
            help_example2.config(height=200, width=900)
            help_example2_header_label = Label(help_example2, text='How the Vulnerabilities are scored:', font=24,
                                               bg="#2a3439", fg="#FFFFFF")
            help_example2_header_label.place(relx=0.01, rely=0.1, anchor="nw")

            text2 = """ To score the vulnerabilities we will be interfacing with the a CVSS 2.0 scorer.
                    CVSS or better known as the Common Vulnerability Scoring System will take in a number of parameters
                    in order to delivery an accurate threat score. Some of the items taken into account when calculating
                    a score are the Access Vector, Access Complexity, Authentication, Confidentiality Impact, Integrity Impact, 
                    and lastly the Availability Impact.
            """ \
                .replace('\n', ' ').replace('                    ', '')
            help_example2_body_label = Label(help_example2, text=text2, font=20, bg="#2a3439", fg="#FFFFFF",
                                             wraplength=880, justify="left")
            help_example2_body_label.place(relx=0.01, rely=0.25, anchor="nw")

            help_example3 = Frame(help_frame, bg="#2a3439")
            help_example3.place(relx=0.5, rely=0.02, anchor="n")
            help_example3.config(height=200, width=900)
            help_example3_header_label = Label(help_example3, text="What databases we're checking against:", font=24,
                                               bg="#2a3439", fg="#FFFFFF")
            help_example3_header_label.place(relx=0.01, rely=0.1, anchor="nw")

            text3 = """In its current state, the Software Inventory Tool uses the CVE (Common
                    Vulnerabilities and Exposures) Database to detect vulnerabilities in software.
                    Further versions of the Software Inventory Tool may implement more than one
                    database depending on performance using the CVE database and based on the
                    availability of accessing other databases that may or may not exist or
                    be available for public access.""" \
                .replace('\n', ' ').replace('                    ', '')
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
        global last_page

        if last_page != "SettingsPage":
            last_page = "SettingsPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            style = ttk.Style(root)
            style.theme_use('classic')
            style.configure('Test.TSizegrip', background="#1F262A")
            root_size_grip = ttk.Sizegrip(root)

            root_size_grip.configure(style="Test.TSizegrip")
            root_size_grip.pack(side="right", anchor=SE)

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
        global last_page
        global logged_in
        username_var = tk.StringVar(value="")
        token_var = tk.StringVar(value="")

        if last_page != "LoginPage":
            last_page = "LoginPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            style = ttk.Style(root)
            style.theme_use('classic')
            style.configure('Test.TSizegrip', background="#1F262A")
            root_size_grip = ttk.Sizegrip(root)

            root_size_grip.configure(style="Test.TSizegrip")
            root_size_grip.pack(side="right", anchor=SE)
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
            username_label = Label(login_inner_frame, text='Username', font=15, background="#2a3439",
                                   foreground="white")
            username_label.place(relx=0.5, rely=0.3, anchor="center")
            username_entry = Entry(login_inner_frame, textvariable=username_var, background="#1F262A",
                                   foreground="white", font=15)
            username_entry.place(relx=0.5, rely=0.4, anchor='center')
            token_label = Label(login_inner_frame, text='RSA Token', font=15, background="#2a3439", foreground="white")
            token_label.place(relx=0.5, rely=0.53, anchor='center')
            token_entry = Entry(login_inner_frame, textvariable=token_var, background="#1F262A", foreground="white",
                                font=15)
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
                                               command=lambda: [MainWindow() if check_login() else login_error()])
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

        # Search through user list. Return True if user and token are correct.
        def check_login():
            global user_list
            username = username_entry.get()
            token = token_entry.get()
            exists = False
            for i in range(len(user_list)):
                if user_list[i][2] == username and user_list[i][4] == token:
                    exists = True
                    logged_in = True
                    MakeWindow.nav_buttons(self)

            return exists

        # Make error message for login
        def login_error():
            error_message = LabelFrame(login_inner_frame, bg="#2a3439", fg="red", font=10,
                                       text="Wrong Username or RSA Token.", relief=FLAT)
            error_message.place(relx=0.5, rely=0.68, anchor="n")
            error_message.config(height=19, width=240)

        def enter_login(e):
            if check_login():
                MainWindow()
                root.unbind('<Return>', None)
            else:
                login_error()

        root.bind('<Return>', enter_login)


class RegisterPage:

    def __init__(self):
        global root
        global last_page

        # Initialize input variables
        first_name_var = tk.StringVar(value="")
        last_name_var = tk.StringVar(value="")
        username_var = tk.StringVar(value="")
        role_var = tk.StringVar(value="")

        if last_page != "ResultsPage":
            last_page = "ResultsPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()

            root.configure(background="#2a3439")
            style = ttk.Style(root)
            style.theme_use('classic')
            style.configure('Test.TSizegrip', background="#1F262A")
            root_size_grip = ttk.Sizegrip(root)

            root_size_grip.configure(style="Test.TSizegrip")
            root_size_grip.pack(side="right", anchor=SE)

            # Register page frame
            register_frame = Frame(root, bg='#1F262A')
            register_frame.place(relx=0.5, rely=0.5, anchor='center')
            register_frame.config(height=350, width=500)
            register_frame.config(relief=RAISED)

            # Register page entries and labels
            register_title = Label(register_frame, text="Register", background="#1F262A", foreground="white",
                                   font="Bold, 25")
            register_title.place(relx=0.5, rely=.1, anchor='center')

            first_name_frame = Label(register_frame, text="First Name", background="#1F262A", foreground="white",
                                     font=20)
            first_name_frame.place(relx=.16003, rely=.3)
            first_name_entry = Entry(register_frame, textvariable=first_name_var, background="#2a3439",
                                     foreground="white", width=25, font=20)
            first_name_entry.place(relx=.4, rely=.3)

            last_name_frame = Label(register_frame, text="Last Name", background="#1F262A", foreground="white", font=20)
            last_name_frame.place(relx=.16001, rely=.42)
            last_name_entry = Entry(register_frame, textvariable=last_name_var, background="#2a3439",
                                    foreground="white", width=25, font=20)
            last_name_entry.place(relx=.4, rely=.42)

            username_frame = Label(register_frame, text="Username", background="#1F262A", foreground="white", font=20)
            username_frame.place(relx=.1703, rely=.54)
            username_entry = Entry(register_frame, textvariable=username_var, background="#2a3439", foreground="white",
                                   width=25, font=20)
            username_entry.place(relx=.4, rely=.54)

            role_frame = Label(register_frame, text="Role", background="#1F262A", foreground="white", font=20)
            role_frame.place(relx=.25, rely=.66)
            role_entry = Entry(register_frame, textvariable=role_var, background="#2a3439", foreground="white",
                                width=25, font=20)
            role_entry.place(relx=.4, rely=.66)

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
                                                command=lambda: [new_register(), LoginPage()])
            create_button.place(relx=0.5, rely=0.85, anchor='center')

        # Register new user
        def new_register():
            global user_list

            # Get new users info
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            username = username_entry.get()
            role = role_entry.get()

            # Add new user to user list
            new_account = [first_name, last_name, username, role, "123456"]
            user_list.append(new_account)

        def enter_register(e):
            new_register()
            LoginPage()

        root.bind('<Return>', enter_register)