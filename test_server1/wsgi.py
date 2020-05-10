from unnamed.connection.serv import ServLocal
from unnamed.Server import server,POSTForward
from unnamed.Server.dispatcher import dispatch
from .dispatch import disp
# from .settings import hostname,port

s = ServLocal()
s.listen()

while True:
    conn,addr = s.accept()
    print(conn,addr)
    b = server.request_recv(conn)
    d = server.request(b)
    resp = dispatch(disp,list(d['request']),d)
    server.response_send(conn,server.response(resp))
    if d['type'] == 'POST':
        d = POSTForward.forward(d['request'], d['params'], '127.0.0.1', 1025)
        server.response_send(conn, server.response(d))


