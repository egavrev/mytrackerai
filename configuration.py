import streamlit as st
import sqlite3

# Establish a SQLite connection
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

def add_sentiment():
    st.subheader("Add a new sentiment")
    sentiment = st.text_input("Sentiment")
    icon = st.text_input("Icon")
    color = st.color_picker("Color")
    add_button = st.button("Add Sentiment")
    if add_button:
        c.execute('INSERT INTO sentiments(sentiment, icon, color) VALUES (?, ?, ?)',
                  (sentiment, icon, color))
        conn.commit()
        st.success("Successfully added a new sentiment")

def view_sentiments():
    st.subheader("View existing sentiments")
    result = c.execute('SELECT * FROM sentiments').fetchall()
    for i in result:
        st.write(i)

def delete_sentiment():
    st.subheader("Delete a sentiment")
    sentiment_list = [i[0] for i in c.execute('SELECT sentiment_id FROM sentiments')]
    selected_sentiment = st.selectbox("Select sentiment", sentiment_list)
    if st.button("Delete"):
        c.execute('DELETE FROM sentiments WHERE sentiment_id = ?', (selected_sentiment,))
        conn.commit()
        st.success("Sentiment deleted")

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