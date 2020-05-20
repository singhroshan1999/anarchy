from unnamed.connection.udp import UDPConnection

while True:
    text = bytes(input(),encoding='utf-8')
    s = UDPConnection()
    s.send(text,('127.0.0.1',1024))
    data,addr = s.recv()
    print(data,addr)