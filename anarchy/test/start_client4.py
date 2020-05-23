from anarchy.Client import client
from anarchy.connection.tcp import TCPConnection
from anarchy.cryptography.host import host
from base64 import b64decode,b64encode
from anarchy.coding.bencoding import Wrap
import time
import random
from anarchy.connection.udp import UDPConnection
pk = host.load_pk('../../CLIEN1_PK',b'1234')
key = host.load_key('../../CLIEN1_KEY')

while True:
    conn = TCPConnection()
    conn.connect("127.0.0.1",1025)
    ring = random.randint(0,100000)
    params = {
                'text' : str(random.randint(0,10000)*random.randint(0,10000)),
            }
    data_sign = str(b64encode(host.sign_str(pk, bstr=Wrap.reduceToBytes(Wrap.dictToBen(params)))), encoding='utf-8')
    data = {
            'request' : ['post'],
            'params' : params,
            'data-sign' : data_sign
        # 'sign': input(),
        # 'ring': str(ring)
        }
    bstr = Wrap.reduceToBytes(Wrap.dictToBen(data))
    reqd = {
        'request-data': {
            'data': data,
            'type': "POST",
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
    # print(b)
    # print(d['response-data']['data']['db'][0][0]['post']['sign'])
    # if host.verify_str(host.load_key_str(b64decode(d['response-data']['data']['db'][0]['user']['key'])),
    #                    Wrap.reduceToBytes(Wrap.dictToBen(d['response-data']['data']['db'][0]['post']['signed-data'])),
    #                                   b64decode(d['response-data']['data']['db'][0]['post']['sign'])):
    #     print("qazwsxedc")
    print(len(b))
    time.sleep(0.001)