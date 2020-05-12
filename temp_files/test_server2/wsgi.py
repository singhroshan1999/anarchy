from unnamed.connection.serv import ServLocal
from unnamed.Server import server
from temp_files.test_server2.dispatch import disp
from temp_files.test_server2 import handler
from temp_files.test_server2 import key,pk
from unnamed.Server import helper

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
    conn,addr = s.accept()
    print(conn,addr)
    b = server.request_recv(conn)
    d = server.request(b)
    print(d)
    # if d['type'] == 'POST':
    #     d = POSTForward.forward(d['request'], d['params'], '127.0.0.1', 1024)
    #     server.response_send(conn, server.response(d))
    server.request_type_handle(d,handler=handler,conn = conn,dispatch = disp)
    print("END2")
    conn.close()


