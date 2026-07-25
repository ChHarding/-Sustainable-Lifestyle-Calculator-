import streamlit as st

from data_manager import load_history

from visualization import (
    prepare_dataframe,
    create_progress_graph
)

from ui.styles import load_styles


def show_results_page():

    load_styles()

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    if "eco_score" not in st.session_state:

        st.warning(
            "Please calculate your Eco Score first."
        )

        if st.button("← Back"):

            st.session_state.page = "input"

            st.rerun()

        return

    st.title("🌱 Your Sustainability Results")

    st.write(
        """
Review today's performance,
your overall Eco Score,
and recommendations for improvement.
"""
    )

    st.divider()

    # -----------------------------------------
    # Top Section
    # -----------------------------------------

    left, right = st.columns([1, 1.3])

    with left:

        st.metric(
            "Eco Score",
            st.session_state.eco_score
        )

        st.metric(
            "Achievement Level",
            st.session_state.achievement_level
        )

    with right:

        history = load_history()

        if len(history) > 0:

            df = prepare_dataframe(history)

            fig = create_progress_graph(
                df,
                ["Eco Score"]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # -----------------------------------------
    # Category Scores
    # -----------------------------------------

    st.subheader("Category Scores")

    transport, electricity, water, recycling, plastic = (
        st.session_state.category_scores
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(
            "🚗",
            round(transport, 1)
        )

    with c2:

        st.metric(
            "⚡",
            electricity
        )

    with c3:

        st.metric(
            "🚿",
            water
        )

    with c4:

        st.metric(
            "♻",
            recycling
        )

    with c5:

        st.metric(
            "🛍",
            plastic
        )

    st.divider()
    # -----------------------------------------
    # Achievement Guide
    # -----------------------------------------

    st.subheader("🏆 Achievement Level Guide")

    level1, level2, level3, level4, level5 = st.columns(5)

    with level1:

        st.success(
            """
**81–100**

Champion 🌱
"""
        )

    with level2:

        st.info(
            """
**61–80**

Eco-Friendly
"""
        )

    with level3:

        st.warning(
            """
**41–60**

Improving
"""
        )

    with level4:

        st.warning(
            """
**21–40**

Beginner
"""
        )

    with level5:

        st.error(
            """
**0–20**

Unsustainable
"""
        )

    st.divider()

    # -----------------------------------------
    # Recommendations
    # -----------------------------------------

    st.subheader("💡 Top Recommendations")

    st.write(
        """
Based on today's inputs,
here are some personalised suggestions.
"""
    )

    for recommendation in st.session_state.feedback:

        st.success(
            recommendation
        )

    st.divider()

    # -----------------------------------------
    # Today's Summary
    # -----------------------------------------

    st.subheader("📋 Today's Inputs")

    data = st.session_state.user_data

    summary = {

        "Category": [

            "Car",

            "Motorcycle",

            "Bus",

            "Bicycle",

            "Walking",

            "Electricity",

            "Water",

            "Recycling",

            "Plastic"

        ],

        "Value": [

            f"{data['car']} km",

            f"{data['bike']} km",

            f"{data['bus']} km",

            f"{data['cycle']} km",

            f"{data['walk']} km",

            f"{data['electricity']} kWh",

            f"{data['water']} Litres",

            data["recycling"].title(),

            data["plastic"]

        ]

    }

    st.table(summary)

    st.divider()
    # -----------------------------------------
    # Navigation
    # -----------------------------------------

    primary, secondary, tertiary = st.columns([2, 1.2, 1.2])

    # ----------------------------
    # Primary CTA
    # ----------------------------

    with primary:

        if st.button(
            "🏠 Go Home",
            use_container_width=True
        ):

            st.session_state.page = "intro"

            st.rerun()

    # ----------------------------
    # Secondary CTA
    # ----------------------------

    with secondary:

        if st.button(
            "📊 View Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    # ----------------------------
    # Tertiary CTA
    # ----------------------------

    with tertiary:

        if st.button(
            "🔄 Calculate Again",
            use_container_width=True
        ):

            st.session_state.page = "input"

            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "Your Eco Score is calculated using transportation, energy usage, water consumption, recycling habits and plastic consumption."
    )