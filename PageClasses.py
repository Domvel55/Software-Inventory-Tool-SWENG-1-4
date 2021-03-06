"""
    This is the PageClasses.py class for the Software Inventory Tool Project
    This is the file that contains all the different functions to create/destroy the different
    windows that generate from clicking buttons on the GUI
    This file was entirely made by the Puffins Team
    Version:11.5.2021
"""
from time import sleep
from tkinter import *
from tkinter import ttk, filedialog
from tkinter_custom_button import TkinterCustomButton
from Database import *
import os
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from plyer import notification
from ctypes import windll
import threading


global stopped
stopped = False

now = "Last Scanned: ----"
sort_variable = None
history_counter = 0
files_list, user_list, history_list, list_results, filter_settings, sched_list, check_buttons = [], [], [], [], [], [], []
history_comments = {}
name, role, last_page = "", "", ""
results_progressbar = None

root = Tk()
title_bar = Frame(root, bg="#1F262A", relief="raised", bd=1)
title_bar.pack(fill=X)

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

boolTest = FALSE


def read_config():
    global now, user_list
    with open('configuration.ini', encoding='UTF-8') as f:
        file = list(f)
        now = file[0]
        for user in file[2:]:
            temp = user.split('~')
            user_list.append(
                [temp[0][5:].split()[0], temp[0][5:].split()[1], temp[1][5:].split()[0], temp[2][5:].split()[0],
                 temp[3][5:].split()[0], temp[4][5:].split()[0]])
    f.close()


def write_config():
    with open('configuration.ini', 'w', encoding='UTF-8') as f:
        f.write(f'{now}'
                f'Users:\n')
        for user in user_list:
            f.write(f'Name: {user[0]} {user[1]}~User: {user[2]}~Pass: {user[3]}~Role: {user[4]}~Stat: {user[5]}\n')
    f.close()


def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')


def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())


def quitter(e):
    root.quit()


def minimizer(e):
    global boolTest
    root.update_idletasks()
    root.overrideredirect(False)
    boolTest = TRUE
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


def new_page(e):
    ApplicationResultsPage(e.widget.grid_info()['row'])


def history_page(e):
    HistoryLogPage(e.widget.grid_info()['row'])


def new_user_page(e):
    ApplicationAdminPage(e.widget.grid_info()['row'])


def last_time_clicked():
    global now
    now = f'{datetime.datetime.now().strftime("Last Scan: %b %d %Y, %I:%M:%S %p")}\n'


def frame_mapped(e):
    global boolTest
    root.update_idletasks()
    if boolTest:
        root.after(10, lambda: set_appwindow(root))
        boolTest = FALSE
    root.overrideredirect(True)
    root.state('normal')


def update_history():
    global list_results, history_counter
    history_list.append([now, list_results])
    history_counter += 1


def unlock_account(user_num):
    user_list[user_num][5] = 0


def lock_account(user_num):
    user_list[user_num][5] = 5


def update_pb():
    global results_progressbar, root
    # This will actively update the progress bar an appropriate amount of times
    results_progressbar['value'] += (100 / len(files_list))
    root.update_idletasks()


def destroy_pb():
    global results_progressbar
    results_progressbar.destroy()


def stop():
    global stopped
    stopped = True
    destroy_pb()


def start():
    global stopped
    stopped = False
    files_list.clear()
    list_results.clear()


def update_comments(result_num, text):
    history_comments[history_counter] = {result_num: text}


def reset_results_list():
    global list_results
    list_results.clear()


def remove_selected():
    global list_results, check_buttons
    temp = []
    for i in range(len(list_results)):
        if check_buttons[i].get() == 0:
            temp.append(list_results[i])
    list_results = temp
    check_buttons.clear()


def update_selected():
    global list_results, check_buttons
    new_list = []
    popped_list = []
    for i in range(len(list_results)):
        if check_buttons[i].get() == 0:
            new_list.append(list_results[i])
        else:
            popped_list.append(list_results[i])
    list_results = new_list
    check_buttons.clear()
    return popped_list


def print_updates(list_to_print):
    temp = []
    for i in range(len(list_to_print)):
        temp.append(str(list_to_print[i][0][-1].split('/')[-1]))
    return temp


# This will scan the Database
# This function will be called no matter which config is decided on
def scan():
    global files_list, results_progressbar, list_results
    cve = CVEDataFrame()
    rate = CVSSScorer()

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

        update_pb()
        record_query = cve.select_record_by_name(base)
        temp_list = []
        # This will add an entry to the results list with vulnerability from the CVE Database
        if len(record_query) != 0:
            for i in record_query:
                nvd_query = rate.website_query(i[0])
                sleep(0.75)
                temp = i.copy()
                temp.append(nvd_query[1])
                temp.append(nvd_query[0])
                temp.append(record)
                temp_list.append(temp)
            list_results.append(temp_list)

    destroy_pb()
    update_history()
    ResultsPage()
    ResultsPage.print_results('By Severity', filter_settings)
    change_results_button()
    title = 'A scan has been completed!'
    message = 'Please return to the Software Inventory Tool to view results.'
    notification.notify(title=title,
                        message=message,
                        app_icon='logo.ico',
                        timeout=10,
                        toast=False)


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
        x += self.widget.winfo_rootx() + self.widget.winfo_width() / 10
        y += self.widget.winfo_rooty() + self.widget.winfo_height()
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

    def make_nav_buttons(self):
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
                                          command=lambda: [MainWindow(), change_home_button()])
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
                                             command=lambda: [ResultsPage(), change_results_button(),
                                                              ResultsPage.print_results(sort_variable.get(),
                                                                                        filter_settings)])
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
                                              command=lambda: [SettingsPage(), change_settings_button()])
        settings_button.pack(side=LEFT, padx=5)

        # Create Help Button
        help_button = TkinterCustomButton(master=title_bar, bg_color=None,
                                          fg_color="#1F262A",
                                          hover_color="#2a3439",
                                          text_font="Bold, 12",
                                          text="Help",
                                          text_color="white",
                                          corner_radius=0,
                                          width=45,
                                          height=40,
                                          hover=True,
                                          command=lambda: [HelpPage(), change_help_button()])
        help_button.pack(side=LEFT, padx=5)

        # This will change the color of the home button when clicked on
        # This will also change the color of all the other buttons back to default
        global change_home_button, change_results_button, change_settings_button, change_help_button

        def change_home_button():
            home_button.configure_color(fg_color="#5F4B66", text_color="white")
            results_button.configure_color(fg_color="#1F262A", text_color="white")
            settings_button.configure_color(fg_color="#1F262A", text_color="white")
            help_button.configure_color(fg_color="#1F262A", text_color="white")

        # This will change the color of the results button when clicked on
        # This will also change the color of all the other buttons back to default
        def change_results_button():
            home_button.configure_color(fg_color="#1F262A", text_color="white")
            results_button.configure_color(fg_color="#5F4B66", text_color="white")
            settings_button.configure_color(fg_color="#1F262A", text_color="white")
            help_button.configure_color(fg_color="#1F262A", text_color="white")

        # This will change the color of the settings button when clicked on
        # This will also change the color of all the other buttons back to default
        def change_settings_button():
            home_button.configure_color(fg_color="#1F262A", text_color="white")
            results_button.configure_color(fg_color="#1F262A", text_color="white")
            settings_button.configure_color(fg_color="#5F4B66", text_color="white")
            help_button.configure_color(fg_color="#1F262A", text_color="white")

        # This will change the color of the help button when clicked on
        # This will also change the color of all the other buttons back to default
        def change_help_button():
            home_button.configure_color(fg_color="#1F262A", text_color="white")
            results_button.configure_color(fg_color="#1F262A", text_color="white")
            settings_button.configure_color(fg_color="#1F262A", text_color="white")
            help_button.configure_color(fg_color="#5F4B66", text_color="white")


