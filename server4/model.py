from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from server4 import settings
import datetime

class User(settings.base):
    __tablename__ = "User"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    key = Column(String,unique=True,nullable=True)

    def __repr__(self):
        return "(%s:%s)"% (self.name,self.key)
    def toDict(self):
        return {
                'key': self.key,
                'name':self.name
                }
class Post(settings.base):
    __tablename__ = "post"
    id = Column(Integer,primary_key=True,autoincrement=True)
    text = Column(String)
    datetime = Column(DateTime,default=datetime.datetime.now())
    sign = Column(String,unique=True,nullable=False)
    xor = Column(String,unique=True,nullable=False)
    user_id = Column(Integer,ForeignKey('User.id'))
    user = relationship("User")
    def __repr__(self):
        return "(%s:%s:%s:%s:%s)"% (self.text,self.datetime,self.sign,self.user_id,self.user)
    def toDict(self):
        return {'sign': self.sign,
                'signed-data':{
                    'text':self.text
                },
                'datetime':str(self.datetime)
                }

