#!/usr/bin/python3

import socket
#import time
import threading
from tkinter import *

# Hacky helper function
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

# Do the network/socket stuff
def process_messages():
    '''
    print('processing messages')
    while True:
        if running:
            print("running")
            time.sleep(1)
    '''
    host = get_local_ip()
    port = 5000

    clients = []

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(0)

    while True:
        if running:
            try:
                data, addr = s.recvfrom(1024)

                if addr not in clients:
                    clients.append(addr)
                    
                print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
                for client in clients:
                    s.sendto(data, client)
            except:
                pass

# A nifty GUI
class App:
    
    def __init__(self, master):
        self.master = master
        
        # Network stuff
        self.host_ip = get_local_ip()
        self.port = 5000

        # Server status
        self.running = False

        # Window layout
        master.title("PyChat Server")
        master.minsize(width=250, height=150)
        master.maxsize(width=250, height=150)
        
        connection = Frame(master)
        connection.pack()

        controls = Frame(master)
        controls.pack()

        # Connection frame
        self.state = StringVar()
        self.state.set("Press start")
        status = Message(connection, textvariable = self.state)
        status.config(width=250)
        status.pack(side=TOP)

        ip = Message(connection, text = self.host_ip)
        ip.config(width=250, font=('times', 18, 'bold'))
        ip.pack(side=TOP)

        # Controls frame     
        self.start_btn = Button(controls,
                               fg="green",
                               text="Start",
                               command=self.start)
        self.start_btn.pack(side=LEFT)
        
        self.stop_btn = Button(controls,
                               fg="red",
                               text="Stop",
                               command=self.stop)
        self.stop_btn.pack(side=RIGHT)

        
    def start(self):
        global running
        
        running = True
        app.state.set("Server is running at")
        
    def stop(self):
        global running
        
        running = False
        app.state.set("Server is stopped at")


if __name__ == "__main__":
    running = False
    thread = threading.Thread(target=process_messages)
    thread.start()

    root = Tk()
    app = App(root)
    root.mainloop()

    thread.join()


# http://stackoverflow.com/questions/26703502/threads-and-tkinter-python-3

