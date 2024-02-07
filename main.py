import streamlit as st
import journal


PAGES = {
    "Journal": journal
    #"Self Development": self_development,
    #"Summary": summary,
    #"Configuration": configuration
}

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[choice]

    with st.spinner(f"Loading {choice} ..."):
        page.app()

if __name__ == "__main__":
    main()