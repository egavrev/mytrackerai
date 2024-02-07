import streamlit as st
import sqlite3

# Establish a SQLite connection
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

def add_self_dev_entry():
    st.subheader("Add a new self development entry")
    date = st.date_input("Date")
    domain = st.text_input("Domain")
    topic = st.text_input("Topic")
    duration = st.select_slider("Duration", options=range(15, 121, 15))
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Self Development Entry")
    if add_button:
        c.execute('INSERT INTO self_dev(date, domain, topic, duration, description) VALUES (?, ?, ?, ?, ?)',
                  (date, domain, topic, duration, event_desc))
        conn.commit()
        st.success("Successfully added a new self development entry")

def view_self_dev_entries():
    st.subheader("View self development entries")
    result = c.execute('SELECT * FROM self_dev ORDER BY date DESC').fetchall()
    for i in result:
        st.write(i)

def delete_self_dev_entry():
    st.subheader("Delete a self development entry")
    entry_list = [i[0] for i in c.execute('SELECT entry_id FROM self_dev')]
    selected_entry = st.selectbox("Select entry", entry_list)
    if st.button("Delete"):
        c.execute('DELETE FROM self_dev WHERE entry_id = ?', (selected_entry,))
        conn.commit()
        st.success("Entry deleted")

def app():
    st.title("Self Development")
    menu = ["Add", "View", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        add_self_dev_entry()
    elif choice == "View":
        view_self_dev_entries()
    elif choice == "Delete":
        delete_self_dev_entry()