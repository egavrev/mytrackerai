import streamlit as st
import journal
import self_development
import summary

PAGES = {
    "Journal Entry": journal,
    "Self-Development Entry": self_development,
    "Summary": summary
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()