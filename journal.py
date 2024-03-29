from sqlalchemy import create_engine, Table, MetaData, and_
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from streamlit_modal import Modal

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
journal = Table('journal', metadata, autoload_with=engine)
sentiments = Table('sentiments', metadata, autoload_with=engine)
domains = Table('domains', metadata, autoload_with=engine)

def list_sentiments():
    session = Session()
    result = session.execute(sentiments.select()).fetchall()
    #domain_dict = {i.domain: i.domain_id for i in domain_list}
    Session.remove()
    return result

def list_domains():
    session = Session()
    result = session.execute(domains.select()).fetchall()
    #domain_dict = {i.domain: i.domain_id for i in domain_list}
    Session.remove()
    return result

def add_journal_entry(date_input=datetime.today()):

    # Create columns for date, domain, and sentiment
    cols = st.columns([ 1, 1])

    # Date input
    date = date_input

    # Load domains from the topics table
    session = Session()
    domain_list = session.execute(domains.select()).fetchall()
    Session.remove()
    domain_dict = {i.domain: i.domain_id for i in domain_list}
    domain_id = cols[0].selectbox("Domain", list(domain_dict.keys()))

    # Load sentiments from the sentiments table
    session = Session()
    sentiment_list = session.execute(sentiments.select()).fetchall()
    Session.remove()
    sentiment_dict = {i.sentiment: i.sentiment_id for i in sentiment_list}
    sentiment_id = cols[1].selectbox("Sentiment", list(sentiment_dict.keys()))

    # Create a placeholder for the text area
    event_desc_placeholder = st.empty()
    event_desc = event_desc_placeholder.text_area("Event Description")

    add_button = st.button("Add Journal Entry")
    if add_button:
        session = Session()
        session.execute(journal.insert().values(date=date, domain_id=domain_dict[domain_id], sentiment_id=sentiment_dict[sentiment_id], description=event_desc))
        session.commit()
        Session.remove()
        st.success("Successfully added a new journal entry")

        # Clear the text area
        event_desc_placeholder.empty()

def view_journal_entries():
    session = Session()
    result = session.execute(journal.select().order_by(journal.c.date.desc())).fetchall()
    Session.remove()
    return result

def view_journal_entries_for_date(date):
    session = Session()
    result = session.execute(journal.select().where(and_(journal.c.date >= date, journal.c.date < date + timedelta(days=1))).order_by(journal.c.date.desc())).fetchall()
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

    # Add date input
    selected_date = st.date_input("Select a date", value=today)
    add_journal_entry(selected_date)
    st.markdown("""---""")
   # entries = view_journal_entries()
    entries = view_journal_entries_for_date(selected_date)
    sentiments_list = list_sentiments()
    domains_list = list_domains()   


    if entries:
        for entry in entries:
            cols = st.columns([0.5, 0.2, 2.7, 0.5],gap="small")
            color = sentiments_list[entry.sentiment_id-1][3]
            cols[0].markdown(f"<div style='background-color:{color}; padding:10px;'><strong style='color:black;'>{domains_list[entry.domain_id-1][1]}</strong></div>", unsafe_allow_html=True)
            cols[1].markdown(sentiments_list[entry.sentiment_id-1][2])
            # Create a text area for the description and set its initial value to the current description            
            cols[2].markdown(f"{entry.description[:150]}...", unsafe_allow_html=True)
            # Create a placeholder for the text area
            if cols[3].button("Delete", key=entry.entry_id):
                delete_journal_entry(entry.entry_id)