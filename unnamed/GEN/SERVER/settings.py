from unnamed.database.sqlite.db import db
from unnamed.cryptography.host import host

database = db("SERVER.db")
base = database.base
pk = host.load_pk('SERVER_PK',b'1234')
key = host.load_key('SERVER_KEY')
key_str = host.gen_key_str(key)