class MainWindow:

    def __init__(self):
        global root
        global now
        global last_page
        global title_bar

        if last_page != "HomePage":
            last_page = "HomePage"
            change_home_button()
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

            # LabelFrame that shows the Last time some thing was scanned. Initialized as "Last Scanned: ----"
            scan_time_frame = LabelFrame(main_frame, bg="#2a3439", fg="white", font=10, text=now, relief=FLAT)
            scan_time_frame.place(relx=0.18, rely=0.1, anchor="n")
            scan_time_frame.config(height=40, width=350)

            # LabelFrame that shows the current user's name. Initialized as "John Doe"
            current_name = LabelFrame(main_frame, bg="#2a3439", fg="white", font=10, text="NAME:    " + name,
                                      relief=FLAT)
            current_name.place(relx=0.18, rely=0.765, anchor="n")
            current_name.config(height=40, width=350)

            # LabelFrame that shows the current user's role. Initialized as "None"
            current_role = LabelFrame(main_frame, bg="#2a3439", fg="white", font=10, text="ROLE:    " + role,
                                      relief=FLAT)
            current_role.place(relx=0.18, rely=0.8, anchor="n")
            current_role.config(height=40, width=350)

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
            ToolTip(scan_button, "Scans all the software files from a directory.")

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
            ToolTip(express_scan_button, "Scans the selected software files for a quicker scan.")

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
                                                       command=lambda: ScheduleScanPage())
            schedule_scan_button.place(relx=.27)
            ToolTip(schedule_scan_button, "Schedule a full scan.")

            history_button = TkinterCustomButton(master=main_frame,
                                                 bg_color="#2a3439",
                                                 fg_color="#1F262A",
                                                 hover_color="#AAA9AD",
                                                 text_font="Bold, 14",
                                                 text="History",
                                                 text_color="white",
                                                 corner_radius=10,
                                                 width=130,
                                                 height=40,
                                                 hover=True,
                                                 command=lambda: HistoryPage())
            history_button.place(relx=0.6, rely=0.85, anchor='center')
            ToolTip(schedule_scan_button, "See run history")
            # </editor-fold>

            if role == "Admin":
                admin_button = TkinterCustomButton(master=main_frame,
                                                   bg_color="#2a3439",
                                                   fg_color="#1F262A",
                                                   hover_color="#AAA9AD",
                                                   text_font="Bold, 14",
                                                   text="Admin Page",
                                                   text_color="white",
                                                   corner_radius=10,
                                                   width=130,
                                                   height=40,
                                                   hover=True,
                                                   command=lambda: AdminPage())
                admin_button.place(relx=0.8, rely=0.85, anchor='center')
                ToolTip(schedule_scan_button, "See users")

            # Create Logout Button
            logout_button = TkinterCustomButton(master=main_frame, bg_color="#2a3439",
                                                fg_color="#1F262A",
                                                hover_color="#AAA9AD",
                                                text_font="Bold, 14",
                                                text="Logout",
                                                text_color="white",
                                                corner_radius=10,
                                                width=80,
                                                height=40,
                                                hover=True,
                                                command=lambda: [LoginPage()])
            logout_button.place(relx=0.05, rely=0.69, anchor="n")


# Contains the history of the program.
# Creates the page that contains the history.
class HistoryPage:

    def __init__(self):
        global root
        global last_page

        if last_page != "MainWindow":
            last_page = "MainWindow"

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
            history_frame = Frame(root, bg='#1F262A')
            history_frame.place(relx=0.5, rely=0.5, anchor='center')
            history_frame.config(height=400, width=800)
            history_frame.config(relief=RAISED)

            # Container for results
            history_container = Frame(history_frame, bg="#1F262A", borderwidth=2)
            history_container.place(relx=0.5, rely=0.1, anchor="n")
            history_container.config(relief=RIDGE)

            print(history_list)
        HistoryPage.print_history(self, history_list)

    def print_history(self, history_list):

        history_frame = Frame(root, bg="#2a3439")
        history_frame.place(relx=0.5, rely=0.1, anchor="n")
        history_frame.config(height=root.winfo_height(), width=root.winfo_width())

        history_canvas = Canvas(history_frame, height=300, width=900, bg="#2a3439")
        history_canvas.place(relx=0.5, rely=0.15, anchor="n")

        # Container for results
        history_container = Frame(history_canvas, bg="#1F262A", borderwidth=2)
        history_container.place(relx=0.5, rely=0.1, anchor="n")
        history_container.config(relief=RIDGE, height=350, width=900)

        # Bind scrollbar to container
        history_container.bind(
            "<Configure>",
            lambda e: history_canvas.configure(
                scrollregion=history_canvas.bbox("all")
            )
        )
        history_canvas.create_window((0, 0), window=history_container, anchor="nw")

        # This loop will run for the amount of items that are found to have vulnerabilities in the Database
        # It will send a String to the results page with the information
        # It will only run as many times as vulnerabilities found
        for i in range(len(history_list)):
            for a in range(len(history_list[i])):
                history_example = Frame(history_container, bg="#2a3439")
                history_example.config(height=50, width=860)
                history_example1_label = Label(history_example, text=str(history_list[i][0]), font=10,
                                               bg="#2a3439", fg="#FFFFFF")
                history_example1_label.place(relx=0.01, rely=0.5, anchor="w")
                history_example.bind("<Button-1>", history_page)
                history_example.grid(row=i, column=0, padx=10, pady=5)

            # Design around each result
            history_frame1 = Frame(history_example, bg="white")
            history_frame1.config(height=5, width=860)
            history_frame1.place(relx=0.5, rely=0.99, anchor="s")

            # Scrollbar if more than 5 results are displayed
            if len(history_list) > 5:
                history_sb = ttk.Scrollbar(history_canvas, orient="vertical", command=history_canvas.yview)
                history_sb.place(relx=0.98, height=300)
                history_canvas.configure(yscrollcommand=history_sb.set)


# This class will create the scan page
# This will be different whether the full scan or express scan options were selected
# Picking one of the options will load up the proper buttons for that configuration
class ScanConfirmPage:
    def __init__(self):
        global root
        global last_page
        global files_list, results_progressbar
        files_list.clear()
        list_results.clear()

    # This will setup the button for the Full Scan configuration
    def make_full_scan_config(self):
        list_results.clear()
        for widget in root.winfo_children()[1:]:
            widget.destroy()

            root.configure(background="#2a3439")

            # This lets scan() know whether to scan all program files or just selected files
            global scan_type, results_progressbar
            scan_type = "Full Scan"

            # Frame for scan confirmation dialog box
            scan_confirm_frame = Frame(root, bg="#2a3439")
            scan_confirm_frame.place(relx=0.5, rely=0.1, anchor="n")
            scan_confirm_frame.config(height=root.winfo_height(), width=root.winfo_width())

            scan_confirm_label = Label(scan_confirm_frame, text='What will be scanned:', font=14, bg="#2a3439",
                                       fg="white")
            scan_confirm_label.place(relx=0.05, rely=0.05, anchor="w")

            # Container for confirmation dialog
            scan_confirm_container = Frame(scan_confirm_frame, bg="#1F262A", borderwidth=2)
            scan_confirm_container.place(relx=0.5, rely=0.1, anchor="n")
            scan_confirm_container.config(relief=RIDGE, height=250, width=700)

            full_scan_dialog = Label(scan_confirm_container, text='Full Scan: All Program Files Will Be Scanned.',
                                     font=14, bg="#2a3439", fg="white")
            full_scan_dialog.place(relx=0.5, rely=0.5, anchor="center")

            x = threading.Thread(target=scan)

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
                                                  command=lambda: [last_time_clicked(), start(), x.start()])
            continue_button.place(relx=0.25, rely=0.8, anchor="center")
            ToolTip(continue_button, "Continue onto the scanning process.")

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
                                                command=lambda: [ResultsPage(), MainWindow(), stop()])
            cancel_button.place(relx=0.70, rely=0.8, anchor="center")
            ToolTip(cancel_button, "Go back to the home page.")

            # Makes a progress bar
            progressbar_style_element = ttk.Style()
            progressbar_style_element.theme_use('alt')
            progressbar_style_element.configure("red.Horizontal.TProgressbar", foreground='red', bg='red')
            results_progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate',
                                                  style="red.Horizontal.TProgressbar")
            results_progressbar.place(relx=0.5, rely=0.8, anchor="center")

    # This will setup the buttons for the Express Scan Function

    def make_express_config(self):
        files_list.clear()
        list_results.clear()

        x = threading.Thread(target=scan)

        global scan_type, results_progressbar
        # This lets scan() know whether to scan all program files or just selected files
        scan_type = "Express Scan"

        def browse_files():
            global files_list
            filenames = filedialog.askopenfilenames(initialdir="C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
                                                    title="Select Files",
                                                    filetypes=(("all files",
                                                                "*.*"),
                                                               ("applications",
                                                                "*.exe*")))
            # Additional files selected after first selection will be appended to list
            files_list = files_list + list(filenames)
            ctr = 0

            # Display selected files on confirm page
            for file in files_list:
                file_block = Frame(scan_confirm_container, bg="#2a3439")
                file_block.config(height=50, width=860)
                file_label = Label(file_block, text=files_list[ctr], font=14, bg="#2a3439", fg="white",
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
                                              command=lambda: [last_time_clicked(), start, x.start()])
        continue_button.place(relx=0.25, rely=0.8, anchor="center")
        ToolTip(continue_button, "Continue onto the scanning process once programs have been selected.")

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
        ToolTip(add_files_button, "Opens the File Explorer for selecting specific programs.")

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
                                            command=lambda: [ResultsPage(), MainWindow(), x.stop(), stop()])
        cancel_button.place(relx=0.70, rely=0.8, anchor="center")
        ToolTip(cancel_button, "Go back to the home page.")

        # Makes a progress bar
        progressbar_style_element = ttk.Style()
        progressbar_style_element.theme_use('alt')
        progressbar_style_element.configure("red.Horizontal.TProgressbar", foreground='red', bg='red')
        results_progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate',
                                              style="red.Horizontal.TProgressbar")
        results_progressbar.place(relx=0.5, rely=0.8, anchor="center")


