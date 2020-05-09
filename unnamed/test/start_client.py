from unnamed.Client import client
from unnamed.connection.tcp import TCPConnection

while True:
    conn = TCPConnection()
    conn.connect("127.0.0.1",1026)
    client.request_send(conn, client.request([input()], {"name":input(),"fullname":input(),"email":input()}, "GET"))#request.request({"test":["roshan","singh"]},{"a":1,"b":2},"GET")
    b = client.response_recv(conn)
    print(b)
    d = client.response(b[:-2])
    print(d)
    conn.close()

    print(d["response"]['db'])