from tracker.settings import database
from tracker.model import App,Server
from sqlalchemy import and_
import random

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
    database.sesson_close(sesson)
    return {'status':'OK'}

def get_server(header):
    sesson = database.new_session()
    if len(sesson.query(App).filter_by(name = header['data']['params']['app']).all()) == 0:
        database.sesson_close(sesson)
        return {'status':'empty'}
    app = sesson.query(App).filter_by(name = header['data']['params']['app']).all()[0]
    serverlist = sesson.query(Server).filter(and_(
        # Server.hostname != header['data']['params']['hostname'], # TODO
        Server.port != header['data']['params']['port'],
        Server.app == app
    )).all()
    rand = random.randint(0,len(serverlist)-1)
    hostname,port = serverlist[rand].hostname,serverlist[rand].port
    print("->",hostname,port)
    database.sesson_close(sesson)
    return {'status':'OK','db':[hostname,port]}