# This will create the results page
class ResultsPage:
    def __init__(self):
        global root, last_page

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
            filter_settings_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
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

            # </editor-fold>

    # Function to create the update buttons before and after have results
    @staticmethod
    def create_update_buttons(results_frame):
        search_bar = Frame(results_frame)
        search_bar.config(height=50, width=50, relief=RIDGE)
        global search_entry
        search_entry = Entry(search_bar, bg="#5B676D", fg="white", width=50)
        search_entry.insert(0, 'Search...')
        search_entry.pack(side=LEFT, fill=BOTH, expand=1)
        search_button = Button(search_bar, text='Search', bg="#1F262A", fg="white", activebackground="#5F4B66",
                               activeforeground="white", command=lambda: ResultsPage.search(search_entry.get()))
        search_button.pack(side=RIGHT)
        search_bar.place(relx=0.40, rely=0.1)

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
                                                command=lambda: [UpdatePage(print_updates(list_results)),
                                                                 reset_results_list(),
                                                                 ResultsPage.print_results(sort_variable.get(),
                                                                                           filter_settings)])
        update_all_button.place(relx=0.15, rely=0.8, anchor="center")
        ToolTip(update_all_button, "Update all the programs flagged for available updates.")

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
                                                     command=lambda: [UpdatePage(print_updates(update_selected())),
                                                                        ResultsPage.print_results(sort_variable.get(),
                                                                                                    filter_settings)])
        update_selected_button.place(relx=0.35, rely=0.8, anchor="center")
        ToolTip(update_selected_button, "Update all the selected programs that were flagged for available updates.")

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
                                            command=lambda: [ResultsPage(), MainWindow()])
        cancel_button.place(relx=0.9, rely=0.8, anchor="center")
        ToolTip(cancel_button, "Go back to the home page.")

        #not functioning
        def ignore_selected():
            for i in range(len(list_results)):
                # if var.get():
                print(list_results[i] + "checked")

        ignore_selected_button = TkinterCustomButton(master=results_frame,
                                                     fg_color="#8797AF",
                                                     hover_color="#1F262A",
                                                     text_font="Bold, 14",
                                                     text="Ignore Selected",
                                                     text_color="white",
                                                     corner_radius=10,
                                                     width=200,
                                                     height=75,
                                                     hover=True,
                                                     command=lambda: [remove_selected(),
                                                                      ResultsPage.print_results(sort_variable.get(),
                                                                                       filter_settings)])
        ignore_selected_button.place(relx=0.75, rely=0.8, anchor="center")
        ToolTip(ignore_selected_button, "Ignore all the selected programs that were flagged for available updates.")

        ignore_all_button = TkinterCustomButton(master=results_frame,
                                                fg_color="#848689",
                                                hover_color="#1F262A",
                                                text_font="Bold, 14",
                                                text="Ignore All",
                                                text_color="white",
                                                corner_radius=10,
                                                width=200,
                                                height=75,
                                                hover=True,
                                                command=lambda: [ResultsPage(), MainWindow(), reset_results_list()])
        ignore_all_button.place(relx=0.55, rely=0.8, anchor="center")
        ToolTip(ignore_all_button, "Ignore all the programs flagged for available updates.")

        ## Sort Settings
        sort_settings_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
        sort_settings_container.place(relx=0.04, rely=0.0, anchor="nw")
        sort_settings_container.config(relief=RIDGE)

        sort_scan_label = Label(sort_settings_container, text='Sort scan results...', font='2', bg='#2a3439',
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
        sort_variable = StringVar(sort_settings_container)
        # Default sorting is by severity
        sort_variable.set("By Severity")

        opt = OptionMenu(sort_settings_container, sort_variable, *option_list)
        opt.config(background="#1F262A", foreground="white", width=15, font=('Bold', 12))
        opt.grid()

        ## Refresh the page
        refresh_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
        refresh_container.place(relx=0.1, rely=0.1)
        refresh_container.config(relief=RIDGE)

        refresh_button = TkinterCustomButton(master=results_frame,
                                             fg_color="#2a3439",
                                             hover_color="#1F262A",
                                             text_font="Bold, 24",
                                             text="???",
                                             text_color="white",
                                             corner_radius=10,
                                             width=50,
                                             height=50,
                                             hover=True,
                                             command=lambda: ResultsPage.print_results(sort_variable.get(),
                                                                                       filter_settings))
        refresh_button.place(relx=0.31, rely=0.025)

        ## Filter settings
        filter_settings_container = Frame(results_frame, bg="#1F262A", borderwidth=2)
        filter_settings_container.place(relx=0.4, rely=0.0, anchor="nw")
        filter_settings_container.config(relief=RIDGE)

        filter_label = ttk.Label(filter_settings_container, text='Filter Settings', font='2', background="#1F262A",
                                 foreground="white")
        filter_label.grid(row=1, column=2, columnspan=2)

        for i in range(4):
            filter_settings.append(IntVar())

        frame_style = ttk.Style()
        frame_style.configure("BW.TCheckbutton", background="#1F262A", foreground="white", highlightthickness=0)

        filter_button_1 = ttk.Checkbutton(filter_settings_container, text='Hide low', onvalue=1, offvalue=0,
                                          variable=filter_settings[0], style="BW.TCheckbutton",
                                          command=lambda: ResultsPage.print_results(sort_variable.get(), filter_settings))
        filter_button_1.grid(row=2, column=1, padx=20)
        filter_button_2 = ttk.Checkbutton(filter_settings_container, text='Hide medium', onvalue=1, offvalue=0,
                                          variable=filter_settings[1], style="BW.TCheckbutton",
                                          command=lambda: ResultsPage.print_results(sort_variable.get(), filter_settings))
        filter_button_2.grid(row=2, column=2, padx=20)
        filter_button_3 = ttk.Checkbutton(filter_settings_container, text='Hide high', onvalue=1, offvalue=0,
                                          variable=filter_settings[2], style="BW.TCheckbutton",
                                          command=lambda: ResultsPage.print_results(sort_variable.get(), filter_settings))
        filter_button_3.grid(row=2, column=3, padx=20)
        filter_button_4 = ttk.Checkbutton(filter_settings_container, text='Hide critical', onvalue=1, offvalue=0,
                                          variable=filter_settings[3], style="BW.TCheckbutton",
                                          command=lambda: ResultsPage.print_results(sort_variable.get(), filter_settings))
        filter_button_4.grid(row=2, column=4, padx=20)

        style = ttk.Style(root)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(root)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)
        # </editor-fold>

    # This will take the software found from a scan
    # And print them to the results page
    @staticmethod
    def print_results(sorting, filter_settings):
        global sort_variable, list_results, results_names, results_container

        # This list stores program names as displayed in results.
        # Used by Search Bar.
        results_names = []

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

        temp_list_results = []
        individual_record_list = []
        if sorting == 'By Severity':
            for record_list in list_results:
                rating = 0.0
                for record in record_list:
                    rating += float(record[-2])
                rating = rating / float(len(record_list))
                temp_list_results.append([rating, record_list])
            temp_list_results.sort()
            list_results = []
            for record_list in reversed(temp_list_results):
                list_results.append(record_list[-1])

        elif sorting == 'By Time':
            for record_list in list_results:
                individual_record_list = []
                for record in record_list:
                    individual_record_list.append((record[-3], record))
                individual_record_list.sort()
                temp_list_results.append(individual_record_list)
            temp_list_results.sort()
            list_results = []
            temp_list = []
            for record_list in temp_list_results:
                temp_list = []
                for record in record_list:
                    temp_list.append(record[-1])
                list_results.append(temp_list)

        elif sorting == 'Alphabetically':
            for record_list in list_results:
                individual_record_list = []
                for record in record_list:
                    individual_record_list.append((record[-1].split('/')[-1].upper(), record))
                individual_record_list.sort()
                temp_list_results.append(individual_record_list)
            temp_list_results.sort()
            list_results = []
            temp_list = []
            for record_list in temp_list_results:
                temp_list = []
                for record in record_list:
                    temp_list.append(record[-1])
                list_results.append(temp_list)

        for widget in results_container.winfo_children():
            widget.destroy()

        # This loop will run for the amount of items that are found to have vulnerabilities in the Database
        # It will send a String to the results page with the information
        # It will only run as many times as vulnerabilities found
        for i in range(len(list_results)):

            rating = 0

            # Getting the score and changing the color to match the new rating
            for j in list_results[i]:
                rating += float(j[-2])
            rating = rating / float(len(list_results[i]))

            if rating < 4:
                color = "limegreen"
                rating = "Low"
            elif 4 <= rating < 7:
                color = "yellow"
                rating = "Medium"
            elif 7 <= rating < 9:
                color = "orange"
                rating = "High"
            else:
                color = "red"
                rating = "Critical"

            if rating == "Low":
                if filter_settings[0].get() == 1:
                    continue
            elif rating == "Medium":
                if filter_settings[1].get() == 1:
                    continue
            elif rating == "High":
                if filter_settings[2].get() == 1:
                    continue
            elif rating == "Critical":
                if filter_settings[3].get() == 1:
                    continue

            results_example = Frame(results_container, bg="#2a3439")
            results_example.config(height=50, width=860)
            results_example1_label = Label(results_example, text=str(list_results[i][0][-1].split('/')[-1]), font=14,
                                           bg="#2a3439", fg="#FFFFFF")

            results_example1_label.place(relx=0.05, rely=0.5, anchor="w")

            # Selection Boxes
            check_buttons.append(IntVar())

            selection_box = Checkbutton(results_example, variable=check_buttons[i], onvalue=1, offvalue=0, bg="#2a3439")
            selection_box.place(relx=0.00, rely=0.5, anchor="w")
            results_example.bind("<Button-1>", new_page)
            results_example.grid(row=i, column=0, padx=10, pady=5)



            # Label for Rating
            rating_label = Label(results_example, text=rating, font=14, bg=color, fg="black")
            rating_label.config(height=2, width=7)
            rating_label.place(relx=0.904, rely=0.5, anchor="w")

            # Design around each result
            rate_frame1 = Frame(results_example, bg=color)
            rate_frame1.config(height=5, width=860)
            rate_frame1.place(relx=0.5, rely=0.99, anchor="s")

            # Label for Flags

            # takes the oldest date a vulnerablility was discovered and compares it to the current date
            # If 365 days or more, will setup a flag
            limit = datetime.timedelta(days=365)
            compareDate = list_results[i][-1][-3].rsplit("-")
            daysSince = datetime.date.today() - datetime.date(int(compareDate[0]), int(compareDate[1]),
                                                              int(compareDate[2]))
            if daysSince >= limit:
                flags_label = Label(results_example, text="Flagged! " + str(daysSince.days) + " days old", font=8, bg=color, fg="black")
                flags_label.config(height=2, width=30)
                flags_label.place(relx=0.5, rely=0.5, anchor="w")

            # Scrollbar if more than 5 files are selected
            if len(list_results) > 5:
                results_sb = ttk.Scrollbar(results_canvas, orient="vertical",
                                           command=results_canvas.yview)
                results_sb.place(relx=0.98, height=300)
                results_canvas.configure(yscrollcommand=results_sb.set)


        # If search bar is empty, re-print original results.
        # Otherwise, hide results that don't contain the keyword;
        # Leave those that do.
        def search(keyword):
            if keyword == '':
                for result in results_container.winfo_children():
                    if result.winfo_class() == 'Frame':
                        result.grid()
            elif not any(keyword in result for result in results_names):
                search_entry.insert(0, "No results match keyword ")
            else:
                for result in results_container.winfo_children():
                    if result.winfo_class() == 'Frame':
                        result.grid()
                for widget in results_container.winfo_children():
                    if widget.winfo_class() == 'Frame':
                        for child in widget.winfo_children():
                            if child.winfo_class() == 'Label' and '.' in child.cget("text"):
                                if keyword in child.cget("text"):
                                    pass
                                else:
                                    widget.grid_forget()


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
            help_example1.config(height=220, width=1060)
            help_example1_header_label = Label(help_example1, text='How to use the program:', font=24, bg="#2a3439",
                                               fg="#FFFFFF")
            help_example1_header_label.place(relx=0.01, rely=0.01, anchor="nw")

            text1 = """First after logging in, you have a choice of what to do. If choose to run a scan this can be done 
                    clicking onto the home page. From here you have the choice of what kind of scan you would like to run. 
                    Mousing over the options will give a brief description of the differences between them. From there you 
                    will be directed to the Results Page. Here the applications that have vulnerabilities will be listed. If 
                    the user that is logged in has the permissions, they will be able to update the application from here. 
                    Otherwise they will just be able to see the vulnerabilities. If instead the Results page is clicked, 
                    this will display the results from the scan that was last run. And lastly if the Settings Page is selected, 
                    this will bring you to a page where you can change options such as font size and the way items are sorted to make the 
                    tool as easy to use as possible.""" \
                .replace('\n', ' ').replace('                    ', '')
            help_example1_body_label = Label(help_example1, text=text1, font=14, bg="#2a3439", fg="#FFFFFF",
                                             wraplength=1060, justify="left")
            help_example1_body_label.place(relx=0.01, rely=0.125, anchor="nw")

            help_example2 = Frame(help_frame, bg="#2a3439")
            help_example2.place(relx=0.5, rely=0.02, anchor="n")
            help_example2.config(height=140, width=1064)
            help_example2_header_label = Label(help_example2, text='How the Vulnerabilities are scored:', font=24,
                                               bg="#2a3439", fg="#FFFFFF")
            help_example2_header_label.place(relx=0.01, rely=0.01, anchor="nw")

            text2 = """To score the vulnerabilities we will be interfacing with the a CVSS 2.0 scorer.
                    CVSS or better known as the Common Vulnerability Scoring System will take in a number of parameters
                    in order to delivery an accurate threat score. Some of the items taken into account when calculating
                    a score are the Access Vector, Access Complexity, Authentication, Confidentiality Impact, Integrity Impact,
                    and lastly the Availability Impact.
            """ \
                .replace('\n', ' ').replace('                    ', '')
            help_example2_body_label = Label(help_example2, text=text2, font=14, bg="#2a3439", fg="#FFFFFF",
                                             wraplength=1060, justify="left")
            help_example2_body_label.place(relx=0.01, rely=0.25, anchor="nw")

            help_example3 = Frame(help_frame, bg="#2a3439")
            help_example3.place(relx=0.5, rely=0.02, anchor="n")
            help_example3.config(height=168, width=1060)
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
            help_example3_body_label = Label(help_example3, text=text3, font=14, bg="#2a3439", fg="#FFFFFF",
                                             wraplength=1060, justify="left")
            help_example3_body_label.place(relx=0.01, rely=0.3, anchor="nw")
            # Align tips in a grid
            help_example1.grid(row=0, column=0, padx=10, pady=5)
            help_example2.grid(row=1, column=0, padx=10, pady=5)
            help_example3.grid(row=2, column=0, padx=10, pady=5)


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

            settings_frame = Frame(root)
            settings_frame.place(relx=0.5, rely=0.5, anchor='center')
            settings_frame.config(height=500, width=700)
            settings_frame.config(relief=RIDGE, background="#1F262A")

            settings_page_label = ttk.Label(settings_frame, text='Settings', font= 'bold, 14', background="#1F262A",
                                            foreground="white")
            settings_page_label.place(relx=0.5, rely=0.15, anchor='center')

            frame_style = ttk.Style()
            frame_style.configure("BW.TFrame", background="#1F262A")

            set_options_frame = ttk.Frame(settings_frame)
            set_options_frame.place(relx=0.5, rely=0.5, anchor='center')
            set_options_frame.config(height=300, width=500, style="BW.TFrame")
            set_options_frame.config(relief=RIDGE)
            set_options_frame.config(padding=(30, 15))

            text_size_label = ttk.Label(set_options_frame, text='Days Until Flagged', background="#1F262A", foreground="white")
            text_size_label.grid(row=0, column=0, padx=50, pady=30)

            txt_size_entry = ttk.Entry(set_options_frame, width=5)
            txt_size_entry.grid(row=0, column=2)
            txt_size_entry.insert(0, '365')

            set_3_label = ttk.Label(set_options_frame, text='When scan finishes...', background="#1F262A",
                                    foreground="white")
            set_3_label.grid(row=2, column=0, padx=50)
            after_scan = StringVar()

            frame_style = ttk.Style()
            frame_style.configure("BW.TRadiobutton", background="#1F262A", foreground="white", highlightthickness=0)

            set_3_button_1 = ttk.Radiobutton(set_options_frame, text='Do Nothing', variable=after_scan, value='nothing',
                                             style="BW.TRadiobutton")
            set_3_button_1.grid(row=2, column=2)
            set_3_button_2 = ttk.Radiobutton(set_options_frame, text='Close the program', variable=after_scan,
                                             style="BW.TRadiobutton", value='close')
            set_3_button_2.grid(row=3, column=2)

            reset_settings_label = ttk.Label(set_options_frame, text='Reset Default Settings', background="#1F262A",
                                             foreground="white")
            reset_settings_label.grid(row=5, column=0, padx=50, pady=30)
            reset_button = Button(set_options_frame, text='Reset', bg="#2a3439", fg="white")
            reset_button.grid(row=5, column=2)

            apply_button = Button(settings_frame, text='Apply', bg="#2a3439", fg="white")
            apply_button.place(relx=0.5, rely=0.95, anchor='center')


