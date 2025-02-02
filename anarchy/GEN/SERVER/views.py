from test_server1.settings import database
from test_server1.model import User,Post
from anarchy.cryptography.host import host
from anarchy.Server.helper import binToHex

def get(header):
    sesson = database.new_session()
    p = sesson.query(Post).all()[-1]
    d = p.user
    database.sesson_close(sesson)
    return  {"db":[{'post':p.toDict(),'user':d.toDict()}]}

def post(header):
    sesson = database.new_session()
    if len(sesson.query(Post).filter_by(sign = header['data']['data-sign']).all()) > 0 :
        database.sesson_close(sesson)
        return {'status' : 'exist'}
    user = sesson.query(User).filter_by(key=header['key'])[0]
    xor = int(sesson.query(Post).all()[-1].xor,base=16)
    xor ^= int(binToHex(host.hash(bytes(header['data']['data-sign'],encoding='utf-8'))),base=16)
    post = Post(text = header['data']['params']['text'],sign=header['data']['data-sign'],user=user,xor=hex(xor)[2:])
    sesson.add(post)
    sesson.commit()
    database.sesson_close(sesson)
    return  {"status":"OK"}

def add_user(header):
    user = User(name = header['data']['params']['name'], key = header['key'])
    sesson = database.new_session()
    sesson.add(user)
    sesson.commit()
    database.sesson_close(sesson)
    return {"status":"OK"}

def replicate(header):
    xor_key = header['data']['params']['xor']
    sesson = database.new_session()
    if len(sesson.query(Post).filter_by(xor=xor_key).all()) == 0:
        database.sesson_close(sesson)
        return {'status':'NOT_FOUND'}
    xor_id = sesson.query(Post).filter_by(xor=xor_key)[0].id
    lst = sesson.query(Post).filter(Post.id > xor_id)
    resp_lst = []
    for i in lst:
        user = sesson.query(User).filter_by(id=i.user_id)[0]
        resp_lst.append({'text': i.text, 'sign': i.sign, 'key': user.key})
    database.sesson_close(sesson)
    return {'status': 'OK', 'response': resp_lst}

