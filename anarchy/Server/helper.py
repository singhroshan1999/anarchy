from anarchy.Client import client
from anarchy.connection.tcp import TCPConnection
from  anarchy.coding.bencoding import Wrap
from base64 import b64encode
from anarchy.cryptography.host import host
from anarchy.Server import server
import sys

def tracker_update(tracker_hostname,
                   tracker_port,
                   request,
                   app_name,
                   hostname,
                   port,
                   key,
                   pk):
    conn = TCPConnection()
    conn.connect(tracker_hostname, tracker_port)
    data = {
        'request': request,
        'params': {
            'app': app_name,
            'hostname': hostname,
            'port': port
        }
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
    client.request_send(conn, req)
    b = client.response_recv(conn)
    d = client.response(b)
    conn.close()
    return d

def tracker_get(tracker_hostname,
                   tracker_port,
                   request,
                   app_name,
                   hostname,
                   port,
                   key,
                   pk):
    conn = TCPConnection()
    conn.connect(tracker_hostname, tracker_port)
    data = {
        'request': request,
        'params': {
            'app': app_name,
            'hostname': hostname,
            'port': port
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
    req = client.request(reqd)
    client.request_send(conn, req)
    b = client.response_recv(conn)
    d = client.response(b)
    conn.close()
    return d

def binToHex(bstr):
    sstr = ""
    for i in bstr:
        sstr += hex(i)[2:]
    return sstr

def serve(conn,addr,handler,disp,s):
    # print(conn,addr)
    b = server.request_recv(conn)
    d = server.request(b)
    # print(d)
    server.request_type_handle(d,handler=handler,conn = conn,dispatch = disp,port = s.port)
    conn.close()
    # print("END1")
    sys.exit()

def invalid_request_response(pk,key_str,sign):
    data = {
        'status' : 'invalid-sign',
        'sign' : sign
    }
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
    return  resp

