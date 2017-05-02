#!/usr/bin/python3

import socket
import time
import threading
from tkinter import *

class Client:
    
    def __init__(self):
        self.server = None
        self.running = False
        
    # Hacky helper function
    def get_network_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        
        return ip

    # Client controls
    def run(self, app):
        self.app = app

        host = self.get_network_ip()
        port = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(0)

        thread = threading.Thread(target=self.receive, args=("RecvThread", self.sock))
        thread.start()

    def start(self, app, server_ip):
        self.server = (server_ip, 5000)
        self.running = True
        
    def stop(self):
        self.server = None
        self.running = False
        
    # Do the network/socket stuff
    def send(self, alias, msg):
        if self.server != None:
            if msg != '':
                data = (alias + ":" + msg).encode()
                self.sock.sendto(data, self.server)
    
    def receive(self, name, sock):
        tLock = threading.Lock()

        while True:
            if self.running:
                try:
                    tLock.acquire()
                    while True:
                        data, addr = self.sock.recvfrom(1024)
                        app.update_chat(str(data))
                except:
                    pass
                finally:
                    tLock.release()

            time.sleep(0.5)
    
class App:
    
    def __init__(self, master, client):
        master.title("PyChat Client")
        self.client = client
        
        connection = Frame(master)
        connection.pack()

        chat_frame = Frame(master)
        chat_frame.pack()

        text_entry = Frame(master)
        text_entry.pack()

        # Join section
        self.alias = Text(connection, height=1, width=10)
        self.alias.pack(side=LEFT, fill=Y)

        ip_address = ""
        self.connection_text_widget = Text(connection, height=1, width=15)
        self.connection_text_widget.pack(side=LEFT, fill=Y)
        self.connection_text_widget.insert(END, ip_address)

        self.join_btn = Button(connection, 
                               text="Join",
                               command=self.join_chat)
        self.join_btn.pack(side=LEFT)

        self.join_btn = Button(connection, 
                               text="Leave",
                               command=self.leave_chat)
        self.join_btn.pack(side=LEFT)

        
        # Chat area
        chat_log = "Begin chat...\n"
        
        self.chat_text = Text(chat_frame, height=20, width=50)
        self.chat_scroll = Scrollbar(chat_frame)
        
        self.chat_text.pack(side=LEFT, fill=Y)
        self.chat_scroll.pack(side=RIGHT, fill=Y)
        
        self.chat_text.config(yscrollcommand=self.chat_scroll.set)
        self.chat_scroll.config(command=self.chat_text.yview)
        
        self.chat_text.insert(END, chat_log)


        # Message entry area
        default_text = ""

        self.msg_text = Text(text_entry, height=4, width=50)
        self.msg_scroll = Scrollbar(text_entry)
        
        self.msg_text.pack(side=LEFT, fill=Y)
        self.msg_scroll.pack(side=RIGHT, fill=Y)
        
        self.msg_text.config(yscrollcommand=self.msg_scroll.set)
        self.msg_scroll.config(command=self.msg_text.yview)
        
        #self.msg_text.insert(END, default_text)

        self.send_btn = Button(text_entry,
                               fg="green",
                               text="Send",
                               command=self.send_message)
        self.send_btn.pack(side=LEFT)
    
    def join_chat(self):        
        ip_address = self.connection_text_widget.get("1.0",END)
        self.chat_text.insert(END, "You've joined {}\n".format(ip_address))

        self.client.start(self, ip_address)

    def leave_chat(self):        
        self.chat_text.insert(END, "You've left the chat.\n")
        self.client.stop()

    def send_message(self):
        alias = self.alias.get("1.0", END).strip()
        msg = self.msg_text.get("1.0", END).strip()

        if len(msg) > 0:
            self.client.send(alias, msg)
            self.msg_text.delete("1.0", END)

    def update_chat(self, data):        
        colon_pos = data.index(':')
        alias = data[2: colon_pos]
        msg = data[colon_pos + 1: -1]
        output = alias + ": " + msg
        
        self.chat_text.insert(END, output + "\n")
        self.chat_text.see(END)
        


if __name__ == "__main__":    
    root = Tk()
    client = Client()
    app = App(root, client)
    root.after(500, client.run(app))
    root.mainloop()
