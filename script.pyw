import time 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler 
import csv
from datetime import datetime
import os
import psutil
from threading import Thread
import pyclamd
import sys
from win10toast import ToastNotifier
import time
import subprocess


global logFile, script, absolutepath
filename = sys.argv[0]
absolutepath = os.path.abspath(filename)
logFile = os.path.abspath('LogFile.csv') 
script = absolutepath


class OnMyWatch(): 
    # Set the directory on watch 
    # watchDirectory = input('Input short path:')
  
    def __init__(self): 
        self.observer = Observer() 

    def run(self, path): 
        event_handler = Handler() 
        self.path = path
        self.observer.schedule(event_handler, self.path, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(5) 
        except: 
            self.observer.stop() 
            print("[*]Logging has stopped\n") 
  
        self.observer.join()

    def showlog(self):
        count = 0
        print('\n[*]Press CTRL + C to Stop Logging')
        print('[*]Logging has started...')
                
        with open(os.path.abspath('LogFile.csv')) as csv_file:
            print("DATE\t\t TIME\t\t\t   EVENT\t ADDRESS")
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                count = count + 1
                print(row[0],'|',row[1],'|',row[2],'|', row[3])
            # print('\n')

        if count == 0:
            print("\t\tErr!!(NoLogFiles)\n")
  
  
class Handler(FileSystemEventHandler): 
  
    @staticmethod
    def on_any_event(event):

        if event.is_directory: 
            return None
  
        elif event.event_type == 'created' and event.src_path != logFile and event.src_path != script: 
            # Event is created, you can process it now
            csv.writer(open(logFile, mode='a+', newline=''), delimiter=',').writerow([datetime.date(datetime.now()), datetime.time(datetime.now()), event.event_type, event.src_path]) 
            print("Watchdog received created event - % s." % event.src_path)
            scanMalicious(event.src_path)

        elif event.event_type == 'modified' and event.src_path != logFile and event.src_path != script: 
            # Event is modified, you can process it now
            csv.writer(open(logFile, mode='a+', newline=''), delimiter=',').writerow([datetime.date(datetime.now()), datetime.time(datetime.now()),event.event_type, event.src_path]) 
            print("Watchdog received modified event - % s." % event.src_path) 
        
        elif event.event_type == 'moved' and event.src_path != logFile and event.src_path != script:
            # Event is received, you can process it now
            csv.writer(open(logFile, mode='a+', newline=''), delimiter=',').writerow([datetime.date(datetime.now()), datetime.time(datetime.now()),event.event_type, event.src_path])
            print("Watchdog received moved event - %s." % event.src_path)
        
        elif event.event_type == 'deleted' and event.src_path != logFile and event.src_path != script:
            # Event is deleted, you can process it now 
            csv.writer(open(logFile, mode='a+', newline=''), delimiter=',').writerow([datetime.date(datetime.now()), datetime.time(datetime.now()),event.event_type, event.src_path]) 
            print("Watchdog received deleted event - %s." % event.src_path)

def scanMalicious(path):
    # path = path.replace(".", "")
    path = path.replace("/", "\\")
    # print (path)
    eventName = ""
    try:
        cd = pyclamd.ClamdAgnostic()
        lwl = cd.ping()
        hasil = cd.scan_file(path)
        print(hasil)
    except:
        pass

    try:
        if hasil[path]:
            values = hasil.get(path)
            # print(hasil)
            eventName = values[0] + " MALICIOUS \"" + values[1] + "\""
            print(eventName)
            csv.writer(open(logFile, mode='a+', newline=''), delimiter=',').writerow([datetime.date(datetime.now()), datetime.time(datetime.now()), eventName, path])
        else:
            pass
    except:
        pass
    
    try:
        toast = ToastNotifier()
        toast.show_toast("WARNING!!!",eventName ,duration=20,icon_path=absolutepath.replace("script.pyw", "") + "Devil_1.ico")
        # print("test")
    except:
        pass

def checkpoint():
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

    f = open("running.txt","w")
    pid = str(os.getpid())
    f.write(pid)
    f.close()

def runClamd():
    path =  '"'+ os.path.abspath("ClamAv") + "\clamd" + '"'
    command = "Start-Process " + path + " -WindowStyle Hidden"
    print(command)

    try:
        p = subprocess.Popen(["powershell.exe", 
                    command], 
                    stdout=sys.stdout)

        p.communicate()
    except:
        pass

def main():
        checkpoint()

        paths = ''

        fr = open("config.txt", "r")
        path = fr.readline()
        fr.readline()
        exeConfig = fr.readline()

        print(exeConfig)

        length = len(path)

        index = 1
        for i in range(length):
            if index == length:
                break
            else:
                paths += path[i]
                index += 1

        if os.path.isfile(logFile) == False:
            csv.writer(open(logFile, mode='w', newline=''), delimiter=',')


        try:
            watch = OnMyWatch()
            watch.run(paths)
            runClamd()
            time.wait(15) #untuk menunggu loading clamd

        except FileNotFoundError:
            print('There\'s no such directory')
        except ValueError:
            print('Input the right PATH')
        except OSError:
            print('Input the right PATH')       


if __name__ == '__main__':
    # test = input("HELLO : ")
    main()
    # exit1 = input("Press enter to exit...." )

