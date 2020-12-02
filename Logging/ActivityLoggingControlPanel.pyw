import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from subprocess import check_output
from subprocess import Popen
import os
import psutil
import sys
import csv
import getpass
from win32com.client import Dispatch
import logging

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

        # end program
        sys.exit()

    def autoRun(self, curr):
        username = getpass.getuser()
        path = r"C:\Users" + "\\" + username + r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        path = os.path.join(path, "Logging.lnk")
        if(curr == 1):
            # putSHORTCUT HERE
            target = r"D:\Documents\PITON\Logging\script.pyw"
            wDir = r"D:\Documents\PITON\Logging"
            icon = r"D:\Documents\PITON\Logging\script.pyw"
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

        inputs = filedialog.askopenfilename(initialdir="/",
                                            title="Select a CSV File",
                                            filetypes=(("*.csv", "*.csv"), ("All Files", "*.*"))
                                            )

        filenames = inputs
        pathfile = tk.Label(self.entry_path, text=filenames, bg='white')
        pathfile.place(rely=0.1, relx=0.01)


    def show_log(self, name):

        with open(name) as f:
            reader = csv.reader(f, delimiter=',')
        
            number = 0
            
            for row in reader:
                number += 1
                dates = row[0]
                times = row[1]
                events = row[2]
                pathFile = row[3]
                ttk.tree.insert("", 1, values=(number, dates, times, events, pathFile))



    def on_enter(self, e):
        menuShow_log['background'] = 'gray'

    def on_leave(self, e):
        menuShow_log['background'] = 'SystemButtonFace'
    #####


    def __init__(self):
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

        #untuk assign frame config
        tab_control.add(tabConfig, text="config")

        #untuk assign frame show log
        tab_control.add(tabLog, text="log")

        tab_control.pack(expand=1, fill='both')

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
            print(self.Check1 + "Autorun")
            self.checkbox1.state(['selected'])
        elif(int(self.Check1) == 0):
            print(self.Check1 + "Autorun")
            self.checkbox1.state(['!selected'])
        self.checkbox1.grid(column = 1, row=3, sticky="w", padx = (10,10), pady = (10,10))

        #run button
        buttonterminate = tk.Button(tabConfig , text= "run", width = 10, command = lambda : self.run())
        buttonterminate.pack()

        #select directory button
        button1 = tk.Button(frame1, width = 3, text ="...", command = lambda : self.directory())
        button1.grid(column=2, row=2, padx = (0,5), pady = (10,10))

        # #ShowLog
        # menuShow_log = ttk.Label(window, text="Show Log", padx=5, pady=4)
        # menuShow_log.bind("<Enter>", on_enter)
        # menuShow_log.bind("<Leave>", on_leave)

        # menuShow_log.grid(row=1, column=0)

        # Choose or Type and Open File
        open_file = tk.LabelFrame(tabLog, bg="white")
        open_file.place(height=80, width=699, rely=0.115, relx=0.5, anchor='center')

        label_open = tk.LabelFrame(open_file, text="Choose Log File (*.csv)")
        label_open.place(height=55, width=452, rely=0.45, relx=0.5, anchor='center')

        self.entry_path = tk.Entry(label_open, width=50)
        self.entry_path.place(height=25, width= 330, rely=0.1, relx=0.03)

        button_path = tk.Button(label_open, text=". . .", command = lambda: [self.file_opener()])
        button_path.place(width=30 , rely=0.1, relx=0.78)

        button_show = tk.Button(label_open, text="Show", command=lambda:show_log(self.filenames))
        button_show.place(width=50 , rely=0.1, relx=0.86)


        # Log Data
        log_file = tk.LabelFrame(tabLog)
        log_file.place(height=490, width=699, rely=0.59, relx=0.5, anchor='center')

        scrollbarx = tk.Scrollbar(log_file, orient="horizontal")
        scrollbary = tk.Scrollbar(log_file, orient="vertical")
        tree = ttk.Treeview(log_file, columns=("No", "Date", "Time", "Event", "Path File"), height=400, selectmode="extended", 
                            yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side="right", fill="y")
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side="bottom", fill="x")
        tree.heading('No', text="No.", anchor="e")
        tree.heading('Date', text="Date", anchor="nw")
        tree.heading('Time', text="Time", anchor="nw")
        tree.heading('Event', text="Event", anchor='center')
        tree.heading('Path File', text="Path File", anchor="nw")
        tree.column('#0', stretch="no", minwidth=0, width=0)
        tree.column('#1', stretch="no", minwidth=0, width=50, anchor="e")
        tree.column('#2', stretch="no", minwidth=0, width=100)
        tree.column('#3', stretch="no", minwidth=0, width=150)
        tree.column('#4', stretch="no", minwidth=0, width=100, anchor='center')
        tree.column('#5', stretch="no", minwidth=0, width=500)
        tree.pack()

        window.mainloop()

if __name__ == "__main__":
    f = window()