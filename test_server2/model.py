from sqlalchemy import Column,String,Integer
from test_server1 import settings

class User(settings.base):
    __tablename__ = "User"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)
    def __repr__(self):
        return "(%s:%s:%s)"% (self.name,self.fullname,self.email)