class LoginPage:

    def __init__(self):
        global root
        global last_page
        error = ""
        username_var = StringVar(value="")
        password_var = StringVar(value="")

        if last_page != "LoginPage":
            last_page = "LoginPage"

            for widget in root.winfo_children()[1:]:
                widget.destroy()
            for widget in title_bar.winfo_children()[4:]:
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

            # Login username and Password labels and entries
            username_label = Label(login_inner_frame, text='Username', font=15, background="#2a3439",
                                   foreground="white")
            username_label.place(relx=0.5, rely=0.3, anchor="center")
            username_entry = Entry(login_inner_frame, textvariable=username_var, background="#1F262A",
                                   foreground="white", font=15)
            username_entry.place(relx=0.5, rely=0.4, anchor='center')

            password_label = Label(login_inner_frame, text='Password', font=15, background="#2a3439",
                                   foreground="white")
            password_label.place(relx=0.5, rely=0.53, anchor='center')
            password_entry = Entry(login_inner_frame, textvariable=password_var, show='*', background="#1F262A",
                                   insertbackground="#1F262A",
                                   foreground="white",
                                   font=15)
            password_entry.place(relx=0.5, rely=0.63, anchor='center')
            global show_pass
            show_pass = False

            toggle_label = Label(login_inner_frame, text='Show Password', font='Bold, 10', background="#2a3439",
                                 foreground="grey")
            toggle_label.place(relx=0.52, rely=0.73, anchor='center')

            # Create Show Password Button
            show_password_button = TkinterCustomButton(master=login_inner_frame,
                                                       bg_color="#2a3439",
                                                       fg_color="#56667A",
                                                       hover_color="#AAA9AD",
                                                       text_font="Bold, 12",
                                                       text=" ",
                                                       text_color="white",
                                                       corner_radius=2,
                                                       width=20,
                                                       height=20,
                                                       hover=True,
                                                       command=lambda: toggle_password1())
            show_password_button.place(relx=0.4, rely=0.73, anchor='center')

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
            ToolTip(login_button, "Login into the Software Inventory Tool.")

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
            ToolTip(register_button, "Register for an account to use the Software Inventory Tool.")

        # Search through user list. Return True if user and password are correct.
        def check_login():
            global user_list, name, role, error
            username = username_entry.get()
            password = password_entry.get()
            exists = False
            error = "Login Error"
            for i in range(len(user_list)):

                # Check to see if account is locked
                # Sets error code
                if user_list[i][2] == username and int(user_list[i][5]) >= 5:
                    error = "Too many attempts. Account has been locked."
                    return exists

                # Increment the account_status if the username is right but the password is wrong
                # Sets error code
                if user_list[i][2] == username and user_list[i][3] != password:
                    user_list[i][5] = str(int(user_list[i][5]) + 1)
                    error = "Wrong Username or Password."
                    return exists

                # Checks for combination of user, password, and account_status to be valid
                if user_list[i][2] == username and user_list[i][3] == password and int(user_list[i][5]) < 5:
                    exists = True
                    name = user_list[i][0] + " " + user_list[i][1]
                    role = user_list[i][4]
                    MakeWindow.make_nav_buttons(self)
            return exists

        # Make error message for login
        def login_error():
            global error
            error_message = LabelFrame(login_inner_frame, bg="#2a3439", fg="red", font=10,
                                       text=error, relief=FLAT, labelanchor="n")
            error_message.place(relx=0.5, rely=0.68, anchor="n")
            error_message.config(height=26, width=340)
            error_message.after(3000, lambda: error_message.destroy())

        def enter_login(e):
            if check_login():
                MainWindow()
                root.unbind('<Return>', None)
            else:
                login_error()

        root.bind('<Return>', enter_login)

        # Changes password to be visible or not
        def toggle_password1():
            if password_entry.cget('show') == '':
                password_entry.config(show='*')
                toggle_label.config(text='Show Password')
            else:
                password_entry.config(show='')
                toggle_label.config(text='Hide Password')


