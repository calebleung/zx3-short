import short_config
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(short_config.DATABASE, echo=short_config.DEBUG)

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
    print('Database initialized.')

if __name__ == '__main__':
    init()