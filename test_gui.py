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
        self.ip_address = "192.168.1.64"
        self.connection_text_widget = Text(connection, height=1, width=15)
        self.connection_text_widget.pack(side=LEFT, fill=Y)
        self.connection_text_widget.insert(END, self.ip_address)

        self.button = Button(connection, 
                             text="Join", fg="red",
                             command=self.join_chat)
        self.button.pack(side=LEFT)

        
        # Chat area
        self.chat_log = "Begin chat...\n"
        
        self.chat_text = Text(chat_frame, height=20, width=50)
        self.chat_scroll = Scrollbar(chat_frame)
        
        self.chat_text.pack(side=LEFT, fill=Y)
        self.chat_scroll.pack(side=RIGHT, fill=Y)
        
        self.chat_text.config(yscrollcommand=self.chat_scroll.set)
        self.chat_scroll.config(command=self.chat_text.yview)
        
        self.chat_text.insert(END, self.chat_log)


        # Message entry
        new_message = ""

        self.T = Text(text_entry, height=4, width=50)
        self.S = Scrollbar(text_entry)
        
        self.T.pack(side=LEFT, fill=Y)
        self.S.pack(side=RIGHT, fill=Y)
        
        self.T.config(yscrollcommand=self.S.set)
        self.S.config(command=self.T.yview)
        
        self.T.insert(END, new_message)

        self.slogan = Button(text_entry,
                             text="Send",
                             command=self.send_message)
        self.slogan.pack(side=LEFT)
    
    def join_chat(self):
        self.T.insert(END, "You've join a chat...\n")

    def send_message(self):
        message = self.T.get("1.0",END)
        self.T.delete("1.0",END)
        
        self.chat_text.insert(END, message)

root = Tk()
app = App(root)
root.mainloop()
