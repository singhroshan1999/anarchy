from unnamed.Client import client
from unnamed.connection.tcp import TCPConnection
from unnamed.cryptography.host import host
from base64 import b64decode,b64encode
from unnamed.coding.bencoding import Wrap
import time
pk = host.load_pk('../../CLIEN1_PK',b'1234')
key = host.load_key('../../CLIEN1_KEY')
while True:
    conn = TCPConnection()
    conn.connect("127.0.0.1",1024)
    data = {
        "request" : [input()],
        "params" : {"name": input(), "fullname": input(), "email": input()},

    }
    bstr = Wrap.reduceToBytes(Wrap.dictToBen(data))
    request_data = {

        'data' : data,
        'type' : input(),
        'key'  : str(b64encode(host.gen_key_str(key)), encoding='utf-8'),
        'sign' : str(b64encode(host.sign_str(pk, bstr=bstr)), encoding='utf-8')
    }
    reqd = {
        'request-data' : request_data,
        'request-type' : 'new',
    }
    req = client.request(reqd)
    print(req)
    # print((len(req)*8)/1000.0)
    # time.sleep((len(req)*8)/1000.0)
    client.request_send(conn,req)
    b = client.response_recv(conn)
    print(b)
    d = client.response(b)
    print(d)
    conn.close()

    print(d['response-type'])