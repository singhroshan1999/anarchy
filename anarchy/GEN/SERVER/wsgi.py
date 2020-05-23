from anarchy.connection.serv import ServLocal
from test_server1.dispatch import disp
from test_server1.handler import handler
from test_server1.settings import key,pk,database
from anarchy.Server import helper
from test_server1.replication import xor_replication_post
import time
from anarchy.multithreading.thread import container
from test_server1.validator import validator
from anarchy.connection.udp import UDPConnection
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
        if trac['response-data']['data']['status'] == 'empty-list':
            time.sleep(5)
            continue
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


