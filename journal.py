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
journal = Table('journal', metadata, autoload_with=engine)
sentiments = Table('sentiments', metadata, autoload_with=engine)
domains = Table('domains', metadata, autoload_with=engine)

def add_journal_entry():

    # Create columns for date, domain, and sentiment
    cols = st.columns([0.5, 1, 1])

    # Date input
    date = cols[0].date_input("Date",value="today",format="DD-MM-YYYY")

    # Load domains from the topics table
    session = Session()
    domain_list = session.execute(domains.select()).fetchall()
    Session.remove()
    domain_dict = {i.domain: i.domain_id for i in domain_list}
    domain = cols[1].selectbox("Domain", list(domain_dict.keys()))

    # Load sentiments from the sentiments table
    session = Session()
    sentiment_list = session.execute(sentiments.select()).fetchall()
    Session.remove()
    sentiment_dict = {i.sentiment: i.sentiment_id for i in sentiment_list}
    sentiment = cols[2].selectbox("Sentiment", list(sentiment_dict.keys()))

    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Journal Entry")
    if add_button:
        session = Session()
        session.execute(journal.insert().values(date=date, domain=domain_dict[domain], sentiment=sentiment_dict[sentiment], description=event_desc))
        session.commit()
        Session.remove()
        st.success("Successfully added a new journal entry")

def view_journal_entries():
    session = Session()
    result = session.execute(journal.select().order_by(journal.c.date.desc())).fetchall()
    Session.remove()
    return result

def delete_journal_entry(entry_id):
    session = Session()
    session.execute(journal.delete().where(journal.c.entry_id == entry_id))
    session.commit()
    Session.remove()

def app():
    #string to show current week date from monday to sunday
    today = datetime.today()
    monday = today + relativedelta(weekday=MO(-1))
    sunday = today + relativedelta(weekday=SU(+1))
    st.header(f"Journal entries")
    st.subheader(f" :calendar: {monday.strftime('%Y-%m-%d')} to {sunday.strftime('%Y-%m-%d')}")
    add_journal_entry()
    st.markdown("""---""")
    entries = view_journal_entries()
    if entries:
        for entry in entries:
            cols = st.columns([1, 1, 1, 1, 1])
            cols[0].write(entry.date)
            cols[1].write(entry.domain)
            cols[2].write(entry.sentiment)
            cols[3].write(entry.description)
            if cols[4].button("Delete", key=entry.entry_id):
                delete_journal_entry(entry.entry_id)