from sqlalchemy import create_engine, Table, MetaData, and_, func
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

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

    # Prepare data for the graph
    data = {
        'Topic': [],
        'Time Spent': [],
        'Target Time': []
    }

    # Write the summary and populate the graph data
    for topic_id, (target_time, topic_name) in target_dict.items():
        total_time = summary.get(topic_id, 0)
        data['Topic'].append(topic_name)
        data['Time Spent'].append(total_time)
        data['Target Time'].append(target_time)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Draw the chart
    chart = st.bar_chart(df.set_index('Topic'))

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

    st.header("Progress for last 7 days:")
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