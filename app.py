"""
app.py

Entry point for the Sustainable Lifestyle Calculator.

This file is responsible for launching the Streamlit application,
configuring the page settings, and managing navigation between
the different pages of the application. Navigation is controlled
using Streamlit's session state, allowing the application to
behave like a simple multi-page interface while keeping all
calculations and user data within a single session.
"""

import streamlit as st

from ui.intro import show_intro
from ui.input_page import show_input_page
from ui.results import show_results_page
from ui.dashboard import show_dashboard


# Configure the application's title,
# icon and page layout.
st.set_page_config(
    page_title="Sustainable Lifestyle Calculator",
    page_icon="🌱",
    layout="wide"
)

# Create the default landing page when
# the application is opened for the first time.
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Read the currently active page
# from the session state.
page = st.session_state.page

# Display the appropriate page
# based on the user's navigation.
if page == "intro":

    show_intro()

elif page == "input":

    show_input_page()

elif page == "results":

    show_results_page()

elif page == "dashboard":

    show_dashboard()