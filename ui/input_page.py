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
    # Navigation Buttons
    # ----------------------------------------------------

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
    # Calculate Score
    # ----------------------------------------------------

    if calculate:

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

        # ------------------------------------------
        # Calculate Scores
        # ------------------------------------------

        category_scores = calculate_scores(user_data)

        eco_score = calculate_eco_score(
            category_scores
        )

        achievement_level = get_level(
            eco_score
        )

        feedback = generate_feedback(
            category_scores
        )

        # ------------------------------------------
        # Save Record
        # ------------------------------------------

        save_record(

            user_data,

            category_scores,

            eco_score,

            achievement_level,

            feedback

        )

        # ------------------------------------------
        # Store Values
        # ------------------------------------------

        st.session_state.user_data = user_data

        st.session_state.category_scores = category_scores

        st.session_state.eco_score = eco_score

        st.session_state.achievement_level = achievement_level

        st.session_state.feedback = feedback

        # ------------------------------------------
        # Navigate
        # ------------------------------------------

        st.session_state.page = "results"

        st.rerun()