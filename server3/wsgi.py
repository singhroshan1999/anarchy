from unnamed.connection.serv import ServLocal
from server3.dispatch import disp
from server3.handler import handler
from server3.settings import key,pk,database
from unnamed.Server import helper
from server3.replication import xor_replication_post
import time
from unnamed.multithreading.thread import container
from server3.validator import validator
from unnamed.connection.udp import UDPConnection
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

def replicate_run():
    while True:
        trac = helper.tracker_get('127.0.0.1', 1024, ['get'], 'my_app2', '127.0.0.1', s.port, key, pk)
        xor_replication_post(trac, database=database)
        time.sleep(1)
replica = container()
replica.run_function(replicate_run)

cont = container()

v = UDPConnection()
v.bind(('127.0.0.1',s.port))
vt = container()
vt.run_function(validator,(v,))


while True:
    conn,addr = s.accept()
    cont.run_function(helper.serve,(conn,addr,handler,disp,s))