class RegisterPage:
    first_name_var: StringVar
    last_name_var: StringVar
    username_var: StringVar
    password_var: StringVar
    role_var: StringVar

    def __init__(self):
        global root
        global last_page

        # Initialize input variables
        self.first_name_var = StringVar(value="")
        self.last_name_var = StringVar(value="")
        self.username_var = StringVar(value="")
        self.password_var = StringVar(value="")
        self.role_var = StringVar(value="")
        self.conf_password_var = StringVar(value="")

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
            first_name_frame.place(relx=.16003, rely=.2)
            first_name_entry = Entry(register_frame, textvariable=self.first_name_var, background="#2a3439",
                                     foreground="white", width=25, font=20)
            first_name_entry.place(relx=.4, rely=.2)

            last_name_frame = Label(register_frame, text="Last Name", background="#1F262A", foreground="white", font=20)
            last_name_frame.place(relx=.16001, rely=.3)
            last_name_entry = Entry(register_frame, textvariable=self.last_name_var, background="#2a3439",
                                    foreground="white", width=25, font=20)
            last_name_entry.place(relx=.4, rely=.3)

            username_frame = Label(register_frame, text="Username", background="#1F262A", foreground="white", font=20)
            username_frame.place(relx=.1703, rely=.4)
            username_entry = Entry(register_frame, textvariable=self.username_var, background="#2a3439",
                                   foreground="white",
                                   width=25, font=20)
            username_entry.place(relx=.4, rely=.4)

            password_frame = Label(register_frame, text="Password", background="#1F262A", foreground="white", font=20)
            password_frame.place(relx=.1703, rely=.5)
            password_entry = Entry(register_frame, textvariable=self.password_var, background="#2a3439",
                                   foreground="white",
                                   width=25, font=20)
            password_entry.place(relx=.4, rely=.5)

            conf_password_frame = Label(register_frame, text="Confirm Password", background="#1F262A",
                                        foreground="white", font=20)
            conf_password_frame.place(relx=.05, rely=.6)
            conf_password_entry = Entry(register_frame, textvariable=self.conf_password_var, background="#2a3439",
                                        foreground="white",
                                        width=25, font=20)
            conf_password_entry.place(relx=.4, rely=.6)

            # Label for roles
            role_frame = Label(register_frame, text="Role", background="#1F262A", foreground="white", font=20)
            role_frame.place(relx=.25, rely=.7)
            # Style for radio buttons
            frame_style = ttk.Style()
            frame_style.configure("BW.TRadiobutton", background="#1F262A", foreground="white", highlightthickness=0)
            # Admin radio button
            admin_radio_button = ttk.Radiobutton(register_frame, text='Admin', variable=self.role_var, value='Admin',
                                                 style="BW.TRadiobutton")
            admin_radio_button.place(relx=.4, rely=.71)
            # User radio button
            user_radio_button = ttk.Radiobutton(register_frame, text='User', variable=self.role_var, value='User',
                                                style="BW.TRadiobutton")
            user_radio_button.place(relx=.60, rely=.71)

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
                                                command=lambda: [
                                                    enter_register() if valid_register() else registration_error()])
            create_button.place(relx=0.35, rely=0.9, anchor='center')
            ToolTip(create_button, "Create an account using the provided information.")

            # Back Button (sends you back to login page)
            back_button = TkinterCustomButton(master=register_frame,
                                              bg_color="#1F262A",
                                              fg_color="#56667A",
                                              hover_color="#AAA9AD",
                                              text_font=20,
                                              text="Back",
                                              text_color="white",
                                              corner_radius=10,
                                              width=100,
                                              height=30,
                                              hover=True,
                                              command=lambda: [LoginPage()])
            back_button.place(relx=0.65, rely=0.9, anchor='center')
            ToolTip(back_button, "Go back to the Login Page.")

            # Register new user

        def valid_register():
            global user_list
            valid = True

            if self.password_var.get() != self.conf_password_var.get():
                valid = False
                return valid

            username = self.username_var.get()
            for i in range(len(user_list)):
                if username == user_list[i][2]:
                    valid = False
                    return valid

            if len(self.first_name_var.get()) == 0:
                valid = False
                return valid
            if len(self.last_name_var.get()) == 0:
                valid = False
                return valid
            if len(self.username_var.get()) == 0:
                valid = False
                return valid
            if len(self.password_var.get()) == 0:
                valid = False
                return valid
            if len(self.role_var.get()) == 0:
                valid = False
                return valid

            return valid

        def enter_register():
            # Get new users info
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            role = self.role_var.get()
            account_status = 0
            # Add new user to user list
            new_account = [first_name, last_name, username, password, role, account_status]
            user_list.append(new_account)
            LoginPage()

        def registration_error():
            error_message = LabelFrame(register_frame, bg="#1F262A", fg="red", font=10,
                                       text="Registration Error", relief=FLAT, labelanchor="n")
            error_message.place(relx=0.5, rely=0.78, anchor="n")
            error_message.config(height=20, width=170)
            error_message.after(2000, lambda: error_message.destroy())


        root.bind('<Return>', enter_register)


