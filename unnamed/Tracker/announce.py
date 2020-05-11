# from unnamed.database.sqlite.db import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy import Column,String,Integer
# database = db(":memory")
#
# class Application(database.base):
#     __tablename__ = "application"
#     id = Column(Integer,primary_key=True)
#     name = Column(String)
#     server_id = Column(Integer,ForeignKey('server.id'))
#     server = relationship("Server",back_populates = 'application')
# class Server(database.base):
#     __tablename__ = "server"
#     id = Column(Integer,primary_key=True)
#     hostname
#
#
#TODO