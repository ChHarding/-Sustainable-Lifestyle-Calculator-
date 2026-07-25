import streamlit as st

from ui.intro import show_intro
from ui.input_page import show_input_page
from ui.results import show_results_page
from ui.dashboard import show_dashboard

st.set_page_config(
    page_title="Sustainable Lifestyle Calculator",
    page_icon="🌱",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "intro"

page = st.session_state.page

if page == "intro":
    show_intro()

elif page == "input":
    show_input_page()

elif page == "results":
    show_results_page()

elif page == "dashboard":
    show_dashboard()
    