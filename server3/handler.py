from unnamed.Server.dispatcher import dispatch
from unnamed.Server import server,helper
from unnamed.coding.bencoding import Wrap
from base64 import b64decode
from unnamed.cryptography.host import host
from server3.settings import pk,key_str
from unnamed.connection.tcp import TCPConnection
from unnamed.Client import client

def new(req,**kwargs):
    bstr = Wrap.toBen(req['request-data']['data'])
    key = host.load_key_str(b64decode( req['request-data']['key']))
    sign = b64decode(req['request-data']['sign'])
    if not host.verify_str(key,bstr,sign):
        print("UN VERIFIED")
        raise Exception
    else:
        print("VERIFIED")
    data = dispatch(kwargs['dispatch'],list(req['request-data']['data']['request']),req['request-data'])
    out_bstr = Wrap.toBen(data)
    response_data = {
        'data': data,
        'host':host.b64_str(key_str),
        'sign' : host.b64_str(host.sign_str(pk,out_bstr))
    }
    resp = {
        'response-data' : response_data,
        'response-type' : 'DATA'
    }
    server.response_send(kwargs['conn'],server.response(resp))
    if req['request-data']['type'] == 'POST':
        fw_bstr = Wrap.toBen(req['request-data'])
        req['request-type'] = 'forward'
        req['forward-host'] = host.b64_str(key_str)
        req['forward-sign'] = host.b64_str(host.sign_str(pk,fw_bstr))
        print(req)
        trac = helper.tracker_get('127.0.0.1', 1024, ['get'], 'my_app2', '127.0.0.1', kwargs['port'], key, pk)
        req_b = client.request(req)
        fw_conn = TCPConnection()
        fw_conn.connect('127.0.0.1',1025)
        client.request_send(fw_conn,req_b)
        fw_resp_b = client.response_recv(fw_conn)
        fw_resp = client.response(fw_resp_b)
        #verify_response
        server.response_send(kwargs['conn'], server.response(fw_resp))
        kwargs['conn'].close()
        fw_resp_b2 = client.response_recv(fw_conn)
        fw_resp2 = client.response(fw_resp_b)
        #verify_response

        fw_conn.close()

def forward(req,**kwargs):
    #verify_forward-host
    new(req,**kwargs)


handler = {
    'new': new,
    'forward' : forward,
}