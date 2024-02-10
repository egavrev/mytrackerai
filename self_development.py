from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU


# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
self_dev = Table('self_dev', metadata, autoload_with=engine)
topics = Table('topics', metadata, autoload_with=engine)

def list_topics():
    session = Session()
    result = session.execute(topics.select()).fetchall()
    topic_dict = {i.topic_id : i.topic for i in result}
    Session.remove()
    return topic_dict

def add_self_dev_entry():
    cols = st.columns([0.70, 1, 2])
    date = cols[0].date_input("Date")

    session = Session()
    topic_list = session.execute(topics.select()).fetchall()
    Session.remove()
    topic_dict = {i.topic: i.topic_id for i in topic_list}
    topic_id = cols[1].selectbox("Topic", list(topic_dict.keys()))

    duration = cols[2].select_slider("Duration", options=range(15, 121, 15))
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Self Development Entry")
    if add_button:
        session = Session()
        session.execute(self_dev.insert().values(date=date, topic_id=topic_dict[topic_id], duration=duration, description=event_desc))
        session.commit()
        Session.remove()
        st.success("Successfully added a new self development entry")

def view_self_dev_entries():

    session = Session()
    result = session.execute(self_dev.select().order_by(self_dev.c.date.desc())).fetchall()
    Session.remove()
    return result
    

def delete_self_dev_entry(entry_id):
    session = Session()
    session.execute(self_dev.delete().where(self_dev.c.entry_id == entry_id))
    session.commit()
    Session.remove()

def app():
    today = datetime.today()
    monday = today + relativedelta(weekday=MO(-1))
    sunday = today + relativedelta(weekday=SU(+1))
    st.header(f"Self development ")
    st.subheader(f" :calendar: {monday.strftime('%Y-%m-%d')} to {sunday.strftime('%Y-%m-%d')}")
    add_self_dev_entry()
    st.markdown("""---""")
    topics = list_topics()
    all_entries = view_self_dev_entries()
    for entry in all_entries:
        cols = st.columns([1, 1, 1, 1, 1])
        cols[0].write(entry.date)
        cols[1].write(topics[entry.topic_id])
        cols[2].write(entry.duration)
        cols[3].write(entry.description)
        if cols[4].button("Delete", key=entry.entry_id):
            delete_self_dev_entry(entry.entry_id)