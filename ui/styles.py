"""
styles.py

Contains the custom styling used throughout the application.

This file injects CSS into the Streamlit interface to provide
a more consistent visual appearance across all pages. The
styles customise the layout, colours, buttons, metric cards,
tables and other interface elements.
"""

import streamlit as st


def load_styles():
    """
    Apply the application's custom CSS styling.

    This function injects a shared stylesheet into the
    Streamlit application. It is called at the beginning
    of every page to ensure a consistent look and feel
    throughout the application.
    """

    st.markdown("""
<style>

/* -----------------------------
Main Layout
Controls the overall page width
and spacing.
----------------------------- */

.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* -----------------------------
Application Background
----------------------------- */

.stApp{
    background:#FAFCFA;
}

/* -----------------------------
Buttons
Styles all primary buttons used
throughout the application.
----------------------------- */

.stButton > button{

    width:100%;
    height:52px;

    background:#2E7D32 !important;

    color:white !important;

    border:none;

    border-radius:12px;

    font-weight:600;

    font-size:16px;

}

.stButton > button:hover{

    background:#256428 !important;

    color:white !important;

}

/* Ensure button text remains visible. */

.stButton > button p{

    color:white !important;

}

/* -----------------------------
Metric Cards
Customises the appearance of
Streamlit metric widgets.
----------------------------- */

[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5E7EB;

    border-radius:12px;

    padding:15px;

}

/* -----------------------------
Alert Messages
----------------------------- */

div[data-testid="stAlert"]{

    border-radius:12px;

}

/* -----------------------------
Data Tables
----------------------------- */

[data-testid="stDataFrame"]{

    border-radius:12px;

}

/* -----------------------------
Streamlit Branding
Hide default Streamlit menu
and footer for a cleaner UI.
----------------------------- */

footer{

    visibility:hidden;

}

#MainMenu{

    visibility:hidden;

}

</style>
""",
unsafe_allow_html=True)