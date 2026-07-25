"""
intro.py

Displays the application's landing page.

This is the first page users see when they launch the
Sustainable Lifestyle Calculator. It provides a brief
introduction to the application, highlights its main
features, and guides users to either calculate their
first Eco Score or view their previous results in the
dashboard.
"""

import streamlit as st

from data_manager import record_count
from ui.styles import load_styles


def show_intro():
    """
    Display the application's introduction page.

    This page introduces the purpose of the Sustainable
    Lifestyle Calculator, provides a brief overview of
    its main features, and allows users to either begin
    a new sustainability assessment or access the
    dashboard if previous records are available.
    """

    # Apply the application's shared styling.
    load_styles()

    # --------------------------------------------------
    # Hero Section
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
    # Feature Overview
    # --------------------------------------------------
    # Introduce the three main areas of the application
    # before the user begins the assessment.

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
    # Quick Statistics
    # --------------------------------------------------
    # Display a summary of the user's saved records
    # along with the maximum possible Eco Score.

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
    # Navigation
    # --------------------------------------------------
    # Guide the user to either begin a new calculation
    # or open the dashboard if historical data exists.

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

    # Inform the user why the dashboard
    # is currently unavailable.
    if dashboard_disabled:

        st.caption(
            "Dashboard will be available after your first Eco Score is calculated."
        )

    st.divider()

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    st.caption(
        "Designed to help you build sustainable daily habits through simple lifestyle tracking."
    )