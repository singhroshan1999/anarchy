from anarchy.database.sqlite.db import db
from anarchy.cryptography.host import host

database = db("SERVER.db")
base = database.base
pk = host.load_pk('TRACKER_PK',b'1234')
key = host.load_key('TRACKER_KEY')
key_str = host.gen_key_str(key)