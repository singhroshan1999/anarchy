from unnamed.coding.bencoding import Wrap


def request(req):
    # d = {
    #     "data":data,
    #     "type" : type,
    #     "key" : key,
    #     "sign" : sign
    # }
    return Wrap.reduceToBytes(Wrap.dictToBen(req))


def request_append(request,uri):
    return request+":"+uri

def response(reqresp):
    d = Wrap.bytesToReduce(reqresp)
    return d[0]


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

