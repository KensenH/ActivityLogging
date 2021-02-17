import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter.font as font
from subprocess import check_output
from subprocess import Popen
import os
import psutil
import sys
import csv
import getpass
from win32com.client import Dispatch
import logging
import time
import datetime


composition = ['Date', 'Time', 'Activity', 'Path File']
opt_a = 0
opt_b = 1
opt_c = 2
opt_d = 3

fmt_date = 1
fmt_date_new = 1

class window:
    def checkConfig(self):
        #cek config sebelumnya
        if(os.path.isfile("./config.txt")):
            f = open("config.txt", "r")
            self.dir = f.readline().split('\n')
            self.Check1 = f.readline()
            # print(f"THis is check1 : {self.Check1}\n")
            f.close()

        else:
            pass

    def run(self):
        #over write config sebelumnya
        self.checkRUN()
        
        self.OG = self.Check1
        if(self.checkbox1.instate(['selected'])):
            self.Check1 = 1
        else:
            self.Check1 = 0

        fw = open("config.txt", "w")
        fw.seek(0)
        fw.write("".join(self.dir) + "\n")
        fw.write(str(self.Check1))
        fw.close()


        #set auto run
        if(str(self.Check1) == "1" and str(self.OG) == "0" or str(self.Check1) == "0" and str(self.OG) == "1"):
            self.autoRun(self.Check1)
            # print("OIK")
        #run script
        Popen('pythonw script.pyw')
        self.LabelStatus.config(text="a script is running ...")
        # end program
        # sys.exit()

    def autoRun(self, curr):
        username = getpass.getuser()
        path = r"C:\Users" + "\\" + username + r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        path = os.path.join(path, "Logging.lnk")
        if(curr == 1):
            # putSHORTCUT HERE
            filename = sys.argv[0]
            absolutepath = os.path.abspath(filename)
            target = absolutepath
            wDir = os.path.abspath(".")
            icon = absolutepath
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
        elif(curr == 0):
            os.remove(path)

    def checkRUN(self):
        #cek script yang berjalan
        if(os.path.isfile("./running.txt")):
            f = open("running.txt", "r")
            pid = int(f.readline())
            f.close()

            if psutil.pid_exists(pid):
                psutil.Process(pid).terminate()
                os.remove("running.txt")
            else:
                os.remove("running.txt")
        else:
            pass

        try:
            self.LabelStatus.config(text="No script is running ..")
        except:
            pass

    def directory(self):
        #memilih directory
        self.dir = filedialog.askdirectory()
        print(self.dir)
        if (self.dir != ""):
            self.entry1.config(state='normal')
            self.entry1.delete(0, "end")
            self.entry1.insert(0, self.dir)
            self.entry1.config(state='disabled')
            self.entry1.grid(column=1, row=2, padx = (10,10))
        else:
            pass
    #####  
    def file_opener(self):
        global filenames
        inputs = filedialog.askopenfilename(initialdir="/",
                                            title="Select a CSV File",
                                            filetypes=(("*.csv", "*.csv"), ("All Files", "*.*"))
                                            )
        
        filenames = inputs
        pathfile = tk.Label(self.entry_path, text=filenames, bg='white')
        pathfile.place(rely=0.1, relx=0.01)


    def show_log(self, name, composition, tabLog):
        # Log Data
        log_file = tk.LabelFrame(tabLog)
        log_file.place(height=490, width=699, rely=0.59, relx=0.5, anchor='center')

        scrollbarx = tk.Scrollbar(log_file, orient="horizontal")
        scrollbary = tk.Scrollbar(log_file, orient="vertical")
        
        
        global tree
        tree = ttk.Treeview(log_file, columns=("No", composition[0], composition[1], composition[2], composition[3]), height=400, selectmode="extended", 
                            yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side="right", fill="y")
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side="bottom", fill="x")
        tree.heading('No', text="No.", anchor="e")
        tree.heading('Date', text="Date", anchor="nw")
        tree.heading('Time', text="Time", anchor="nw")
        tree.heading('Activity', text="Activity", anchor="nw")
        tree.heading('Path File', text="Path File", anchor="nw")
        tree.column('#0', stretch="no", minwidth=0, width=0)
        tree.column('#1', stretch="no", minwidth=0, width=50, anchor="e")
        tree.column('#2', stretch="no", minwidth=0, width=100)
        tree.column('#3', stretch="no", minwidth=0, width=150)
        tree.column('#4', stretch="no", minwidth=0, width=100)
        tree.column('#5', stretch="no", minwidth=0, width=500)
        tree.pack()

        time.sleep(0.1)

        with open(name) as f:
            reader = csv.reader(f, delimiter=',')

            number = 0

            for row in reader:
                number += 1
                
                if opt_a == 0:
                    dates = row[opt_a]
                    checks = dates.split('-')

                    if(len(checks) < 3):
                        checks = dates.split('/')
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            dates = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            dates = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            dates = a.strftime('%d-%b-%Y')

                    else:
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            dates = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            dates = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            dates = a.strftime('%d-%b-%Y')
                else:
                    dates = row[opt_a]


                if opt_b == 0:
                    times = row[opt_b]
                    checks = times.split('-')

                    if(len(checks) < 3):
                        checks = times.split('/')
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            times = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            times = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            times = a.strftime('%d-%b-%Y')

                    else:
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            times = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            times = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            times = a.strftime('%d-%b-%Y')
                else:
                    times = row[opt_b]


                if opt_c == 0:
                    activity = row[opt_c]
                    checks = activity.split('-')

                    if(len(checks) < 3):
                        checks = activity.split('/')
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            activity = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            activity = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            activity = a.strftime('%d-%b-%Y')

                    else:
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            activity = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            activity = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            activity = a.strftime('%d-%b-%Y')
                else:
                    activity = row[opt_c]
                
                
                if opt_d == 0:
                    pathFile = row[opt_d]
                    checks = pathFile.split('-')

                    if(len(checks) < 3):
                        checks = pathFile.split('/')
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            pathFile = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            pathFile = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            pathFile = a.strftime('%d-%b-%Y')

                    else:
                        a = datetime.datetime(int(checks[0]), int(checks[1]), int(checks[2]))
                        if fmt_date == 1:
                            pathFile = a.strftime('%Y-%m-%d')
                        elif fmt_date == 2:
                            pathFile = a.strftime('%d-%m-%Y')
                        elif fmt_date == 3:
                            pathFile = a.strftime('%d-%b-%Y')
                else:
                    pathFile = row[opt_d]
                
                tree.insert("", number, values=(number, dates, times, activity, pathFile))


    def apply_set(self):
        choose_a = column_a_position.get()
        choose_b = column_b_position.get()
        choose_c = column_c_position.get()
        choose_d = column_d_position.get()

        print('Choosen Column: {} {} {} {}'.format(choose_a, choose_b, choose_c, choose_d))

        choosen = []
        choosen.append(choose_a)
        choosen.append(choose_b)
        choosen.append(choose_c)
        choosen.append(choose_d)

        status = False

        for i in choosen:
            count = 0
            for j in choosen:
                if i == j:
                    count += 1
            
            if count > 1:
                status = True
                break
        
        if status == True:
            thisError = messagebox.showerror('Error Message', 'Each column can only have 1 column name !')
        else:
            global composition, opt_a, opt_b, opt_c, opt_d

            choose_a = int(choose_a) - 1
            composition[choose_a] = 'Date'
            
            choose_b = int(choose_b) - 1
            composition[choose_b] = 'Time'

            choose_c = int(choose_c) - 1
            composition[choose_c] = 'Activity'
            
            choose_d = int(choose_d) - 1
            composition[choose_d] = 'Path File'
            
            thisSuccess = messagebox.showinfo('Success Message', 'Change Successfull\nTo see the changes, go to menu Log > then click Show button')

            opt_a = choose_a
            opt_b = choose_b
            opt_c = choose_c
            opt_d = choose_d
            # print(composition)

    def on_enter(self, e):
        menuShow_log['background'] = 'gray'

    def on_leave(self, e):
        menuShow_log['background'] = 'SystemButtonFace'
    
    def on_enter_view_set(self, e):
        options_1['background'] = 'lightgray'

    def on_leave_view_set(self, e):
        options_1['background'] = 'SystemButtonFace'


    # Theme_mode:hover
    def on_enter_view_mode(self, e):
        options_2['background'] = 'lightgray'

    def on_leave_view_mode(self, e):
        options_2['background'] = 'SystemButtonFace'
    
    
    def view_set_column(self, tabView):
         # Right box
        global view_set
        view_set = tk.LabelFrame(tabView, bg='white')
        view_set.place(width=438, height=574, relx=0.37, rely=0.001)
        
        time.sleep(0.1)

        # Right box:set column - header
        column_header = tk.LabelFrame(view_set, bg='gray', borderwidth=0)
        column_header.place(width=415, height=40, relx=0.02, rely=0.01)

        # Right box:set column - header:column_a
        column_header_a = tk.Label(column_header, bg='lightgray', text='Column Name')
        column_header_a.place(width=207, height=40)

        # Right box:set column - header:column_a
        column_header_b = tk.Label(column_header, bg='lightgray', text='Column Position')
        column_header_b.place(width=206, height=40, relx=0.505)

        opt_list = ['1', '2', '3', '4']

        # Right box:set column - column_a
        column_a = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_a.place(width=415, height=30, relx=0.02, rely=0.1)

        # Right box:set column - column_a:name
        column_a_name = tk.Label(column_a, bg='white', text='Date')
        column_a_name.place(width=207, height=30)

        # Right box:set column - column_a:position
        global column_a_position
        column_a_position = ttk.Combobox(column_a, values= opt_list)
        column_a_position.set(opt_list[0])
        column_a_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_b
        column_b = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_b.place(width=415, height=30, relx=0.02, rely=0.17)

        # Right box:set column - column_b:name
        column_b_name = tk.Label(column_b, bg='white', text='Time')
        column_b_name.place(width=207, height=30)

        # Right box:set column - column_a:position
        global column_b_position
        column_b_position = ttk.Combobox(column_b, values= opt_list)
        column_b_position.set(opt_list[1])
        column_b_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_c
        column_c = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_c.place(width=415, height=30, relx=0.02, rely=0.24)

        # Right box:set column - column_c:name
        column_c_name = tk.Label(column_c, bg='white', text='Activity')
        column_c_name.place(width=207, height=30)

        # Right box:set column - column_c:position
        global column_c_position
        column_c_position = ttk.Combobox(column_c, values= opt_list)
        column_c_position.set(opt_list[2])
        column_c_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_d
        column_d = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_d.place(width=415, height=30, relx=0.02, rely=0.31)

        # Right box:set column - column_d:name
        column_d_name = tk.Label(column_d, bg='white', text='Path File')
        column_d_name.place(width=207, height=30)

        # Right box:set column - column_d:position
        global column_d_position
        column_d_position = ttk.Combobox(column_d, values= opt_list)
        column_d_position.set(opt_list[3])
        column_d_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - apply button
        apply_button = tk.Button(view_set, text='Apply', command=lambda:self.apply_set())
        apply_button.place(width=70, height=30, relx=0.42, rely=0.5)


    def date_rad(self, rad):
        print(rad)

        global fmt_date_new
        fmt_date_new = rad


    def apply_date(self):
        global fmt_date
        
        if fmt_date_new != fmt_date:
            fmt_date = fmt_date_new
            print(fmt_date)

            apply_fmt = messagebox.showinfo("Success Message", "Date Format has been changed\nTo see the changes, go to menu Log > then click Show button")


    def view_date_format(self, tabView):
        date_canvas = tk.LabelFrame(tabView, bg='white')
        date_canvas.place(width=438, height=574, relx=0.37, rely=0.001)

        date_header = tk.LabelFrame(date_canvas, borderwidth=0)
        date_header.place(width=415, height=40, relx=0.02, rely=0.01)

        date_header_text = tk.Label(date_header, text="Choose 1 of 3 Option Below", bg='lightgray')
        date_header_text.place(width=415, height=40)

        rad = tk.IntVar()
        rad.set("4")

        date_opt_1 = tk.Radiobutton(date_canvas, text="yyyy-mm-dd (Ex: 2020-08-15)",
                                        variable=rad, value=1, bg="white", command=lambda:self.date_rad(rad.get()))
        date_opt_1.place(width=415, height=40, relx=0.02, rely=0.1)
      
        date_opt_2 = tk.Radiobutton(date_canvas, text="dd/mm/yyyy (Ex: 15/08/2020)",
                                        variable=rad, value=2, bg="white", command=lambda:self.date_rad(rad.get()))
        date_opt_2.place(width=415, height=40, relx=0.02, rely=0.19)

        date_opt_3 = tk.Radiobutton(date_canvas, text="dd-bb-yyyy  (Ex: 15-Aug-2020)",
                                        variable=rad, value=3, bg="white", command=lambda:self.date_rad(rad.get()))
        date_opt_3.place(width=415, height=40, relx=0.03, rely=0.28)


        date_apply = tk.Button(date_canvas, text="Apply", command=lambda:self.apply_date())
        date_apply.place(width=70, height=30, relx=0.42, rely=0.45)



    def ask_check(self, title_input, desc_input, window_ask):

        getTitle = title_input.get()
        getDesc = desc_input.get("1.0", "end-1c")

        # print("{} {}".format(getTitle, getDesc))

        if getTitle == '' or getDesc == '':
            err_msg = messagebox.showerror('Error Message', 'Title and Description must be filled')
        
        else:
            succ_msg = messagebox.showinfo('Succes Message', 'Your QnA/Feedback has been sent')
            window_ask.destroy()


    def ask(self):
        window_ask = tk.Toplevel()
        window_ask.title('Help')
        window_ask.geometry('500x400')
        window_ask.config(bg='white')
        window_ask.pack_propagate(False)
        window_ask.resizable(0, 0)

        title_ask = tk.LabelFrame(window_ask, text="Title:")
        title_ask.place(height=50, width=400, relx=0.1, rely=0.05)
    
        title_input = tk.Entry(title_ask, bg="white")
        title_input.place(height=25, width=385, relx=0.01)

        desc_ask = tk.LabelFrame(window_ask, text="Description:")
        desc_ask.place(height=200, width=400, relx=0.1, rely=0.2)
    
        desc_input = tk.scrolledtext.ScrolledText(desc_ask, bg="white", wrap=tk.WORD)
        desc_input.place(height=175, width=385, relx=0.01)

        desc_input.focus()

        send_button = tk.Button(window_ask, text="Send", command=lambda:self.ask_check(title_input, desc_input, window_ask))
        send_button.place(height=30, width=80, relx=0.42, rely=0.75)


    def about(self):
        window_ask = tk.Toplevel()
        window_ask.title('Help')
        window_ask.geometry('500x400')
        # window_ask.config(bg='white')
        window_ask.pack_propagate(False)
        window_ask.resizable(0, 0)

        canvas_about = tk.Label(window_ask, bg="white")
        canvas_about.place(width=480, height=380, relx=0.02, rely=0.02)

        header_font = tk.font.Font(size=15, weight="bold")
        header_about = tk.Label(canvas_about, text="Activity Logging", font=header_font, bg="white")
        header_about.place(width=200, height=50)

        line_font = tk.font.Font(size=15)
        line_about = tk.Label(canvas_about, text="_________________________________________", font=line_font, bg="white")
        line_about.place(width=438, height=25, rely=0.1, relx=0.04)


        desc_about = tk.Text(canvas_about, font=("Helvetiva", 10), bg="white", selectborderwidth=0)
        desc_about.place(width=438, height=200, rely=0.2, relx=0.04)

        desc_text="""Activity Logging is a tool for Windows operating system that collects 
information from various sources on a running system, and displays 
a log of actions made by the user and events occurred on this computer. 
The activity displayed by Activity Logging includes: 
Creating File or Folder, Opening File or Folder, Modifying File or Folder,
Deleting File or Folder and Checking Malicious File or Folder"""

        desc_about.insert(tk.END, desc_text)


    def manual(self):
        window_ask = tk.Toplevel()
        window_ask.title('Manual')
        window_ask.geometry('800x600')
        # window_ask.config(bg='white')
        window_ask.pack_propagate(False)
        window_ask.resizable(0, 0)

        canvas_about = tk.Label(window_ask, bg="white")
        canvas_about.place(width=770, height=580, relx=0, rely=0.02)

        header_font = tk.font.Font(size=15, weight="bold")
        header_about = tk.Label(canvas_about, text="Manual", font=header_font, bg="white")
        header_about.place(width=200, height=50)

        # line_font = tk.font.Font(size=15)
        # line_about = tk.Label(canvas_about, text="_________________________________________", font=line_font, bg="white")
        # line_about.place(width=438, height=25, rely=0.1, relx=0.04)


        desc_about = tk.Text(canvas_about, font=("Helvetiva", 10), bg="white", selectborderwidth=0)
        desc_about.place(width=700, height=400, rely=0.09, relx=0.04)

        desc_text="""I. REQUIREMENT
    - Python 3 Installed
    - Downloaded a ClamAV database
    - Windows Defender / anti virus disabled
    - Downloaded all the dependencies
        
II. SETUP
    1. run setup.py to install all the dependencies
    2. disable windows defender / other anti virus
    3. download ClamAv database from http://database.clamav.net/main.cvd
    4. aplikasi sudah siap digunakan
    
III. APP
    - Menjalankan fungsi logging
        1.  pertama buka file "ActivityLoggingControlPanel.pyw" untuk masuk kedalam menu GUI
        2.  pilih alamat directory yang ingin di log
        3.  jika ingin menjalankan tool secara otomatis setiap menghidupkan komputer maka
            checklist kotak auto run
        4.  tekan run
        5.  aplikasi berhasil dijalankan
        
    - Melihat log yang sudah terekam
        1. pertama buka file "ActivityLoggingControlPanel.pyw" untuk masuk kedalam menu GUI
        2. pilih tab log dibagian atas GUI
        3. masukkan alamat file log yang ingin dibaca
        4. tekan tanda show
        5. log akan keluar di GUI
        
    - Mengubah urutan kolom view log
        1. pertama buka file "ActivityLoggingControlPanel.pyw" untuk masuk kedalam menu GUI
        2. pilih tab view dibagian atas GUI
        3. pilih Set Column
        4. set urutan kolom sesuai keinginan
        5. tekan apply
    
    - Mengubah format tanggal pada kolom Date
        1. pertama buka file "ActivityLoggingControlPanel.pyw" untuk masuk kedalam menu GUI
        2. pilih tab view dibagian atas GUI
        3. pilih Date Format
        3. pilih format tanggal sesuai keinginan
        4. tekan apply
        
    """

        desc_about.insert(tk.END, desc_text)


    def modules(self):
        try:
            print("[*] Checking pip update")
            os.system('cmd /c "python -m pip install --upgrade pip"')

            print('[*] Checking win10toast')
            os.system('cmd /c "python -m pip install win10toast"')

            print('\n[*] Checking psutil')
            os.system('cmd /c "python -m pip install psutil"')

            print('\n[*] Checking win32.client')
            os.system('cmd /c "python -m pip install pywin32"')

            print('\n[*] Checking watchdog')
            os.system('cmd /c "python -m pip install watchdog"')

            print('\n[*] Checking pyClamd')
            os.system('cmd /c "python -m pip install pyClamd"')

        except IndentationError:
            print('All Clear')

    #####


    def __init__(self):
        self.modules()

        counter1 = 0

        window = tk.Tk()
        s = ttk.Style()
        #supaya cuma read config sekali
        if(counter1 == 0):
            self.checkRUN()
            self.dir = ""
            self.Check1 = 0
            self.checkConfig()
            counter1 = 1
            print(f"this is directory : {self.dir}\nthis is checkbox : {self.Check1}")
        else:
            pass

        window.title("Activity Logging")
        window.geometry('700x600')
        window.pack_propagate(False)
        window.resizable(width=False, height=False)

        tab_control = ttk.Notebook(window)

        tabConfig = ttk.Frame(tab_control)
        tabLog = ttk.Frame(tab_control)
        tabView = ttk.Frame(tab_control)
        tabHelp = ttk.Frame(tab_control)

        #untuk assign frame config
        tab_control.add(tabConfig, text="Config")
        #untuk assign frame show log
        tab_control.add(tabLog, text="Log")
        #untuk assign frame view
        tab_control.add(tabView, text="View")
        #untuk assign frame help
        tab_control.add(tabHelp, text="Help")

        tab_control.pack(expand=3, fill='both')

        #frame space untuk config
        framespace = tk.Frame(tabConfig, height=20)
        framespace.pack(side="top", padx =20)

        #frame utama config
        frame1 = tk.Frame(tabConfig, bg="#FFFFFF")
        frame1.pack(padx=5, pady=10)

        #text select directory
        label1 = tk.Label(frame1, text="Select Directory", anchor="w", width = 50, bg="#FFFFFF")
        label1.grid(column=1, row=1, padx =(15,15))

        #entry directory
        self.entry1 = tk.Entry(frame1, width = 50)
        self.entry1.insert(0, self.dir)
        self.entry1.config(state='disabled')
        self.entry1.grid(column=1, row=2, padx = (10,5))

        #checkbox autorun
        self.checkbox1 = ttk.Checkbutton(frame1, text = "auto run")
        self.checkbox1.state(['!alternate'])
        if(int(self.Check1) == 1):
            # print(self.Check1 + "Autorun")
            self.checkbox1.state(['selected'])
        elif(int(self.Check1) == 0):
            # print(self.Check1 + "Autorun")
            self.checkbox1.state(['!selected'])
        self.checkbox1.grid(column = 1, row=3, sticky="w", padx = (10,10), pady = (10,10))


        self.LabelStatus = tk.Label(tabConfig, text="No script is running ..", width = 50, bg="#FFFFFF", fg = "#6F6F6F")
        self.LabelStatus.pack(pady = 6)

        framebaru = tk.Frame(tabConfig)
        framebaru.pack()
        #run button
        buttonterminate = tk.Button(framebaru , text= "run", width = 10, command = lambda : self.run())
        buttonterminate.pack(side= "left", padx = 6)

        #stop button
        buttonterminate = tk.Button(framebaru , text= "stop", width = 10, command = lambda : self.checkRUN())
        buttonterminate.pack(side= "left", padx = 6)

        #select directory button
        button1 = tk.Button(frame1, width = 3, text ="...", command = lambda : self.directory())
        button1.grid(column=2, row=2, padx = (0,5), pady = (10,10))


        # Choose or Type and Open File
        open_file = tk.LabelFrame(tabLog, bg="white")
        open_file.place(height=80, width=699, rely=0.115, relx=0.5, anchor='center')

        label_open = tk.LabelFrame(open_file, text="Choose Log File (*.csv)")
        label_open.place(height=55, width=452, rely=0.45, relx=0.5, anchor='center')

        self.entry_path = tk.Entry(label_open, width=50)
        self.entry_path.place(height=25, width= 330, rely=0.1, relx=0.03)

        button_path = tk.Button(label_open, text=". . .", command = lambda: [self.file_opener()])
        button_path.place(width=30 , rely=0.1, relx=0.78)

        button_show = tk.Button(label_open, text="Show", command=lambda:self.show_log(filenames, composition, tabLog))
        button_show.place(width=50 , rely=0.1, relx=0.86)


        log_canvas = tk.LabelFrame(tabLog, bg='white')
        log_canvas.place(height=490, width=699, rely=0.59, relx=0.5, anchor='center')


        # Left box
        view_options = tk.LabelFrame(tabView, bg='white')
        view_options.place(width=250, height=574, relx=0.001, rely=0.001) 

        global options_1
        options_1 = tk.Button(view_options, text="Set Column", command=lambda:self.view_set_column(tabView))
        options_1.bind("<Enter>", self.on_enter_view_set)
        options_1.bind("<Leave>", self.on_leave_view_set)
        options_1.place(width=237, height=40, relx=0.015, rely=0.01)

        global options_2
        options_2 = tk.Button(view_options, text="Date Format", command=lambda:self.view_date_format(tabView))
        options_2.bind("<Enter>", self.on_enter_view_mode)
        options_2.bind("<Leave>", self.on_leave_view_mode)
        options_2.place(width=237, height=40, relx=0.015, rely=0.1)

        # Right box
        global view_set
        view_set = tk.LabelFrame(tabView, bg='white')
        view_set.place(width=438, height=574, relx=0.37, rely=0.001)
        
        time.sleep(0.1)

        # Right box:set column - header
        column_header = tk.LabelFrame(view_set, bg='gray', borderwidth=0)
        column_header.place(width=415, height=40, relx=0.02, rely=0.01)

        # Right box:set column - header:column_a
        column_header_a = tk.Label(column_header, bg='lightgray', text='Column Name')
        column_header_a.place(width=207, height=40)

        # Right box:set column - header:column_a
        column_header_b = tk.Label(column_header, bg='lightgray', text='Column Position')
        column_header_b.place(width=206, height=40, relx=0.505)

        opt_list = ['1', '2', '3', '4']

        # Right box:set column - column_a
        column_a = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_a.place(width=415, height=30, relx=0.02, rely=0.1)

        # Right box:set column - column_a:name
        column_a_name = tk.Label(column_a, bg='white', text='Date')
        column_a_name.place(width=207, height=30)

        # Right box:set column - column_a:position
        global column_a_position
        column_a_position = ttk.Combobox(column_a, values= opt_list)
        column_a_position.set(opt_list[0])
        column_a_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_b
        column_b = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_b.place(width=415, height=30, relx=0.02, rely=0.17)

        # Right box:set column - column_b:name
        column_b_name = tk.Label(column_b, bg='white', text='Time')
        column_b_name.place(width=207, height=30)

        # Right box:set column - column_a:position
        global column_b_position
        column_b_position = ttk.Combobox(column_b, values= opt_list)
        column_b_position.set(opt_list[1])
        column_b_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_c
        column_c = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_c.place(width=415, height=30, relx=0.02, rely=0.24)

        # Right box:set column - column_c:name
        column_c_name = tk.Label(column_c, bg='white', text='Activity')
        column_c_name.place(width=207, height=30)

        # Right box:set column - column_c:position
        global column_c_position
        column_c_position = ttk.Combobox(column_c, values= opt_list)
        column_c_position.set(opt_list[2])
        column_c_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - column_d
        column_d = tk.LabelFrame(view_set, bg='white', borderwidth=0)
        column_d.place(width=415, height=30, relx=0.02, rely=0.31)

        # Right box:set column - column_d:name
        column_d_name = tk.Label(column_d, bg='white', text='Path File')
        column_d_name.place(width=207, height=30)

        # Right box:set column - column_d:position
        global column_d_position
        column_d_position = ttk.Combobox(column_d, values= opt_list)
        column_d_position.set(opt_list[3])
        column_d_position.place(width=45, height=30, relx=0.7)


        # Right box:set column - apply button
        apply_button = tk.Button(view_set, text='Apply', command=lambda:self.apply_set())
        apply_button.place(width=70, height=30, relx=0.42, rely=0.5)


        # Help Part
        help_canvas = tk.LabelFrame(tabHelp, bg="white")
        help_canvas.place(height=575.5, width=697.5)

        help_box = tk.Label(help_canvas, bg="lightgray")
        help_box.place(height=400, width=450, relx=0.51, rely=0.45, anchor="center")

        help_title = tk.Label(help_box, text="Help", font="30", bg="lightgray")
        help_title.place(height=20, width=50,relx= 0.5, rely=0.05, anchor="center")
    
        manual_button = tk.Button(help_box, text="Manual", command=lambda:self.manual())
        manual_button.place(height=30, width=300,relx= 0.5, rely=0.2, anchor="center")
        
        manual_button = tk.Button(help_box, text="QnA/Feedback", command=lambda:self.ask())
        manual_button.place(height=30, width=300,relx= 0.5, rely=0.4, anchor="center")
        
        manual_button = tk.Button(help_box, text="About", command=lambda:self.about())
        manual_button.place(height=30, width=300,relx= 0.5, rely=0.6, anchor="center")

        window.mainloop()


if __name__ == "__main__":
    f = window()