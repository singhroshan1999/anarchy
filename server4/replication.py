from unnamed.Server.dispatcher import dispatch
from unnamed.Server import server,helper
from unnamed.coding.bencoding import Wrap
from base64 import b64decode,b64encode
from unnamed.cryptography.host import host
from server4.settings import pk,key
from server4.model import User,Post
from unnamed.connection.tcp import TCPConnection
from unnamed.Client import client
import time

def xor_replication(Table,trac,database):
    sesson = database.new_session()
    # if len(sesson.query(Table).all()) == 0:
    #     sessor
    last_row = sesson.query(Table).order_by(Table.id)[-1]


def xor_replication_post(trac,database):
    if trac['response-data']['data']['status'] == 'empty':
        return
    sesson = database.new_session()
    # if len(sesson.query(Table).all()) == 0:
    #     sessor

    # fw_conn = TCPConnection()

    respd = None
    rows = sesson.query(Post).order_by(Post.id).all()
    # l = 0
    r = len(rows)
    # xor_key = last_row.xor
    while r > 0 :
        print(r)
        xor_key = rows[r-1].xor
        data = {
                'request' : ['replicate'],
                'params' : {
                    'xor' : xor_key,
                }
            }
        bstr = Wrap.reduceToBytes(Wrap.dictToBen(data))
        reqd = {
            'request-data': {
                'data': data,
                'type': "GET",
                'key': str(b64encode(host.gen_key_str(key)), encoding='utf-8'),
                'sign': str(b64encode(host.sign_str(pk, bstr=bstr)), encoding='utf-8')
            },
            'request-type': 'new'
        }
        fw_conn = TCPConnection()
        # fw_conn.connect('127.0.0.1', 1025)
        try:
            fw_conn.connect(trac['response-data']['data']['db'][0], trac['response-data']['data']['db'][1])
        except ConnectionRefusedError:
            break
        req = client.request(reqd)
        client.request_send(fw_conn,req)
        resp = client.response_recv(fw_conn)
        respd = client.response(resp)
        fw_conn.close()
        if(respd['response-data']['data']['status'] == 'NOT_FOUND'):
            r-=1
            time.sleep(1)
        else:
            break
    if respd is None :
        return
    for i in range(len(respd['response-data']['data']['response'])):
        if len(sesson.query(Post).filter_by(sign=respd['response-data']['data']['response'][i]['sign']).all()) > 0:
            continue
        userlst = sesson.query(User).filter_by(key=respd['response-data']['data']['response'][i]['key']).all()
        if len(userlst) == 0:
            u = User(key = respd['response-data']['data']['response'][i]['key'])
            sesson.add(u)
        user = sesson.query(User).filter_by(key=respd['response-data']['data']['response'][i]['key'])[0]
        xor = int(sesson.query(Post).all()[-1].xor, base=16)
        xor ^= int(helper.binToHex(host.hash(bytes(respd['response-data']['data']['response'][i]['sign'],encoding='utf-8'))),base=16)
        post = Post(text = respd['response-data']['data']['response'][i]['text'],sign=respd['response-data']['data']['response'][i]['sign'],user=user,xor=hex(xor)[2:])
        sesson.add(post)
    sesson.commit()


