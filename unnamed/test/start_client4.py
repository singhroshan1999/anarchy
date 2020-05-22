from unnamed.Client import client
from unnamed.connection.tcp import TCPConnection
from unnamed.cryptography.host import host
from base64 import b64decode,b64encode
from unnamed.coding.bencoding import Wrap
import time
import random
from unnamed.connection.udp import UDPConnection
pk = host.load_pk('../../CLIEN1_PK',b'1234')
key = host.load_key('../../CLIEN1_KEY')

while True:
    conn = TCPConnection()
    conn.connect("127.0.0.1",1025)
    ring = random.randint(0,100000)
    data = {
            'request' : ['get'],
            'params' : {
                'text' : str(random.randint(0,10000)*random.randint(0,10000)),
            }
        # 'sign': input(),
        # 'ring': str(ring)
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
    req = client.request(reqd)
    # udp = UDPConnection()
    # udp.send(req,('127.0.0.1',1024))
    # data,addr = udp.recv()
    # print(data,addr)
    client.request_send(conn,req)
    b = client.response_recv(conn)
    d = client.response(b)
    # if reqd['request-data']['type'] == 'POST':
    #     b2 = client.response_recv(conn)
    conn.close()
    print('A')
    # time.sleep(0.0001)