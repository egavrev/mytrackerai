import streamlit as st
from models import Journal, engine
from sqlalchemy.orm import sessionmaker
from utils import fetch_data, update_db, handle_date_conversion, validate_input
import datetime

Session = sessionmaker(bind=engine)
session = Session()

# Function to render the Journal screen
def render():
    # Show existing entries
    st.header('Existing Entries')
    journal_entries = fetch_data(Journal)
    for entry in journal_entries:
        st.subheader(f'Date: {entry.date}')
        st.text(f'Domain: {entry.domain}')
        st.text(f'Sentiment: {entry.sentiment}')
        st.text(f'Description: {entry.description}')
    
    # Add new entry
    st.header('Add New Entry')
    date = st.date_input('Date', datetime.date.today())
    domain = st.text_input('Domain')
    sentiment = st.text_input('Sentiment')
    description = st.text_area('Description')
    add_button = st.button('Add Entry')
    
    if add_button:
        if validate_input(domain) and validate_input(sentiment) and validate_input(description):
            add_entry(date, domain, sentiment, description)
        else:
            st.error('Invalid input')
    
    # Delete existing entry
    st.header('Delete Entry')
    entry_id = st.number_input('Entry ID', min_value=1)
    delete_button = st.button('Delete Entry')
    
    if delete_button:
        delete_entry(entry_id)

# Function to add a new journal entry
def add_entry(date, domain, sentiment, description):
    new_entry = Journal(date=handle_date_conversion(date), domain=domain, sentiment=sentiment, description=description,
                        created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
    update_db(new_entry)
    st.success('Entry added successfully')

# Function to delete a journal entry
def delete_entry(id):
    entry = session.query(Journal).get(id)
    if entry is not None:
        session.delete(entry)
        session.commit()
        st.success('Entry deleted successfully')
    else:
        st.error('Entry not found')