class ApplicationResultsPage:
    global list_results, history_comments

    def __init__(self, result_num):
        # Toplevel object which will
        # be treated as a new window
        new_window = Toplevel(root)

        # Toplevel widget
        new_window.title("New Window")

        # Window background color
        new_window.configure(background="#2a3439")

        # Scaling UI to user's screen
        app_width = 1064
        app_height = 600
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        new_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        new_window.resizable(True, True)

        # Changes the default tkinter to our Sieve logo when minimized
        new_window.iconbitmap('logo.ico')

        # Change the text after minimizing the tool to task bar
        new_window.title("Sieve")

        # Removes title bar
        # newWindow.overrideredirect(True)
        # newWindow.minimized = False  # only to know if root is minimized
        # newWindow.maximized = False  # only to know if root is maximized

        main_frame = Frame(new_window, bg="#2a3439")
        main_frame.place(relx=0.5, rely=0.1, anchor="n")
        main_frame.config(height=new_window.winfo_height(), width=new_window.winfo_width())

        application_canvas = Canvas(main_frame, height=500, width=700, bg="#2a3439")
        application_canvas.place(relx=0.5, rely=0.00, anchor="n")

        # Container for results
        application_container = Frame(application_canvas, bg="#1F262A", borderwidth=2)
        application_container.place(relx=0.5, rely=0.1, anchor="n")
        application_container.config(relief=RIDGE, height=350, width=700)

        # Bind scrollbar to container
        application_container.bind(
            "<Configure>",
            lambda e: application_canvas.configure(
                scrollregion=application_canvas.bbox("all")
            )
        )
        application_canvas.create_window((0, 0), window=application_container, anchor="nw")

        style = ttk.Style(new_window)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(new_window)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)



        # Login username and Password labels and entries
        file_name_label = Label(application_container, text=list_results[result_num][0][-1], font=15, background="#2a3439",
                                foreground="white")
        file_name_label.grid(row=1, column=0)

        for i in range(len(list_results)):
            count = 2
            for j in list_results[result_num]:
                cvss_score_label = Label(application_container, text=str(f'\nCVE: {j[0]}     Rating: {j[-2]}    Date: {j[-3]}'),
                                         font=15, background="#2a3439", foreground="white")
                cvss_score_label.grid(row=count, column=0)

                cvss_description_label = Label(application_container, text=str(f'Description: {j[1]}') , font = 15,
                                               wraplength=650, background="#2a3439",
                                               foreground="white")
                cvss_description_label.grid(row=count+1, column=0)
                count += 2

        comment_label = Label(application_container, text="Enter a comment below...", font=15, background="#2a3439",
                                foreground="white")
        comment_label.grid(row=count+1, column=0)

        comment_text = Text(application_container, font=15, background="#2a3439", foreground="white", height=10, width=70)
        comment_text.grid(row=count+2, column=0)

        submit_comment_button = TkinterCustomButton(master=application_container,
                                                    fg_color="#848689",
                                                    hover_color="#1F262A",
                                                    text_font="Bold, 14",
                                                    text="Submit Comment",
                                                    text_color="white",
                                                    corner_radius=10,
                                                    width=170,
                                                    height=35,
                                                    hover=True,
                                                    command=lambda: update_comments(result_num,
                                                                                    comment_text.get("1.0", 'end-1c')))
        submit_comment_button.grid(row=count+3, column=0)

        # Scrollbar
        application_sb = ttk.Scrollbar(application_canvas, orient="vertical", command=application_canvas.yview)
        application_sb.place(relx=0.98, height=500)
        application_canvas.configure(yscrollcommand=application_sb.set)


