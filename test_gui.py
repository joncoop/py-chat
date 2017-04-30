#!/usr/bin/python3

from tkinter import *

class App:
    
    def __init__(self, master):
        master.title("PyChat")
        
        connection = Frame(master)
        connection.pack()

        chat_frame = Frame(master)
        chat_frame.pack()

        text_entry = Frame(master)
        text_entry.pack()

        # Join section
        ip_address = "192.168.1.64"
        self.connection_text_widget = Text(connection, height=1, width=15)
        self.connection_text_widget.pack(side=LEFT, fill=Y)
        self.connection_text_widget.insert(END, ip_address)

        self.join_btn = Button(connection, 
                               text="Join",
                               command=self.join_chat)
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


        # Message entry
        new_message = ""

        self.msg_text = Text(text_entry, height=4, width=50)
        self.msg_scroll = Scrollbar(text_entry)
        
        self.msg_text.pack(side=LEFT, fill=Y)
        self.msg_scroll.pack(side=RIGHT, fill=Y)
        
        self.msg_text.config(yscrollcommand=self.msg_scroll.set)
        self.msg_scroll.config(command=self.msg_text.yview)
        
        self.msg_text.insert(END, new_message)

        self.send_btn = Button(text_entry,
                               fg="green",
                               text="Send",
                               command=self.send_message)
        self.send_btn.pack(side=LEFT)
    
    def join_chat(self):
        ip_address = self.connection_text_widget.get("1.0",END)
        self.chat_text.insert(END, "You've joined {}\n".format(ip_address))

    def send_message(self):
        msg = self.msg_text.get("1.0",END).strip()

        if len(msg) > 0:
            self.msg_text.delete("1.0",END)
            self.chat_text.insert(END, msg + "\n")

root = Tk()
app = App(root)
root.mainloop()
