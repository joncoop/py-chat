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
                        app.update(data.decode())
                except:
                    pass
                finally:
                    tLock.release()

            time.sleep(0.5)
            
class App(Frame):
  
    def __init__(self, parent, client):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.client = client
        self.initUI()
        
    def initUI(self):
        self.parent.title("PyChat Client")
        self.pack(fill=BOTH)
        
        frame1 = Frame(self)
        frame1.pack(fill=BOTH)
        
        lbl1 = Label(frame1, text="Server IP", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=5)           
       
        self.server_ip = Entry(frame1)
        self.server_ip.pack(fill=X, padx=5, pady=5)
        
        frame2 = Frame(self)
        frame2.pack(fill=BOTH)
        
        lbl2 = Label(frame2, text="Alias", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=5)        

        self.alias = Entry(frame2)
        self.alias.pack(fill=X, padx=5, pady=5)
              
        frame3 = Frame(self)
        frame3.pack(fill=BOTH)

        send = Button(frame3, text="Disconnect",
                              fg="red",
                              command=self.disconnect)
        send.pack(side=RIGHT, padx=5, pady=5)
        
        send = Button(frame3, text="Connect",
                              fg="green",
                              command=self.connect)
        send.pack(side=RIGHT, padx=5, pady=5)
        
        frame4 = Frame(self)
        frame4.pack(fill=BOTH)
        
        lbl4 = Label(frame4, text="Chat", width=6)
        lbl4.pack(side=LEFT, anchor=N, padx=5, pady=5)        

        self.dialog = Text(frame4)
        self.dialog.pack(fill=BOTH, pady=5, padx=5)           
              
        frame5 = Frame(self)
        frame5.pack(fill=BOTH)
        
        lbl5 = Label(frame5, text="Message", width=6)
        lbl5.pack(side=LEFT, anchor=N, padx=5, pady=5)        

        self.message = Text(frame5, height=4)
        self.message.pack(fill=BOTH, pady=5, padx=5)           
              
        frame6 = Frame(self)
        frame6.pack(fill=BOTH)

        send = Button(frame6, fg="green",
                              text="Send",
                              command=self.send)
        send.pack(side=RIGHT, padx=5, pady=5)
        
    def connect(self):        
        ip_address = self.server_ip.get()
        self.dialog.insert(END, "You've joined {}\n".format(ip_address))
        self.client.start(self, ip_address)
        
    def disconnect(self):        
        self.dialog.insert(END, "You've left the chat.\n")
        self.client.stop()
        
    def send(self):
        alias = self.alias.get().strip()
        msg = self.message.get("1.0", END).strip()
        self.message.delete("1.0", END)
        
        if len(msg) > 0:
            self.client.send(alias, msg)
            
    def update(self, data):
        colon_pos = data.index(':')
        alias = data[:colon_pos]
        msg = data[colon_pos + 1:]
        output = alias + ": " + msg
        
        self.dialog.insert(END, output + "\n")
        self.dialog.see(END)

        
if __name__ == '__main__':
    root = Tk()
    client = Client()
    app = App(root, client)
    root.after(500, client.run(app))
    root.mainloop()  
