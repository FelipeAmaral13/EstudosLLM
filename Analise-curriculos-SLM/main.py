import streamlit as st  
from src.views import home, resume_extract

PAGES = {
    "Home": home,
    "RAG Resume": resume_extract
}

selection = st.sidebar.radio("Ir para:", list(PAGES.keys()))
page = PAGES[selection]
page.show()
