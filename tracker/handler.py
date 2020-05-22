from unnamed.Server.dispatcher import dispatch
from unnamed.Server import server,POSTForward
from unnamed.coding.bencoding import Wrap
from base64 import b64decode,b64encode
from unnamed.cryptography.host import host
from tracker.settings import pk,key,key_str
from unnamed.connection.tcp import TCPConnection
from unnamed.Client import client

def new(req,**kwargs):
    bstr = Wrap.toBen(req['request-data']['data'])
    key = host.load_key_str(b64decode( req['request-data']['key']))
    sign = b64decode(req['request-data']['sign'])
    # if not host.verify_str(key,bstr,sign):
    #     print("UN VERIFIED")
    #     raise Exception
    # else:
    #     print("VERIFIED")
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

def forward(req,**kwargs):
    #verify_forward-host
    new(req,**kwargs)


handler = {
    'new': new,
    'forward' : forward,
}