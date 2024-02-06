from sqlalchemy import Column, Integer, String, Date
from database import Base

class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    domain = Column(String)
    sentiment = Column(String)
    description = Column(String)

class SelfDevelopment(Base):
    __tablename__ = 'self_development'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    domain = Column(String)
    topic = Column(String)
    time_spent = Column(Integer)
    description = Column(String)