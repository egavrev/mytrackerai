import streamlit as st
import sqlite3

# Establish a SQLite connection
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

def add_journal_entry():
    st.subheader("Add a new journal entry")
    date = st.date_input("Date")
    domain = st.text_input("Domain")
    sentiment = st.text_input("Sentiment")
    event_desc = st.text_area("Event Description")
    add_button = st.button("Add Journal Entry")
    if add_button:
        # Create a new connection
        conn = sqlite3.connect('sqlite.db')
        c = conn.cursor()

        # Use the connection
        c.execute('INSERT INTO journal(date, domain, sentiment, description) VALUES (?, ?, ?, ?)',
                  (date, domain, sentiment, event_desc))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        st.success("Successfully added a new journal entry")

def view_journal_entries():
    st.subheader("View journal entries")

    # Create a new connection
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()

    # Use the connection
    result = c.execute('SELECT * FROM journal ORDER BY date DESC').fetchall()
    for i in result:
        st.write(i)

    # Close the connection
    conn.close()

def delete_journal_entry():
    st.subheader("Delete a journal entry")

    # Create a new connection
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()

    # Use the connection
    entry_list = [i[0] for i in c.execute('SELECT entry_id FROM journal')]
    selected_entry = st.selectbox("Select entry", entry_list)
    if st.button("Delete"):
        c.execute('DELETE FROM journal WHERE entry_id = ?', (selected_entry,))
        conn.commit() 
        st.success("Entry deleted")

    # Close the connection
    conn.close()

def app():
    st.title("Journal")
    menu = ["Add", "View", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        add_journal_entry()
    elif choice == "View":
        view_journal_entries()
    elif choice == "Delete":
        delete_journal_entry()