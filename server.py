#!/usr/bin/python3

import socket
import time
import threading
from tkinter import *

class Server:
    
    def __init__(self):
        self.running = False
        
    def get_network_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        
        return ip

    def run(self, app):
        #self.app = app

        host = self.get_network_ip()
        port = 5000

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(0)

        thread = threading.Thread(target=self.process_messages)
        thread.start()

    def start(self):
        self.running = True
        
    def stop(self):
        self.running = False
        
    def process_messages(self):
        clients = []

        while True:
            if self.running:
                try:
                    data, addr = self.sock.recvfrom(1024)

                    if addr not in clients:
                        clients.append(addr)
                        
                    print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
                    for client in clients:
                        self.sock.sendto(data, client)
                except:
                    pass
                
            time.sleep(0.5)
            
class App(Frame):
    
    def __init__(self, parent, server):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.server = server
        self.config()
        self.initUI()

    def config(self):
        self.host_ip = server.get_network_ip()
        self.port = 5000
        
        self.state = StringVar()
        self.state.set("Press start")
        
    def initUI(self):
        self.parent.title("PyChat Server")
        self.pack(fill=BOTH)
        
        frame1 = Frame(self)
        frame1.pack(fill=BOTH)
        
        status = Message(frame1, textvariable = self.state,
                                 width=150)
        status.pack(fill=X, padx=5, pady=5)
        
        frame2 = Frame(self)
        frame2.pack(fill=BOTH)

        ip = Message(frame2, text = self.host_ip)
        ip.config(width=250, font=('courier', 22, 'bold'))
        ip.pack(fill=X, padx=5, pady=5)

        frame3 = Frame(self)
        frame3.pack()

        start = Button(frame3, font=('Helvetica', 16, 'bold'),
                               fg="green",
                               text="Start",
                               command=self.start)
        start.pack(side=LEFT, padx=5, pady=5)
        
        stop = Button(frame3, font=('Helvetica', 16, 'bold'),
                              fg="red",
                              text="Stop",
                              command=self.stop)
        stop.pack(side=RIGHT, padx=5, pady=5)

    def start(self):        
        self.server.start()
        self.state.set("Server is running at")
        
    def stop(self):        
        self.server.stop()
        self.state.set("Server is stopped at")


if __name__ == "__main__":
    root = Tk()
    server = Server()
    app = App(root, server)
    root.after(500, server.run(app))
    root.mainloop()
