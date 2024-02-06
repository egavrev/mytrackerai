import streamlit as st
from database import session
from models import Journal

def journal_entry():
    date = st.date_input('Date')
    domain = st.selectbox('Domain', ['Personal', 'Professional', 'Health', 'Social', 'Other'])
    sentiment = st.selectbox('Sentiment', ['Positive', 'Neutral', 'Negative'])
    description = st.text_area('Description')

    if st.button('Submit'):
        new_entry = Journal(date=date, domain=domain, sentiment=sentiment, description=description)
        session.add(new_entry)
        session.commit()