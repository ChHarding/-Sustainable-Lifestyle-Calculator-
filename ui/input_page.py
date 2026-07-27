"""
input_page.py

Displays the Sustainability Data input page.

This page collects the user's daily lifestyle habits, including
transportation, energy usage, water consumption and waste management.
After the user submits the form, the application calculates the
category scores, determines the overall Eco Score, saves the result,
and redirects the user to the Results page.
"""

import streamlit as st

from calculator import (
    calculate_scores,
    calculate_eco_score,
    get_level,
    generate_feedback
)

from data_manager import save_record

from ui.styles import load_styles


def show_input_page():
    """
    Display the Sustainability Data input form.

    This function allows users to enter their daily sustainability
    habits and calculates their Eco Score based on the submitted data.
    The calculated results are stored in the session state so they
    can be accessed by the Results and Dashboard pages.
    """

    # Apply the application's shared styling.
    load_styles()

    st.title("🌱 Enter Your Sustainability Data")

    st.write(
        """
Complete the information below to calculate your
personal Sustainability Score.
"""
    )

    st.divider()

    # ----------------------------------------------------
    # Transportation
    # ----------------------------------------------------
    # Collect the user's daily travel distances
    # across different modes of transportation.

    st.subheader("🚗 Transportation")

    col1, col2 = st.columns(2)

    with col1:

        car = st.number_input(
            "Car (km)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

        bike = st.number_input(
            "Motorcycle (km)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

        bus = st.number_input(
            "Bus (km)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    with col2:

        cycle = st.number_input(
            "Bicycle (km)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

        walk = st.number_input(
            "Walking (km)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    st.divider()

    # ----------------------------------------------------
    # Energy & Resources
    # ----------------------------------------------------
    # Collect household electricity and
    # water consumption values.

    st.subheader("⚡ Energy & Resources")

    energy1, energy2 = st.columns(2)

    with energy1:

        st.caption(
            "Average household electricity usage is approximately 10–12 kWh/day."
        )

        electricity = st.number_input(
            "Electricity (kWh)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    with energy2:

        st.caption(
            "Average daily water usage is approximately 150 litres per person."
        )

        water = st.number_input(
            "Water (Litres)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    st.divider()

    # ----------------------------------------------------
    # Waste Management
    # ----------------------------------------------------
    # Record recycling habits and the
    # use of single-use plastic items.

    st.subheader("♻ Waste Management")

    waste1, waste2 = st.columns(2)

    with waste1:

        recycling = st.selectbox(
            "Recycling Habit",
            [
                "Never",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

    with waste2:

        plastic = st.number_input(
            "Single-use Plastic Items",
            min_value=0,
            value=0,
            step=1
        )

    st.divider()

    # ----------------------------------------------------
    # Navigation
    # ----------------------------------------------------
    # Allow the user to either return to
    # the home page or calculate their Eco Score.

    left, right = st.columns([1, 2])

    with left:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.page = "intro"
            st.rerun()

    with right:

        calculate = st.button(
            "🌱 Calculate Eco Score",
            use_container_width=True
        )

    # ----------------------------------------------------
    # Process User Input
    # ----------------------------------------------------

    if calculate:

        # Organise all user inputs into a single
        # dictionary before sending them to
        # the scoring functions.

        user_data = {

            "car": car,
            "bike": bike,
            "bus": bus,
            "cycle": cycle,
            "walk": walk,

            "electricity": electricity,
            "water": water,

            "recycling": recycling.lower(),
            "plastic": plastic

        }

        # Calculate the sustainability score
        # for each individual category.

        category_scores = calculate_scores(
            user_data
        )

        # Combine the category scores to
        # calculate the final Eco Score.

        eco_score = calculate_eco_score(
            category_scores
        )

        # Determine the user's achievement level
        # based on the final Eco Score.

        achievement_level = get_level(
            eco_score
        )

        # Generate personalised sustainability
        # recommendations using the category scores.

        feedback = generate_feedback(
            category_scores
        )

        # Save the completed calculation so it can
        # be viewed later in the dashboard.

        save_record(

            user_data,

            category_scores,

            eco_score,

            achievement_level,

            feedback

        )

        # Store the latest calculation in the
        # session state so it can be accessed
        # across multiple pages.

        st.session_state.user_data = user_data

        st.session_state.category_scores = category_scores

        st.session_state.eco_score = eco_score

        st.session_state.achievement_level = achievement_level

        st.session_state.feedback = feedback

        # Navigate to the Results page to display
        # the newly calculated sustainability score.

        st.session_state.page = "results"

        st.rerun()