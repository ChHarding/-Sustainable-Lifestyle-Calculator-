from ui.styles import load_styles

import streamlit as st

from data_manager import (
    load_history,
    record_count
)

from visualization import (
    prepare_dataframe,
    create_progress_graph,
    create_weekly_average_graph,
    create_monthly_average_graph,
    create_goal_graph,
    calculate_goal_summary,
    calculate_trend
)


def show_dashboard():
    load_styles()
    st.title("📊 Sustainability Dashboard")

    st.write(
        """
Track your sustainability journey,
monitor your progress over time,
and review your historical performance.
"""
    )

    history = load_history()

    if len(history) == 0:

        st.info(
            "No historical data available yet."
        )

        if st.button(
            "🏠 Back Home",
            use_container_width=True
        ):

            st.session_state.page = "intro"

            st.rerun()

        return

    df = prepare_dataframe(history)

    latest = df.iloc[-1]

    st.divider()

    # ----------------------------------------------------
    # Dashboard Summary
    # ----------------------------------------------------

    st.subheader("Overview")

    card1, card2, card3 = st.columns(3)

    with card1:

        st.metric(
            "Current Eco Score",
            latest["Eco Score"]
        )

    with card2:

        st.metric(
            "Records Saved",
            record_count()
        )

    with card3:

        trend = calculate_trend(df)

        st.metric(
            "Current Trend",
            trend
        )

    st.divider()
    # ----------------------------------------------------
    # Progress Over Time
    # ----------------------------------------------------

    st.subheader("📈 Progress Over Time")

    progress_fig = create_progress_graph(
        df,
        ["Eco Score"]
    )

    st.plotly_chart(
        progress_fig,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Weekly Average
    # ----------------------------------------------------

    st.subheader("📅 Weekly Moving Average")

    weekly_fig = create_weekly_average_graph(df)

    st.plotly_chart(
        weekly_fig,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Monthly Average
    # ----------------------------------------------------

    st.subheader("📆 Monthly Moving Average")

    monthly_fig = create_monthly_average_graph(df)

    st.plotly_chart(
        monthly_fig,
        use_container_width=True
    )

    st.divider()
    # ----------------------------------------------------
    # Goal Tracking
    # ----------------------------------------------------

    st.subheader("🎯 Goal Tracking")

    st.write(
        "Choose your target Eco Score and compare it with your progress."
    )

    goal = st.slider(
        "Target Eco Score",
        min_value=0,
        max_value=100,
        value=75
    )

    goal_fig = create_goal_graph(
        df,
        goal
    )

    st.plotly_chart(
        goal_fig,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Weekly Goal Summary
    # ----------------------------------------------------

    st.subheader("📊 Weekly Goal Summary")

    summary = calculate_goal_summary(
        df,
        goal
    )

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Trend Analysis
    # ----------------------------------------------------

    st.subheader("📈 Trend Analysis")

    trend = calculate_trend(df)

    if trend == "Improving 📈":

        st.success(trend)

    elif trend == "Declining 📉":

        st.error(trend)

    elif trend == "Stable ➡":

        st.info(trend)

    else:

        st.warning(trend)

    st.divider()
    # ----------------------------------------------------
    # Historical Records
    # ----------------------------------------------------

    st.subheader("📜 Historical Records")

    st.write(
        "Review all previously saved sustainability records."
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Latest Entry
    # ----------------------------------------------------

    st.subheader("📋 Latest Entry")

    latest_table = {

        "Field": [

            "Date",
            "Eco Score",
            "Achievement Level",
            "Transport Score",
            "Electricity Score",
            "Water Score",
            "Recycling Score",
            "Plastic Score"

        ],

        "Value": [

            latest["Date"],
            latest["Eco Score"],
            latest["Achievement Level"],
            latest["Transport Score"],
            latest["Electricity Score"],
            latest["Water Score"],
            latest["Recycling Score"],
            latest["Plastic Score"]

        ]

    }

    st.table(latest_table)

    st.divider()

    # ----------------------------------------------------
    # Navigation
    # ----------------------------------------------------

    left, middle, right = st.columns(3)

    with left:

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.session_state.page = "intro"

            st.rerun()

    with middle:

        if st.button(
            "🌱 Calculate Again",
            use_container_width=True
        ):

            st.session_state.page = "input"

            st.rerun()

    with right:

        if st.button(
            "📊 Results",
            use_container_width=True
        ):

            if "eco_score" in st.session_state:

                st.session_state.page = "results"

            else:

                st.warning(
                    "Please calculate your Eco Score first."
                )

            st.rerun()