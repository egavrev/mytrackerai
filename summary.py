from sqlalchemy import create_engine, Table, MetaData, and_, func
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
topics = Table('topics', metadata, autoload_with=engine)

def summarize_self_dev_entries_for_week(start_date):
    # Calculate the end date
    end_date = start_date
    start_date = start_date - timedelta(days=7)
    # Start a new session
    session = Session()

    # Query the self_dev table to get the total duration per topic for the week
    result = session.query(self_dev.c.topic_id, func.sum(self_dev.c.duration)).\
        filter(and_(self_dev.c.date >= start_date, self_dev.c.date < end_date)).\
        group_by(self_dev.c.topic_id).\
        all()

    # Close the session
    Session.remove()

    # Convert the result to a dictionary
    summary = {row[0]: row[1] for row in result}
    

    # Get the target weekly time for each topic
    topic_list = session.execute(topics.select()).fetchall()
    target_dict = {i.topic_id: (i.target_weekly_time, i.topic) for i in topic_list}
    st.write(target_dict)
    # Write the summary
    for topic_id, total_time in summary.items():
        target_time, topic_name = target_dict.get(topic_id, (0, "Unknown"))
        st.write(f"Topic {topic_name}: spent {total_time} minutes, target was {target_time} minutes")

    return summary

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

    st.header("Progress for last 5 days:")
    today = datetime.now()
    summarize_self_dev_entries_for_week(today)


    st.header("This week's journal entries:")
    journal_entries = get_weekly_journal()
    for entry in journal_entries:
        st.write(entry)

    st.header("This week's self-development entries:")
    self_dev_entries = get_weekly_self_dev()
    for entry in self_dev_entries:
        st.write(entry)