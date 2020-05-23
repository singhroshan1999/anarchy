from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from tracker import settings
import datetime

class App(settings.base):
    __tablename__ = "app"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    # key = Column(String,unique=True,nullable=True)

    def __repr__(self):
        return "(%s)"% (self.name)
class Server(settings.base):
    __tablename__ = "server"
    id = Column(Integer,primary_key=True,autoincrement=True)
    hostname = Column(String,nullable=False)
    port = Column(Integer,nullable=False)
    app_id = Column(Integer,ForeignKey('app.id'))
    app = relationship("App")
    def __repr__(self):
        return "(%s:%s:%s:%s)"% (self.hostname,self.port,self.app_id,self.app)

