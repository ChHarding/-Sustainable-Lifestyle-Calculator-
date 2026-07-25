import streamlit as st


def load_styles():

    st.markdown("""
<style>

/* -----------------------------
Main Layout
----------------------------- */

.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* -----------------------------
Background
----------------------------- */

.stApp{
    background:#FAFCFA;
}

/* -----------------------------
Buttons
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

/* Force white text */

.stButton > button p{

    color:white !important;

}

/* -----------------------------
Metrics
----------------------------- */

[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5E7EB;

    border-radius:12px;

    padding:15px;

}

/* -----------------------------
Alerts
----------------------------- */

div[data-testid="stAlert"]{

    border-radius:12px;

}

/* -----------------------------
Dataframe
----------------------------- */

[data-testid="stDataFrame"]{

    border-radius:12px;

}

/* -----------------------------
Hide Streamlit Footer
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