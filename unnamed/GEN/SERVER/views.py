from test_server1.settings import database
from test_server1.model import User,Post
from unnamed.cryptography.host import host
from unnamed.Server.helper import binToHex

def get(header):
    sesson = database.new_session()
    p = sesson.query(Post).all()[0]
    d = p.user
    print(p.__dict__,d.__dict__)
    database.sesson_close(sesson)
    return  {"db":['p','d']}

def post(header):
    sesson = database.new_session()
    if len(sesson.query(Post).filter_by(sign = header['sign']).all()) > 0 :
        database.sesson_close(sesson)
        return {'status' : 'exist'}
    user = sesson.query(User).filter_by(key=header['key'])[0]
    xor = int(sesson.query(Post).all()[-1].xor,base=16)
    print(xor)
    xor ^= int(binToHex(host.hash(bytes(header['sign'],encoding='utf-8'))),base=16)
    post = Post(text = header['data']['params']['text'],sign=header['sign'],user=user,xor=hex(xor)[2:])
    sesson.add(post)
    sesson.commit()
    # print(header["params"]["name"])
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
    print('x')
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

