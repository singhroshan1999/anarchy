from anarchy.Server import server,helper
from anarchy.coding.bencoding import Wrap
from base64 import b64decode,b64encode
from anarchy.cryptography.host import host
from test_server1.settings import pk,key
from test_server1.model import User,Post
from anarchy.connection.tcp import TCPConnection
from anarchy.Client import client
import time

def xor_replication_post(trac,database):
    if trac['response-data']['data']['status'] == 'empty':
        return
    sesson = database.new_session()
    respd = None
    rows = sesson.query(Post).order_by(Post.id).all()
    r = len(rows)
    database.sesson_close(sesson)
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
            # time.sleep(1)
        else:
            break
    if respd is None :
        return
    sesson = database.new_session()
    print(respd['response-data']['data']['response'])
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
    database.sesson_close(sesson)

