from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
sentiments = Table('sentiments', metadata, autoload_with=engine)

def add_sentiment():
    st.subheader("Add a new sentiment")
    sentiment = st.text_input("Sentiment")
    icon = st.text_input("Icon")
    color = st.color_picker("Color")
    add_button = st.button("Add Sentiment")
    if add_button:
        session = Session()
        session.execute(sentiments.insert().values(sentiment=sentiment, icon=icon, color=color))
        session.commit()
        Session.remove()
        st.success("Successfully added a new sentiment")

def view_sentiments():
    st.subheader("View existing sentiments")
    session = Session()
    result = session.execute(sentiments.select()).fetchall()
    for i in result:
        st.write(i)
    Session.remove()

def delete_sentiment():
    st.subheader("Delete a sentiment")
    session = Session()
    sentiment_list = [i[0] for i in session.execute(sentiments.select())]
    selected_sentiment = st.selectbox("Select sentiment", sentiment_list)
    if st.button("Delete"):
        session.execute(sentiments.delete().where(sentiments.c.sentiment_id == selected_sentiment))
        session.commit()
        st.success("Sentiment deleted")
    Session.remove()

def app():
    st.title("Configuration")
    menu = ["Add Sentiment", "View Sentiments", "Delete Sentiment"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add Sentiment":
        add_sentiment()
    elif choice == "View Sentiments":
        view_sentiments()
    elif choice == "Delete Sentiment":
        delete_sentiment()