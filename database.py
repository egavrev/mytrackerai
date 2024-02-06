from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db', echo = True)
meta = MetaData()

journal = Table(
   'journal', meta, 
   Column('id', Integer, primary_key = True), 
   Column('date', Date), 
   Column('domain', String), 
   Column('sentiment', String),
   Column('description', String),
)

self_development = Table(
   'self_development', meta, 
   Column('id', Integer, primary_key = True), 
   Column('date', Date), 
   Column('domain', String), 
   Column('topic', String),
   Column('time_spent', Integer),
   Column('description', String),
)

meta.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()