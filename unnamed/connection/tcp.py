import socket


class TCPConnection:

    def __init__(self,protocol_ver=socket.AF_INET):
        self.sock = socket.socket(protocol_ver,socket.SOCK_STREAM)

    def connect(self, host="", port=80):
        self.sock.connect((host, port))
        # some handshaking code

    def sendall(self,str):
        self.sock.sendall(str)

    def send(self,byte):
        self.sock.send(byte)

    def recv(self,buffer=4096):
        return self.sock.recv(buffer)

    #TODO : recvfrom
    # def recvfrom(self,buffer=4096):
    #     return self.recvfrom(buffer)

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    test = TCPConnection()
    test.connect("facebook.com")
    test.sendall(b"GET / HTTP/1.1\r\n"+b"Host: facebookcorewwwi.onion\r\n\r\n")
    print(test.recv())
    test.close()
