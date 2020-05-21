from server3.model import Post,User
from unnamed.multithreading.thread import container
from unnamed.Server import server
from server3.settings import pk,key,database,key_str
from unnamed.cryptography.host import host
from unnamed.coding.bencoding import Wrap

def validate(conn,data,addr):
    print('+',data)
    reqd = server.request(data)
    #validate_reqd
    sesson = database.new_session()
    data = reqd['request-data']['data']
    if len(sesson.query(Post).filter_by(sign = reqd['request-data']['data']['sign']).all()) == 0:
        data['isvalid'] = 'no'
    else:
        data['isvalid'] = 'yes'
    out_bstr = Wrap.toBen(data)
    response_data = {
        'data': data,
        'host': host.b64_str(key_str),
        'sign': host.b64_str(host.sign_str(pk, out_bstr))
    }
    respd = {
        'response-data': response_data,
        'response-type': 'DATA'
    }
    resp = server.response(respd)
    conn.send(resp,addr)
    database.sesson_close(sesson)



def validator(conn):
    c = container()
    while True:
        data,addr = conn.recv()
        print(data)
        data_str = str(data,encoding='utf-8')
        c.run_function(validate,(conn,data_str,addr))
