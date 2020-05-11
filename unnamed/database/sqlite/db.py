from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

class db:
    def __init__(self,path):
        self.engine = create_engine("sqlite:///"+path)
        self.base = declarative_base()
        self._session = sessionmaker(bind=self.engine)
    def new_session(self):
        return self._session()
    def migrate(self):
        self.base.metadata.create_all(self.engine)

