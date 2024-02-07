import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Establish a SQLite connection
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

def get_weekly_journal():
    # get date of 7 days ago
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    result = c.execute('SELECT * FROM journal WHERE date >= ?', (week_ago,)).fetchall()
    return result

def get_weekly_self_dev():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    result = c.execute('SELECT * FROM self_dev WHERE date >= ?', (week_ago,)).fetchall()
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