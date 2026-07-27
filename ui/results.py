"""
results.py

Displays the Sustainability Results page.

After the user completes a sustainability assessment,
this page presents the calculated Eco Score, achievement
level, category-wise scores, personalised recommendations,
and a summary of the user's inputs. It also provides a
quick overview of the user's historical progress and
navigation to other parts of the application.
"""

import streamlit as st

from data_manager import load_history

from visualization import (
    prepare_dataframe,
    create_progress_graph
)

from ui.styles import load_styles


def show_results_page():
    """
    Display the Sustainability Results page.

    This page retrieves the latest sustainability
    calculation stored in the session state and
    presents it to the user. It also visualises
    previous Eco Scores, highlights the user's
    achievement level, provides personalised
    recommendations, and summarises the submitted
    sustainability data.
    """

    # Apply the application's shared styling.
    load_styles()

    # --------------------------------------------------
    # Validate Session Data
    # --------------------------------------------------
    # Prevent users from accessing this page
    # before completing a sustainability assessment.

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

    # --------------------------------------------------
    # Results Overview
    # --------------------------------------------------
    # Display the user's latest Eco Score,
    # achievement level and historical progress.

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

        # Display the progress graph only if
        # historical records are available.
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

    # --------------------------------------------------
    # Category Scores
    # --------------------------------------------------
    # Show the individual sustainability
    # scores that contribute to the final
    # Eco Score.

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

    # --------------------------------------------------
    # Achievement Guide
    # --------------------------------------------------
    # Provide a quick reference explaining
    # what each Eco Score range represents.

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

    # --------------------------------------------------
    # Personalised Recommendations
    # --------------------------------------------------
    # Display suggestions generated from
    # the user's category scores.

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

    # --------------------------------------------------
    # Today's Sustainability Summary
    # --------------------------------------------------
    # Present the values entered by the user
    # during the current assessment.

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

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------
    # Allow the user to continue exploring
    # the application after reviewing their results.

    primary, secondary, tertiary = st.columns([2, 1.2, 1.2])

    with primary:

        if st.button(
            "🏠 Go Home",
            use_container_width=True
        ):

            st.session_state.page = "intro"
            st.rerun()

    with secondary:

        if st.button(
            "📊 View Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"
            st.rerun()

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