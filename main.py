import streamlit as st
import journal
import journal_df
import self_development
import summary
import configuration


PAGES = {
    "Journal": journal,
    "Journal_df": journal_df,
    "Self Development": self_development,
    "Summary": summary,
    "Configuration": configuration
}

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[choice]

    with st.spinner(f"Loading {choice} ..."):
        page.app()

if __name__ == "__main__":
    main()