class HistoryLogPage:
    global history_list, history_comments

    def __init__(self, result_num):
        # Toplevel object which will
        # be treated as a new window
        new_window = Toplevel(root)

        # Toplevel widget
        new_window.title("New Window")

        # Window background color
        new_window.configure(background="#2a3439")

        # Scaling UI to user's screen
        app_width = 1064
        app_height = 600
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        new_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        new_window.resizable(True, True)

        # Changes the default tkinter to our Sieve logo when minimized
        new_window.iconbitmap('logo.ico')

        # Change the text after minimizing the tool to task bar
        new_window.title("Sieve")

        # Removes title bar
        # newWindow.overrideredirect(True)
        # newWindow.minimized = False  # only to know if root is minimized
        # newWindow.maximized = False  # only to know if root is maximized

        main_frame = Frame(new_window, bg="#2a3439")
        main_frame.place(relx=0.5, rely=0.1, anchor="n")
        main_frame.config(height=new_window.winfo_height(), width=new_window.winfo_width())

        history_log_canvas = Canvas(main_frame, height=500, width=700, bg="#2a3439")
        history_log_canvas.place(relx=0.5, rely=0.00, anchor="n")

        # Container for results
        history_log_container = Frame(history_log_canvas, bg="#1F262A", borderwidth=2)
        history_log_container.place(relx=0.5, rely=0.1, anchor="n")
        history_log_container.config(relief=RIDGE, height=350, width=700)

        # Bind scrollbar to container
        history_log_container.bind(
            "<Configure>",
            lambda e: history_log_canvas.configure(
                scrollregion=history_log_canvas.bbox("all")
            )
        )
        history_log_canvas.create_window((0, 0), window=history_log_container, anchor="nw")


        style = ttk.Style(new_window)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(new_window)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)

        count = 0
        record_counter = 0
        for record_list in history_list[result_num][1]:

            # Login username and Password labels and entries
            file_name_label = Label(history_log_container, text=record_list[0][-1], font=15, background="#2a3439",
                                    foreground="white")
            file_name_label.grid(row=count, column=0)
            count += 1

            for record in record_list:
                cvss_score_label = Label(history_log_container, text=str(f'CVE: {record[0]}     Rating: {record[-2]}    Date: {record[-3]}'),
                                         font=15, background="#2a3439", foreground="white")
                cvss_score_label.grid(row=count, column=0)
                count += 1
            try:
                comment_label = Label(history_log_container, text=f'Comments: \n{history_comments[history_counter][record_counter]}',
                                  font=15, background="#2a3439", foreground="white")
                comment_label.grid(row=count+1, column=0)
            except:
                comment_label = Label(history_log_container, text='No Comments',
                                      font=15, background="#2a3439", foreground="white")
                comment_label.grid(row=count + 1, column=0)
            count += 2
            record_counter += 1

        # Scrollbar
        history_log_sb = ttk.Scrollbar(history_log_canvas, orient="vertical", command=history_log_canvas.yview)
        history_log_sb.place(relx=0.98, height=500)
        history_log_canvas.configure(yscrollcommand=history_log_sb.set)


class UpdatePage:

    def __init__(self, update_list):
        # Toplevel object which will
        # be treated as a new window
        new_window = Toplevel(root)

        # Toplevel widget
        new_window.title("New Window")

        # Window background color
        new_window.configure(background="#2a3439")

        # Scaling UI to user's screen
        app_width = 500
        app_height = 400
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        new_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        new_window.resizable(True, True)

        # Changes the default tkinter to our Sieve logo when minimized
        new_window.iconbitmap('logo.ico')

        # Change the text after minimizing the tool to task bar
        new_window.title("Sieve")

        # Removes title bar
        # newWindow.overrideredirect(True)
        # newWindow.minimized = False  # only to know if root is minimized
        # newWindow.maximized = False  # only to know if root is maximized

        main_frame = Frame(new_window, bg="#2a3439")
        main_frame.place(relx=0.5, rely=0.1, anchor="n")
        main_frame.config(height=new_window.winfo_height(), width=new_window.winfo_width())

        update_label = Label(main_frame, text='The following programs may require an update\n'
                                              'To retrieve the most recent version of each\n'
                                              'application, visit the main distribution page\n', font=15, background="#2a3439",
                                foreground="white")
        update_label.grid(row=0, column=0)

        count = 1
        for record in update_list:

            record_label = Label(main_frame, text=record, font=15,
                                 background="#2a3439",
                                 foreground="white")
            record_label.grid(row=count, column=0)
            count += 1


class AdminPage:
    def __init__(self):
        global root
        global last_page

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        last_page="AdminPage"

        root.configure(background="#2a3439")
        style = ttk.Style(root)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(root)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)

        AdminPage.print_admin()

    @staticmethod
    def print_admin():
        global user_list

        admin_frame = Frame(root, bg="#2a3439")
        admin_frame.place(relx=0.5, rely=0.1, anchor="n")
        admin_frame.config(height=root.winfo_height(), width=root.winfo_width())

        # Label: "Users"
        users_label = Label(admin_frame, text="Users", font=("Bold", 18), bg="#2a3439", fg="white")
        users_label.place(relx=0.1, rely=0.1)

        # Refresh Button (unlocks account)
        refresh_button = TkinterCustomButton(master=admin_frame,
                                             bg_color="#2a3439",
                                             fg_color="#56667A",
                                             hover_color="#AAA9AD",
                                             text_font=10,
                                             text="Refresh",
                                             text_color="white",
                                             corner_radius=10,
                                             width=100,
                                             height=30,
                                             hover=True,
                                             command=lambda: [AdminPage()])
        refresh_button.place(relx=0.1, rely=0.7)

        admin_canvas = Canvas(admin_frame, height=300, width=900, bg="#2a3439")
        admin_canvas.place(relx=0.5, rely=0.15, anchor="n")

        # Container for users
        admin_container = Frame(admin_canvas, bg="#1F262A", borderwidth=2)
        admin_container.place(relx=0.5, rely=0.1, anchor="n")
        admin_container.config(relief=RIDGE, height=350, width=900)

        # Bind scrollbar to container
        admin_container.bind(
            "<Configure>",
            lambda e: admin_canvas.configure(
                scrollregion=admin_canvas.bbox("all")
            )
        )
        admin_canvas.create_window((0, 0), window=admin_container, anchor="nw")

        # This loop will run for the amount of users in user_list
        # It will send the user information to the admin page with the information
        # It will only run as many times as vulnerabilities found
        for i in range(len(user_list)):
            for a in range(len(user_list[i])):
                admin_example = Frame(admin_container, bg="#2a3439")
                admin_example.config(height=50, width=860)
                admin_example1_label = Label(admin_example, text=str(user_list[i][2]), font=10,
                                             bg="#2a3439", fg="#FFFFFF")
                admin_example1_label.place(relx=0.01, rely=0.5, anchor="w")
                admin_example.bind("<Button-1>", new_user_page)
                admin_example.grid(row=i, column=0, padx=10, pady=5)

            # Design around each result
            if int(user_list[i][5]) >= 5:
                color = "coral1"
            else:
                color = "aquamarine1"
            admin_frame1 = Frame(admin_example, bg=color)
            admin_frame1.config(height=5, width=860)
            admin_frame1.place(relx=0.5, rely=0.99, anchor="s")

        # Scrollbar if more than 5 users are displayed
        if len(user_list) > 5:
            admin_sb = ttk.Scrollbar(admin_canvas, orient="vertical", command=admin_canvas.yview)
            admin_sb.place(relx=0.98, height=300)
            admin_canvas.configure(yscrollcommand=admin_sb.set)


