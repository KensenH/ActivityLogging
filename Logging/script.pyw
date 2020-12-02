import time 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler 
import csv
from datetime import datetime
import os
import psutil

global logFile, script

logFile = 'D:/LogFile.csv'
script = 'D:/Latihan Python/Tkinter/Logging/script.pyw'


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
                
        with open('D:\\LogFile.csv') as csv_file:
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


def main():
        checkpoint()

        paths = ''

        fr = open("config.txt", "r")
        path = fr.readline()
        length = len(path)

        index = 1
        for i in range(length):
            if index == length:
                break
            else:
                paths += path[i]
                index += 1

        if os.path.isfile("D:\LogFile.csv") == False:
            csv.writer(open("D:\LogFile.csv", mode='w', newline=''), delimiter=',')

        try:
            watch = OnMyWatch() 
            watch.run(paths)

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

