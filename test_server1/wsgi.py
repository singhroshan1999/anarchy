from unnamed.connection.serv import ServLocal
from unnamed.Server import server,POSTForward
from tracker.dispatch import disp
from tracker.handler import handler

s = ServLocal()
s.listen()
print(s.hostname,s.port)

while True:
    conn,addr = s.accept()
    print(conn,addr)
    b = server.request_recv(conn)
    d = server.request(b)
    print(d)
    # if d['type'] == 'POST':
    #     d = POSTForward.forward(d['request'], d['params'], '127.0.0.1', 1024)
    #     server.response_send(conn, server.response(d))
    server.request_type_handle(d,handler=handler,conn = conn,dispatch = disp)

    conn.close()
    print("END1")

