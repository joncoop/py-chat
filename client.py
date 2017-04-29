import socket
import threading
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data))
        except:
            pass
        finally:
            tLock.release()

host = get_local_ip()
port = 0

server_ip = input("Enter server ip:")           
server = (server_ip, 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

alias = input("Name: ")
message = input(alias + "-> ")
while message != 'q':
    if message != '':
        s.sendto((alias + ": " + message).encode(), server)
    tLock.acquire()
    message = input(alias + "-> ")
    tLock.release()
    time.sleep(0.2)

shudown = True
rT.join()
s.close()
