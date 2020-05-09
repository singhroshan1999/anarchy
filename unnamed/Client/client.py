from unnamed.coding.bencoding import Wrap


def request(request,params,type):
    d = {
        "request": request,
        "params" : params,
        "type" : type
    }
    return Wrap.reduceToBytes(Wrap.dictToBen(d))


def request_append(request,uri):
    return request+":"+uri

def response(reqresp):
    d = Wrap.bytesToReduce(reqresp)
    return d


def request_send(conn,req):
    conn.sendall(req+b'\r\n')


def response_recv(conn):
    b = b''
    while True:
        r = conn.recv(1024)
        b+=r
        if b[-2:] == b'\r\n':
            break
    return str(b[:-2],encoding="utf-8")

