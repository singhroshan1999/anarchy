from unnamed.Client import client
from unnamed.connection.tcp import TCPConnection
from  unnamed.coding.bencoding import Wrap
from base64 import b64encode
from unnamed.cryptography.host import host

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