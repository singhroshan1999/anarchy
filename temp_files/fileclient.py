import socket

out = open('out.py','wb+')
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',1024))
inp = b""
inp+= s.recv(1024)
indx = inp.find(b'\r\n')
size = int(str(inp[:indx],encoding='utf8'))
inp = inp[indx+2:]
while len(inp) < size-1:
    inp+=s.recv(1024)
out.write(inp)
s.close()