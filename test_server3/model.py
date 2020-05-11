from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from test_server3 import settings
import datetime


class User(settings.base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    key = Column(String, unique=True, nullable=True)

    def __repr__(self):
        return "(%s:%s:%s)" % (self.name, self.fullname, self.email)


class Post(settings.base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.now())
    sign = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User")

    def __repr__(self):
        return "(%s:%s:%s:%s:%s)" % (self.text, self.datetime, self.sign, self.user_id, self.user)

