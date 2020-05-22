from unnamed.connection.serv import ServLocal
from tracker.dispatch import disp
from tracker.handler import handler
from unnamed.multithreading.thread import container
from unnamed.Server import helper

s = ServLocal()
s.listen()
print(s.hostname,s.port)

c = container()

while True:
    conn,addr = s.accept()
    c.run_function(helper.serve,(conn,addr,handler,disp,s))

