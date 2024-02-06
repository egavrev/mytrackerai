import streamlit as st
from database import session
from models import SelfDevelopment

def self_development_entry():
    date = st.date_input('Date')
    domain = st.selectbox('Domain', ['Personal', 'Professional', 'Health', 'Social', 'Other'])
    topic = st.text_input('Topic')
    time_spent = st.number_input('Time Spent (in minutes)', min_value=0)
    description = st.text_area('Description')

    if st.button('Submit'):
        new_entry = SelfDevelopment(date=date, domain=domain, topic=topic, time_spent=time_spent, description=description)
        session.add(new_entry)
        session.commit()