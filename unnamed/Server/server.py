from unnamed.coding.bencoding import Wrap


def response(resp):
    d = {"response":resp}
    return Wrap.reduceToBytes(Wrap.dictToBen(d))


def request(b):
    d = Wrap.bytesToReduce(b)
    return d


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

