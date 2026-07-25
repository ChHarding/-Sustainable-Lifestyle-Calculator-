import streamlit as st

from data_manager import record_count
from ui.styles import load_styles


def show_intro():

    load_styles()

    # --------------------------------------------------
    # HERO
    # --------------------------------------------------

    st.caption("SUSTAINABLE LIFESTYLE CALCULATOR")

    st.title("🌱 Sustainable Lifestyle Calculator")

    st.markdown(
        """
### Turn everyday habits into a measurable impact score.

Track your transportation, energy usage, water consumption,
and waste management to receive a personalised Eco Score
and practical sustainability recommendations.
"""
    )

    st.divider()

    # --------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
### 🚗 Transportation

Measure how sustainable your
daily travel habits are.
"""
        )

    with col2:

        st.info(
            """
### ⚡ Energy

Track electricity,
water and household usage.
"""
        )

    with col3:

        st.info(
            """
### 🌱 Eco Score

Receive personalised
recommendations instantly.
"""
        )

    st.divider()

    # --------------------------------------------------
    # STATS
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.metric(
            "Saved Records",
            record_count()
        )

    with right:

        st.metric(
            "Maximum Eco Score",
            100
        )

    st.divider()

    # --------------------------------------------------
    # CALL TO ACTION
    # --------------------------------------------------

    st.subheader("Ready to calculate your Eco Score?")

    st.write(
        "Start by entering your daily sustainability habits."
    )

    primary, secondary = st.columns([2, 1])

    with primary:

        if st.button(
            "🌱 Calculate My Eco Score",
            use_container_width=True
        ):

            st.session_state.page = "input"
            st.rerun()

    with secondary:

        dashboard_disabled = record_count() == 0

        if st.button(
            "📊 View Dashboard",
            use_container_width=True,
            disabled=dashboard_disabled
        ):

            st.session_state.page = "dashboard"
            st.rerun()

    if dashboard_disabled:

        st.caption(
            "Dashboard will be available after your first Eco Score is calculated."
        )

    st.divider()

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.caption(
        "Designed to help you build sustainable daily habits through simple lifestyle tracking."
    )