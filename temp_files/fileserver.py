import socket
import os

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',1024))
s.listen()
while True:
    conn,addr = s.accept()
    inp = open("sqlalchemyy.py",'rb')

    size = os.path.getsize('sqlalchemyy.py')
    print("1")
    conn.sendall(bytes(str(size),encoding='utf-8')+b'\r\n')

    while inp.tell() < size-1:
        conn.sendall(inp.read(1024))
    conn.close()