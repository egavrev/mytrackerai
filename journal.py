from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
journal = Table('journal', metadata, autoload_with=engine)

def add_journal_entry():
    st.subheader("Add a new journal entry")
    date = st.date_input("Date")
    domain = st.text_input("Domain")
    sentiment = st.text_input("Sentiment")
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Journal Entry")
    if add_button:
        session = Session()
        session.execute(journal.insert().values(date=date, domain=domain, sentiment=sentiment, description=event_desc))
        session.commit()
        Session.remove()
        st.success("Successfully added a new journal entry")

def view_journal_entries():
    st.subheader("View journal entries")
    session = Session()
    result = session.execute(journal.select().order_by(journal.c.date.desc())).fetchall()
    for i in result:
        st.write(i)
    Session.remove()

def delete_journal_entry():
    st.subheader("Delete a journal entry")
    session = Session()
    entry_list = [i[0] for i in session.execute(journal.select())]
    selected_entry = st.selectbox("Select entry", entry_list)
    if st.button("Delete"):
        session.execute(journal.delete().where(journal.c.entry_id == selected_entry))
        session.commit()
        st.success("Entry deleted")
    Session.remove()

def app():
    st.title("Journal")
    menu = ["Add", "View", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        add_journal_entry()
    elif choice == "View":
        view_journal_entries()
    elif choice == "Delete":
        delete_journal_entry()