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
        # print("UN VERIFIED")
        resp = helper.invalid_request_response(pk,key_str,req['request-data']['sign'])
        server.response_send(kwargs['conn'], server.response(resp))
        kwargs['conn'].close()
        raise Exception
    # else:
        # print("VERIFIED")
        # pass
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
    if req['request-data']['type'] == 'POST' and data['status'] == 'OK':
        flag = True
        while True:
            fw_bstr = Wrap.toBen(req['request-data'])
            req['request-type'] = 'forward'
            req['forward-host'] = host.b64_str(key_str)
            req['forward-sign'] = host.b64_str(host.sign_str(pk,fw_bstr))
            trac = helper.tracker_get('127.0.0.1', 1024, ['get'], 'my_app2', '127.0.0.1', kwargs['port'], key, pk)
            fw_conn = TCPConnection()
            fw_conn.connect(trac['response-data']['data']['db'][0], trac['response-data']['data']['db'][1])
            req_b = client.request(req)
            client.request_send(fw_conn,req_b)
            fw_resp_b = client.response_recv(fw_conn)
            fw_resp = client.response(fw_resp_b)
            #verify_response
            fw_bstr = Wrap.toBen(fw_resp['response-data']['data'])
            fw_key = host.load_key_str(b64decode(fw_resp['response-data']['host']))
            fw_sign = b64decode(fw_resp['response-data']['sign'])
            if not host.verify_str(fw_key, fw_bstr, fw_sign):
                # print("UN VERIFIED")
                resp = helper.invalid_request_response(pk, key_str, fw_resp['response-data']['host'])
                server.response_send(fw_conn, server.response(resp))
                fw_conn.close()
                # return
                raise Exception
            if flag:
                server.response_send(kwargs['conn'], server.response(fw_resp))
                kwargs['conn'].close()
                flag = False
            if fw_resp['response-data']['data']['status'] != 'OK':
                fw_conn.close()
                return
            fw_resp_b2 = client.response_recv(fw_conn)
            fw_resp2 = client.response(fw_resp_b2)
            fw_bstr2 = Wrap.toBen(fw_resp2['response-data']['data'])
            fw_key2 = host.load_key_str(b64decode(fw_resp2['response-data']['host']))
            fw_sign2 = b64decode(fw_resp2['response-data']['sign'])
            if not host.verify_str(fw_key2, fw_bstr2, fw_sign2):
                # print("UN VERIFIED")
                resp = helper.invalid_request_response(pk, key_str, fw_resp2['response-data']['host'])
                server.response_send(fw_conn, server.response(resp))
                fw_conn.close()
                continue
                # raise Exception
            #verify_response
        fw_conn.close()

def forward(req,**kwargs):
    #verify_forward-host
    fw_bstr = Wrap.toBen(req['request-data'])
    fw_key = host.load_key_str(b64decode(req['forward-host']))
    fw_sign = b64decode(req['forward-sign'])
    if not host.verify_str(fw_key,fw_bstr,fw_sign):
        resp = helper.invalid_request_response(pk, key_str, req['forward-host'])
        server.response_send(kwargs['conn'], server.response(resp))
        kwargs['conn'].close()
        return
    new(req,**kwargs)


handler = {
    'new': new,
    'forward' : forward,
}