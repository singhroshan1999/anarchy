import socket


class ServLocal:
    def __init__(self, hostname='', port=None, protocol_ver=socket.AF_INET):
        self.sock = socket.socket(protocol_ver, socket.SOCK_STREAM)
        self.port = port
        self.hostname = hostname
        for i in range(1024, 49151):
            try:
                self.sock.bind((hostname, i))
            except socket.error as e:
                print(e)
            else:
                self.port = i
                break

    def listen(self, backlog=10):
        self.sock.listen(backlog)

    def accept(self):
        return self.sock.accept()

    def sendall(self, conn, bytes):
        conn.sendall(bytes)

    def send(self, conn, bytes):
        conn.send(bytes)

    def recv(self, conn, buffer=4096):
        return conn.recv(buffer)

    def recvfrom(self, conn, buffer=4096):
        return conn.recvfrom(buffer)

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    try:
        s = ServLocal()
        s.listen()
        print(s.port, " ", s.hostname)
        while True:
            conn, addr = s.accept()
            print(conn, " ", addr)
            print(s.recv(conn))
            print(s.sendall(conn,b"success!"))

    except KeyboardInterrupt:
        s.sock.shutdown(socket.SHUT_RDWR)
        s.close()
        exit(0)



