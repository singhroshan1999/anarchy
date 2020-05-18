from unnamed.connection.serv import ServLocal
from unnamed.Server import server
from server1.dispatch import disp
from server1.handler import handler
from server1.settings import key,pk,database
from unnamed.Server import helper
from server1.replication import xor_replication_post
import time
from unnamed.multithreading.thread import container
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

# while True:
#     trac = helper.tracker_get('127.0.0.1', 1024, ['get'], 'my_app2', '127.0.0.1',s.port, key, pk)
#     xor_replication_post(trac,database=database)
#     time.sleep(5)

cont = container()

while True:
    conn,addr = s.accept()
    cont.run_function(helper.serve,(conn,addr,handler,disp,s))


