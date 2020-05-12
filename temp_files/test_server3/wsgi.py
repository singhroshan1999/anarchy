from unnamed.connection.serv import ServLocal
from unnamed.Server import server, helper
from temp_files.test_server3 import disp
from temp_files.test_server3 import handler
from temp_files.test_server3 import key,pk

s = ServLocal()
s.listen()
print(s.hostname,s.port)
# update tracker

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

    server.request_type_handle(d,handler=handler,conn = conn,dispatch = disp)

    conn.close()


