from server3 import settings
from server3 import model

settings.database.migrate()
sesson = settings.database.new_session()
user = model.User(id=0,name="0",key="00000000000000000000000000000000")
sesson.add(user)
post = model.Post(id=0,text="0",sign="0",xor = "00000000000000000000000000000000",user=user)
sesson.add(post)
sesson.commit()