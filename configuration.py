from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import streamlit as st

# Create engine and scoped session
engine = create_engine('sqlite:///sqlite.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Reflect tables
metadata = MetaData()
# Reflect additional tables
sentiments = Table('sentiments', metadata, autoload_with=engine)
domains = Table('domains', metadata, autoload_with=engine)
topics = Table('topics', metadata, autoload_with=engine)


#add functions for sentiments
def add_sentiment():
    st.subheader("Add a new sentiment")
    sentiment = st.text_input("Sentiment")
    icon = st.text_input("Icon")
    color = st.text_input("Color")
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
    entries = session.execute(sentiments.select()).fetchall()
    if entries:
        for entry in entries:
            cols = st.columns([1, 1, 1, 1, 1])
            cols[0].write(entry.sentiment_id)
            cols[1].write(entry.sentiment)
            cols[2].write(entry.icon)
            cols[3].write(entry.color)
            if cols[4].button("Delete", key=entry.sentiment_id):
                delete_sentiment(entry.sentiment_id)
    Session.remove()

def delete_sentiment(sentiment_id):
    session = Session()
    session.execute(sentiments.delete().where(sentiments.c.sentiment_id == sentiment_id))
    session.commit()
    st.success("Sentiment deleted")
    Session.remove()

# Add functions for domains
def add_domain():
    st.subheader("Add a new domain")
    domain = st.text_input("Domain")
    add_button = st.button("Add Domain")
    if add_button:
        session = Session()
        session.execute(domains.insert().values(domain=domain))
        session.commit()
        Session.remove()
        st.success("Successfully added a new domain",icon="✅")

def view_domains():
    st.subheader("View existing domains")
    session = Session()
    entries = session.execute(domains.select()).fetchall()
    if entries:
        for entry in entries:
            cols = st.columns([1, 1, 1])
            cols[0].write(entry.domain_id)
            cols[1].write(entry.domain)
            if cols[2].button("Delete", key=entry.domain_id):
                print(f"delete domain {entry.domain_id}")
                delete_domain(entry.domain_id)
    Session.remove()

def delete_domain(domain_id):
    session = Session()
    session.execute(domains.delete().where(domains.c.domain_id == domain_id))
    session.commit()
    Session.remove()

# Add similar functions for domains_self_dev and topics
def add_topic():
    st.subheader("Add a new topic")
    topic = st.text_input("Topic")
    add_button = st.button("Add Topic")
    if add_button:
        session = Session()
        session.execute(topics.insert().values(topic=topic))
        session.commit()
        Session.remove()

def view_topic():
    st.subheader("View existing topics")
    session = Session()
    entries = session.execute(topics.select()).fetchall()
    if entries:
        for entry in entries:
            cols = st.columns([1, 1, 1])
            cols[0].write(entry.topic_id)
            cols[1].write(entry.topic)
            if cols[2].button("Delete", key=entry.topic_id):
                delete_topic(entry.topic_id)
    Session.remove()

def delete_topic(topic_id):
    session = Session()
    session.execute(topics.delete().where(topics.c.topic_id == topic_id))
    session.commit()
    Session.remove()



# Update app function
def app():
    st.title("Configuration")
    menu = ["Sentiment", "Domain", "Topic"]
    choice = st.selectbox("Menu", menu)
    if choice == "Sentiment":
        add_sentiment()
        view_sentiments()
    elif choice == "Domain":
        add_domain()
        view_domains()
    elif choice == "Topic":
        add_topic()
        view_topic()
        
    # Add conditions for domains_self_dev and topics