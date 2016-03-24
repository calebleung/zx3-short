import app
import short_config
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = app.engine

Base = declarative_base()

class Shortlinks(Base):
    __tablename__ = 'shortlinks'

    id = Column(Integer, primary_key=True)
    link_id = Column(String)
    link_url = Column(String)
    link_hits = Column(Integer)

    def __repr__(self):
        return "<Shortlinks(link_id='%s', link_url='%s', link_hits='%s')>" % (self.link_id, self.link_url, self.link_hits)

def init():
    Base.metadata.create_all(engine)
    session = app.connectDBSession()
    return session

if __name__ == '__main__':
    session = init()