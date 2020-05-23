import socks


class SockConnection:

    def __init__(self, proxy="127.0.0.1", port=9050, socks_ver=socks.SOCKS5):
        self.sock = socks.socksocket()
        self.sock.set_proxy(socks_ver, proxy, port)

    def connect(self, host="", port=80):
        if not host.endswith(".onion"):
            print("WARNING: ", host, " may not be onion")
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
    #client
    from anarchy.coding.bencoding import Wrap
    test = SockConnection(port=9050)
    test.connect("xqso4scpm76hrkdkl3vqpfaiemaaee4uxlyiwitztaf4lurv5uazs7qd.onion")
    test.sendall(Wrap.reduceToBytes(Wrap.listToBen(["hello","world",123])))
    print(test.recv())
    test.close()
