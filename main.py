import streamlit as st
import journal
import self_dev
import summary
import config

PAGES = {
    "Journal": journal,
    "Self-Development": self_dev,
    "Summary": summary,
    "Configuration": config
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()