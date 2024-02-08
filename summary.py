from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime, timedelta
import streamlit as st

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
journal = Table('journal', metadata, autoload_with=engine)
self_dev = Table('self_dev', metadata, autoload_with=engine)

def get_weekly_journal():
    # get date of 7 days ago
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    session = Session()
    result = session.execute(journal.select().where(journal.c.date >= week_ago)).fetchall()
    Session.remove()
    return result

def get_weekly_self_dev():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    session = Session()
    result = session.execute(self_dev.select().where(self_dev.c.date >= week_ago)).fetchall()
    Session.remove()
    return result

def app():
    st.title("Weekly Summary")

    st.header("This week's journal entries:")
    journal_entries = get_weekly_journal()
    for entry in journal_entries:
        st.write(entry)

    st.header("This week's self-development entries:")
    self_dev_entries = get_weekly_self_dev()
    for entry in self_dev_entries:
        st.write(entry)