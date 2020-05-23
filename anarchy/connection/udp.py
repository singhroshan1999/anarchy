import socket

class UDPConnection:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    def send(self,bstr,addr):
        self.sock.sendto(bstr,addr)
    def recv(self,buff=1024):
        return self.sock.recvfrom(buff)
    def bind(self,addr):
        self.sock.bind(addr)

