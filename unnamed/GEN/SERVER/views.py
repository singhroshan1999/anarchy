from test_server1.settings import database
from test_server1.model import User,Post


def get(header):
    sesson = database.new_session()
    p = sesson.query(Post).all()[0]
    d = p.user
    print(p.__dict__,d.__dict__)
    return  {"db":['p','d']}

def post(header):
    sesson = database.new_session()
    user = sesson.query(User).filter_by(key=header['key'])[0]
    post = Post(text = header['data']['params']['text'],sign=header['sign'],user=user)
    sesson.add(post)
    sesson.commit()
    # print(header["params"]["name"])
    return  {"status":"OK"}

def add_user(header):
    user = User(name = header['data']['params']['name'], key = header['key'])
    sesson = database.new_session()
    sesson.add(user)
    sesson.commit()
    return {"status":"OK"}
