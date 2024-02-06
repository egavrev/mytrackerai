from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///my_database.db')
Base = declarative_base()

class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    domain = Column(String)
    sentiment = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class SelfDevelopment(Base):
    __tablename__ = 'self_development'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    domain = Column(String)
    topic = Column(String)
    duration = Column(Integer)
    details = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

Base.metadata.create_all(engine)