class ApplicationAdminPage:
    global user_list

    def __init__(self, user_num):
        global account_status
        # Toplevel object which will
        # be treated as a new window
        new_window = Toplevel(root)

        # Toplevel widget
        new_window.title("New Window")

        # Window background color
        new_window.configure(background="#2a3439")

        # Scaling UI to user's screen
        app_width = 700
        app_height = 400
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        new_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        new_window.resizable(True, True)

        # Changes the default tkinter to our Sieve logo when minimized
        new_window.iconbitmap('logo.ico')

        # Change the text after minimizing the tool to task bar
        new_window.title("Sieve")

        main_frame = Frame(new_window, bg="#2a3439")
        main_frame.place(relx=0.5, rely=0.1, anchor="n")
        main_frame.config(height=new_window.winfo_height(), width=new_window.winfo_width())

        style = ttk.Style(new_window)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(new_window)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)

        # Setting each users attributes to variables
        first_name = user_list[user_num][0]
        last_name = user_list[user_num][1]
        username = user_list[user_num][2]
        password = user_list[user_num][3]
        role = user_list[user_num][4]

        # Checking for status of the account
        if int(user_list[user_num][5]) >= 5:
            account_status = "Locked"
        else:
            account_status = "Unlocked"

        # Static labels for each attribute
        first_name_label1 = Label(main_frame, text="First Name: ", font=15, background="#2a3439", foreground="white")
        last_name_label1 = Label(main_frame, text="Last Name: ", font=15, background="#2a3439", foreground="white")
        username_label1 = Label(main_frame, text="Username: ", font=15, background="#2a3439", foreground="white")
        password_label1 = Label(main_frame, text="Password: ", font=15, background="#2a3439", foreground="white")
        role_label1 = Label(main_frame, text="Role: ", font=15, background="#2a3439", foreground="white")
        account_status_label1 = Label(main_frame, text="Account Status: ", font=15, background="#2a3439",
                                      foreground="white")

        # Showing value of each attribute
        first_name_label2 = Label(main_frame, text=first_name, font=15, background="#2a3439", foreground="white")
        last_name_label2 = Label(main_frame, text=last_name, font=15, background="#2a3439", foreground="white")
        username_label2 = Label(main_frame, text=username, font=15, background="#2a3439", foreground="white")
        password_label2 = Label(main_frame, text=password, font=15, background="#2a3439", foreground="white")
        role_label2 = Label(main_frame, text=role, font=15, background="#2a3439", foreground="white")
        account_status_label2 = Label(main_frame, text=account_status, font=15, background="#2a3439",
                                      foreground="white")

        # Arranging static labels
        first_name_label1.grid(row=2, column=1, padx=10, pady=5)
        last_name_label1.grid(row=3, column=1, padx=10, pady=5)
        username_label1.grid(row=4, column=1, padx=10, pady=5)
        password_label1.grid(row=5, column=1, padx=10, pady=5)
        role_label1.grid(row=6, column=1, padx=10, pady=5)
        account_status_label1.grid(row=7, column=1, padx=10, pady=5)

        # Arranging variable labels
        first_name_label2.grid(row=2, column=2, padx=10, pady=5)
        last_name_label2.grid(row=3, column=2, padx=10, pady=5)
        username_label2.grid(row=4, column=2, padx=10, pady=5)
        password_label2.grid(row=5, column=2, padx=10, pady=5)
        role_label2.grid(row=6, column=2, padx=10, pady=5)
        account_status_label2.grid(row=7, column=2, padx=10, pady=5)

        # Unlock Button (unlocks account)
        unlock_button = TkinterCustomButton(master=main_frame,
                                            fg_color="aquamarine1",
                                            hover_color="#1F262A",
                                            text_font=14,
                                            text="Unlock",
                                            text_color="black",
                                            corner_radius=0,
                                            width=70,
                                            height=40,
                                            hover=True,
                                            command=lambda: [unlock_account(user_num), account_unlock()])
        unlock_button.grid(row=8, column=1, padx=10, pady=5)

        # Lock Button (locks account)
        lock_button = TkinterCustomButton(master=main_frame,
                                          fg_color="coral1",
                                          hover_color="#1F262A",
                                          text_font=14,
                                          text="Lock",
                                          text_color="black",
                                          corner_radius=0,
                                          width=70,
                                          height=40,
                                          hover=True,
                                          command=lambda: [lock_account(user_num), account_lock()])
        lock_button.grid(row=8, column=2, padx=10, pady=5)

        # Updates account status to locked
        def account_lock():
            global account_status
            account_status = "Locked"
            account_status_label2.config(text=account_status)

        # Updates account status to unlocked
        def account_unlock():
            global account_status
            account_status = "Unlocked"
            account_status_label2.config(text=account_status)


class ScheduleScanPage:
    minute_var: StringVar
    hour_var: StringVar
    day_var: StringVar
    month_var: StringVar
    year_var: StringVar

    def __init__(self):
        global root
        global last_page
        global sched_date
        global sched_list

        self.minute_var = StringVar(value="")
        self.hour_var = StringVar(value="")
        self.day_var = StringVar(value="")
        self.month_var = StringVar(value="")
        self.year_var = StringVar(value="")

        last_page = "ScheduleScanPage"

        for widget in root.winfo_children()[1:]:
            widget.destroy()

        style = ttk.Style(root)
        style.theme_use('classic')
        style.configure('Test.TSizegrip', background="#1F262A")
        root_size_grip = ttk.Sizegrip(root)

        root_size_grip.configure(style="Test.TSizegrip")
        root_size_grip.pack(side="right", anchor=SE)

        schedule_frame = Frame(root)
        schedule_frame.place(relx=0.5, rely=0.5, anchor='center')
        schedule_frame.config(height=500, width=700)
        schedule_frame.config(relief=RIDGE, background="#1F262A")

        schedule_button = TkinterCustomButton(master=schedule_frame,
                                              fg_color="aquamarine1",
                                              hover_color="aquamarine4",
                                              text_font=14,
                                              text="Schedule",
                                              text_color="black",
                                              corner_radius=0,
                                              width=90,
                                              height=40,
                                              hover=True,
                                              command=lambda: [schedule_time() if check_time() else schedule_error()])
        schedule_button.grid(row=7, column=2, padx=10, pady=5)


        # Static labels for each attribute
        minute_label = Label(schedule_frame, text="Minute: ", font=15, background="#1F262A", foreground="white")
        hour_label = Label(schedule_frame, text="Hour: ", font=15, background="#1F262A", foreground="white")
        day_label = Label(schedule_frame, text="Day: ", font=15, background="#1F262A", foreground="white")
        month_label = Label(schedule_frame, text="Month: ", font=15, background="#1F262A", foreground="white")
        year_label = Label(schedule_frame, text="Year: ", font=15, background="#1F262A", foreground="white")
        sched_list_label = Label(schedule_frame, text="Schedule List ", font=15, background="#1F262A", foreground="white")


        # Showing value of each attribute
        minute_entry = Entry(schedule_frame, textvariable=self.minute_var, background="#1F262A", foreground="white", width=3, font=20)
        hour_entry = Entry(schedule_frame, textvariable=self.hour_var, background="#1F262A", foreground="white", width=3, font=20)
        day_entry = Entry(schedule_frame, textvariable=self.day_var, background="#1F262A", foreground="white", width=3, font=20)
        month_entry = Entry(schedule_frame, textvariable=self.month_var, background="#1F262A", foreground="white", width=3, font=20)
        year_entry = Entry(schedule_frame, textvariable=self.year_var, background="#1F262A", foreground="white", width=5, font=20)

        # Arranging static labels
        minute_label.grid(row=2, column=1, padx=10, pady=5)
        hour_label.grid(row=3, column=1, padx=10, pady=5)
        day_label.grid(row=4, column=1, padx=10, pady=5)
        month_label.grid(row=5, column=1, padx=10, pady=5)
        year_label.grid(row=6, column=1, padx=10, pady=5)
        sched_list_label.grid(row=2, column=3, padx=10, pady=5)

        # Arranging variable labels
        minute_entry.grid(row=2, column=2, padx=10, pady=5)
        hour_entry.grid(row=3, column=2, padx=10, pady=5)
        day_entry.grid(row=4, column=2, padx=10, pady=5)
        month_entry.grid(row=5, column=2, padx=10, pady=5)
        year_entry.grid(row=6, column=2, padx=10, pady=5)

        for i in range(len(sched_list)):
            time = sched_list[i]
            time_label = Label(schedule_frame, text=time, font=10,
                                             bg="#1F262A", fg="white")
            time_label.grid(row=(i+3), column=3, padx=10, pady=5)



        def check_time():
            valid_time = True
            global sched_date
            current_time = datetime.datetime.now()
            try:
                sched_date = datetime.datetime(int(self.year_var.get()), int(self.month_var.get()),
                                                   int(self.day_var.get()), int(self.hour_var.get()),
                                                    int(self.minute_var.get()))
                valid_time = True
            except ValueError:
                valid_time = False

            if current_time>sched_date:
                valid_time = False

            return valid_time



        def schedule_error():
            error_message = LabelFrame(schedule_frame, bg="#1F262A", fg="red", font=10, text="Schedule Error", relief=FLAT, labelanchor="n")
            error_message.grid(row=7, column=1, padx=10, pady=5)
            error_message.config(height=20, width=170)
            error_message.after(2000, lambda: error_message.destroy())

        def schedule_time():
            sched = BackgroundScheduler(daemon=True)
            sched.add_job(sched_scan,'date', run_date=datetime.datetime(int(self.year_var.get()), int(self.month_var.get()),
                                                   int(self.day_var.get()), int(self.hour_var.get()),
                                                    int(self.minute_var.get()), 0), args=['job1'])
            sched_list.append(str(datetime.datetime(int(self.year_var.get()), int(self.month_var.get()),
                                                   int(self.day_var.get()), int(self.hour_var.get()),
                                                    int(self.minute_var.get()), 0)))
            sched.start()
            ScheduleScanPage()

        def sched_scan(job1):
            ScanConfirmPage.make_full_scan_config(self)
            x = threading.Thread(target=scan)
            sched_list.remove(sched_list[0])
            last_time_clicked(), start(), x.start()
