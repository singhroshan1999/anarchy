from unnamed.connection.serv import ServLocal
from unnamed.Server import server
from server4.dispatch import disp
from server4.handler import handler
from server4.settings import key,pk,database
from unnamed.Server import helper
from server4.replication import xor_replication_post
import time
s = ServLocal()
s.listen()
print(s.hostname,s.port)

helper.tracker_update('127.0.0.1',
                      1024,
                      ['add'],
                      'my_app2',
                      '127.0.0.1',
                      s.port,
                      key,
                      pk)

while True:
    trac = helper.tracker_get('127.0.0.1', 1024, ['get'], 'my_app2', '127.0.0.1',s.port, key, pk)
    xor_replication_post(trac,database=database)
    time.sleep(5)

while True:
    conn,addr = s.accept()
    print(conn,addr)
    b = server.request_recv(conn)
    d = server.request(b)
    print(d)
    # if d['type'] == 'POST':
    #     d = POSTForward.forward(d['request'], d['params'], '127.0.0.1', 1024)
    #     server.response_send(conn, server.response(d))
    server.request_type_handle(d,handler=handler,conn = conn,dispatch = disp,port = s.port)

    conn.close()
    print("END1")

