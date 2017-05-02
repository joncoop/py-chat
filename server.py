#!/usr/bin/python3

import socket
import time
import threading
from tkinter import *

class Server:
    
    def __init__(self):
        self.running = False
        
    # Hacky helper function
    def get_network_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        
        return ip

    # Server controls
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
        
    # Do the network/socket stuff
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
            
# A nifty GUI
class App:
    
    def __init__(self, master, server):
        self.master = master
        self.server = server
        
        # Network stuff
        self.host_ip = server.get_network_ip()
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
        status.pack(side=TOP, fill=X, padx=10, pady=10)

        ip = Message(connection, text = self.host_ip)
        ip.config(width=250, font=('courier', 22, 'bold'))
        ip.pack(side=TOP, fill=X, padx=10, pady=10)

        # Controls frame     
        start_btn = Button(controls,
                           font=('courier', 16, 'bold'),
                           fg="green",
                           text="Start",
                           command=self.start)
        start_btn.pack(side=LEFT, padx=10, pady=10)
        
        stop_btn = Button(controls,
                          font=('courier', 16, 'bold'),
                          fg="red",
                          text="Stop",
                          command=self.stop)
        stop_btn.pack(side=RIGHT, padx=10, pady=10)

        
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
