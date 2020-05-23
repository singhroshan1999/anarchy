from test_server1.model import Post,User
from anarchy.multithreading.thread import container
from anarchy.Server import server
from test_server1.settings import pk,key,database,key_str
from anarchy.cryptography.host import host
from anarchy.coding.bencoding import Wrap

def validate(conn,data,addr):
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
        data_str = str(data,encoding='utf-8')
        c.run_function(validate,(conn,data_str,addr))
