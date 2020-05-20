from tracker.settings import database
from tracker.model import App,Server
from sqlalchemy import and_,or_
import random


# def hello(header):
#     sesson = database.new_session()
#     p = sesson.query(Post).all()[0]
#     d = p.user
#     print(p.__dict__,d.__dict__)
#     return  {"db":['p','d']}
#
# def hello2(header):
#     sesson = database.new_session()
#     user = sesson.query(User).filter_by(key=header['key'])[0]
#     post = Post(text = header['data']['params']['text'],sign=header['sign'],user=user)
#     sesson.add(post)
#     sesson.commit()
#     # print(header["params"]["name"])
#     return  {"status":"OK"}
#
# def add_user(header):
#     user = User(name = header['data']['params']['name'], key = header['key'])
#     sesson = database.new_session()
#     sesson.add(user)
#     sesson.commit()
#     return {"status":"OK"}

def add_server(header):
    sesson = database.new_session()
    if len(sesson.query(App).filter_by(name = header['data']['params']['app']).all()) == 0:
        new_app = App(name = header['data']['params']['app'])
        sesson.add(new_app)
    app = sesson.query(App).filter_by(name = header['data']['params']['app']).all()[0]
    new_server = Server(hostname = header['data']['params']['hostname'],
                        port = header['data']['params']['port'],
                        app = app)
    sesson.add(new_server)
    sesson.commit()
    return {'status':'OK'}

def get_server(header):
    sesson = database.new_session()
    if len(sesson.query(App).filter_by(name = header['data']['params']['app']).all()) == 0:
        return {'status':'empty'}
    app = sesson.query(App).filter_by(name = header['data']['params']['app']).all()[0]
    serverlist = sesson.query(Server).filter(and_(
        # Server.hostname != header['data']['params']['hostname'], # TODO
        Server.port != header['data']['params']['port'],
        Server.app == app
    )).all()
    print('server::',serverlist)
    rand = random.randint(0,len(serverlist)-1)
    hostname,port = serverlist[rand].hostname,serverlist[rand].port
    print("->",hostname,port)
    return {'status':'OK','db':[hostname,port]}

