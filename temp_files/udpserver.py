from anarchy.connection.udp import UDPConnection

s = UDPConnection()
s.bind(('127.0.0.1',1024))
while True:
    data,addr = s.recv()
    print(data,addr)
    s.send(data+b'|resived',addr)