from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
self_dev = Table('self_dev', metadata, autoload_with=engine)

def add_self_dev_entry():
    st.subheader("Add a new self development entry")
    date = st.date_input("Date")
    domain = st.text_input("Domain")
    topic = st.text_input("Topic")
    duration = st.select_slider("Duration", options=range(15, 121, 15))
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Self Development Entry")
    if add_button:
        session = Session()
        session.execute(self_dev.insert().values(date=date, domain=domain, topic=topic, duration=duration, description=event_desc))
        session.commit()
        Session.remove()
        st.success("Successfully added a new self development entry")

def view_self_dev_entries():
    st.subheader("View self development entries")
    session = Session()
    result = session.execute(self_dev.select().order_by(self_dev.c.date.desc())).fetchall()
    for i in result:
        st.write(i)
    Session.remove()

def delete_self_dev_entry():
    st.subheader("Delete a self development entry")
    session = Session()
    entry_list = [i[0] for i in session.execute(self_dev.select())]
    selected_entry = st.selectbox("Select entry", entry_list)
    if st.button("Delete"):
        session.execute(self_dev.delete().where(self_dev.c.entry_id == selected_entry))
        session.commit()
        st.success("Entry deleted")
    Session.remove()

def app():
    st.title("Self Development")
    menu = ["Add", "View", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        add_self_dev_entry()
    elif choice == "View":
        view_self_dev_entries()
    elif choice == "Delete":
        delete_self_dev_entry()