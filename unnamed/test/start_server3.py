from unnamed.connection.serv import ServLocal
from unnamed.Server import server,dispatcher
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///new.db')
base = declarative_base()
class User(base):
    __tablename__ = "User"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)
    def __repr__(self):
        return "(%s:%s:%s)"% (self.name,self.fullname,self.email)
base.metadata.create_all(engine)

def hello(header):
    Session = sessionmaker(bind=engine)
    sesson = Session()
    d = sesson.query(User).all()[0]

    print(header["params"]["name"])

    return  {"db":[d.name,d.fullname,d.email]}

def hello2(header):
    user = User(name = header['params']['name'],fullname=header['params']['fullname'],email = header['params']['email'])
    Session = sessionmaker(bind = engine)
    sesson = Session()
    sesson.add(user)
    sesson.commit()
    print(header["params"]["name"])

    return  {"db":["roshan","singh",123456789,"gd76g5d7fg5d67g76et67346t6"]}


disp = {
    "get":hello,
    "post": hello2
}
disp2 = {
    "hello":disp
}

s = ServLocal()
print(s.hostname,s.port)
s.listen()
while True:
    conn,addr = s.accept()
    b = server.request_recv(conn)
    print(b)
    d = server.request(b)
    print(d)
    resp = dispatcher.dispatch(disp,list(d["request"]),d)
    # resp = "hfghfgh"+ str(random.randint(1,1000))
    server.response_send(conn, server.response(resp))
    conn.close()

