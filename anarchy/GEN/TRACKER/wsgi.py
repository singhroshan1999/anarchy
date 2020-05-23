from anarchy.connection.serv import ServLocal
from tracker.dispatch import disp
from tracker.handler import handler
from anarchy.multithreading.thread import container
from anarchy.Server import helper

s = ServLocal()
s.listen()
print(s.hostname,s.port)

c = container()

while True:
    conn,addr = s.accept()
    c.run_function(helper.serve,(conn,addr,handler,disp,s))

