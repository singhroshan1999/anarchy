from unnamed.Client import client
from unnamed.connection.tcp import TCPConnection
def forward(request,params,hostname,port):
    conn = TCPConnection()
    conn.connect(hostname,port)
    req = client.request(request,params,"POST")
    client.request_send(conn,req)
    d = client.response(client.response_recv(conn))
    conn.close()
    return d