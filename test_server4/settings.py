from unnamed.database.sqlite.db import db
from unnamed.cryptography.host import host

database = db("SERVER1.db")
base = database.base
pk = host.load_pk('SERVER1_PK',b'1234')
key = host.load_key('SERVER1_KEY')
key_str = host.gen_key_str(key)