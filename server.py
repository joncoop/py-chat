import socket
import time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

host = get_local_ip()
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print("Server Started on " + host)

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
            
        print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
        for client in clients:
            s.sendto(data, client)
    except:
        pass
    
s.close()
