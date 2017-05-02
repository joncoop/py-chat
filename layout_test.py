#!/usr/bin/python3

from tkinter import *
    
class App:
    
    def __init__(self, master):
        # Titlebar
        master.title("Grid Layout")

        # Elements
        Label(master, text="Status").grid(row=0, column=0, sticky=E)
        Label(master, text="Server IP").grid(row=1, column=0, sticky=E)
        Label(master, text="Alias").grid(row=2, column=0, sticky=E)

        status = Message(master, text="Disconnected")
        server_ip = Entry(master)
        alias = Entry(master)

        dialog = Text(master)
        message = Entry(master)
        
        join_btn = Button(text="Join",
                               command=self.join_chat)

        leave_btn = Button(text="Leave",
                               command=self.leave_chat)

        send_btn = Button(text="Send",
                               command=self.send_message)

        # Layout
        status.grid(row=0, column=1)
        server_ip.grid(row=1, column=1)
        alias.grid(row=2, column=1)
        join_btn.grid(row=3, column=1)
        leave_btn.grid(row=4, column=1)
        
        dialog.grid(row=0, column=2, rowspan=5)
        message.grid(row=4, column=2)
        send_btn.grid(row=5, column=2)
        
        '''
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
        self.msg_text = Text(text_entry, height=4, width=50)
        self.msg_scroll = Scrollbar(text_entry)
        
        self.msg_text.pack(side=LEFT, fill=Y)
        self.msg_scroll.pack(side=RIGHT, fill=Y)
        
        self.msg_text.config(yscrollcommand=self.msg_scroll.set)
        self.msg_scroll.config(command=self.msg_text.yview)
        
        self.send_btn = Button(text_entry,
                               fg="green",
                               text="Send",
                               command=self.send_message)
        self.send_btn.pack(side=LEFT)
        '''
              
    def join_chat(self):        
        pass

    def leave_chat(self):        
        pass

    def send_message(self):
        passs       

    def update_chat(self, data):     
        pass


if __name__ == "__main__":    
    root = Tk()
    app = App(root)
    root.mainloop()
