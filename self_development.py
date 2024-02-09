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
domains_self_dev = Table('domains_self_dev', metadata, autoload_with=engine)

def add_self_dev_entry():
    cols = st.columns([0.70, 1, 1, 2])
    date = cols[0].date_input("Date")
    session = Session()
    domain_list = session.execute(domains_self_dev.select()).fetchall()
    Session.remove()
    domain_dict = {i.domain: i.domain_self_dev_id for i in domain_list}
    domain = cols[1].selectbox("Domain", list(domain_dict.keys()))

    session = Session()
    topic_list = session.execute(topics.select()).fetchall()
    Session.remove()
    topic_dict = {i.topic: i.topic_id for i in topic_list}
    topic = cols[2].selectbox("Topic", list(topic_dict.keys()))

    duration = cols[3].select_slider("Duration", options=range(15, 121, 15))
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Self Development Entry")
    if add_button:
        session = Session()
        session.execute(self_dev.insert().values(date=date, domain=domain, topic=topic, duration=duration, description=event_desc))
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

    all_entries = view_self_dev_entries()
    for entry in all_entries:
        cols = st.columns([1, 1, 1, 1, 1, 1])
        cols[0].write(entry.date)
        cols[1].write(entry.domain)
        cols[2].write(entry.topic)
        cols[3].write(entry.duration)
        cols[4].write(entry.description)
        if cols[5].button("Delete", key=entry.entry_id):
            delete_self_dev_entry(entry.entry_id)