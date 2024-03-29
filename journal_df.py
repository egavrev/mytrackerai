from sqlalchemy import create_engine, Table, MetaData, and_
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from streamlit_modal import Modal
import pandas as pd


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

def data_editor_callback(df):
    print(st.session_state["my_key"]["edited_rows"])
    print(df)
    for row in st.session_state["my_key"]["edited_rows"]:
       print({st.session_state["my_key"]["edited_rows"][row]['description']})  
       print(row)
      #      with engine.connect() as conn:
       #         conn.execute(journal.update().where(journal.c.entry_id == row["entry_id"]).values(description=row["description"])
    #clearn session state
    st.session_state["my_key"]["edited_rows"] = {}         

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

    with engine.connect() as conn:
        query = """
            SELECT journal.entry_id, domains.domain, sentiments.sentiment, journal.description
            FROM journal
            JOIN domains ON journal.domain_id = domains.domain_id
            JOIN sentiments ON journal.sentiment_id = sentiments.sentiment_id
            WHERE journal.date >= :selected_date AND journal.date < :next_date
            ORDER BY journal.date DESC
        """
        df = pd.read_sql(query, conn, params={"selected_date": selected_date, "next_date": selected_date + timedelta(days=1)})

    # Display the DataFrame in a Streamlit app transfer df to callback function
    
    st.data_editor(df, num_rows="dynamic", key="my_key", on_change=data_editor_callback, args={"df": df},
        column_config={
        "entry_id":None,
        "domain": {"disabled": True},
        "sentiment": {"disabled": True},
        "description": {"editable": False}})
   
    st.write("Here's the value in Session State:")
    st.write(st.session_state["my_key"]) 