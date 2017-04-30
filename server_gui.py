#!/usr/bin/python3

import socket
import time
from tkinter import *



class App:
    
    def __init__(self, master):
        master.title("PyChat Server")
        master.minsize(width=250, height=150)
        master.maxsize(width=250, height=150)
        
        connection = Frame(master)
        connection.pack()

        controls = Frame(master)
        controls.pack()

        # Connection
        self.host_ip = self.get_local_ip()
        self.port = 5000
        
        msg = Message(connection, text = self.host_ip)
        msg.config(width=250, bg='lightgreen', font=('times', 18, 'bold'))
        msg.pack(side=TOP)

        # Controls        
        self.start_btn = Button(controls,
                               fg="green",
                               text="Start",
                               command=self.start)
        self.start_btn.pack(side=LEFT)
        
        self.stop_btn = Button(controls,
                               fg="red",
                               text="Stop",
                               command=self.stop)
        self.stop_btn.pack(side=LEFT)

        self.running = False
        
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        
        return ip

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host_ip, self.port))
        self.s.setblocking(0)

        self.clients = []
        
        self.running = True
        print("Server started on " + self.host_ip)

    def stop(self):
        print("stop")
        self.running = False

    def run(self):
        print("processing messages started")

        while self.running:
            print("running")
            try:
                data, addr = self.s.recvfrom(1024)
                if "Quit" in str(data):
                    self.quitting = True
                if addr not in self.clients:
                    clients.append(addr)
                    
                print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
                for client in self.clients:
                    self.s.sendto(data, client)
            except:
                pass
        else:
            print("not running")

        #time.sleep(1000)
        
root = Tk()
app = App(root)
root.after(1000, app.run)
root.mainloop()
#app.run()


