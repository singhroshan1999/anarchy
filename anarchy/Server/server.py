from anarchy.coding.bencoding import Wrap


def response(resp):
    return Wrap.reduceToBytes(Wrap.dictToBen(resp))


def request(b):
    d = Wrap.bytesToReduce(b)
    return d[0]


def response_send(conn, resp):
    conn.sendall(resp+b'\r\n')


def request_recv(conn):
    b = b''
    while True:
        r = conn.recv(1024)
        b += r
        if b[-2:] == b'\r\n':
            break
    return str(b[:-2],encoding="utf-8")

def request_type_handle(req,handler,**kwargs):
    return handler[req['request-type']](req,**kwargs)