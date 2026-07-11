"""
app.py

Main Streamlit application for the
Sustainable Lifestyle Calculator.
"""

import streamlit as st

from calculator import (
    calculate_scores,
    calculate_eco_score,
    get_level,
    generate_feedback
)

from data_manager import (
    save_record,
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


# Streamlit Page Configuration

st.set_page_config(
    page_title="Sustainable Lifestyle Calculator",
    page_icon="🌱",
    layout="wide"
)


# Title

st.title("🌱 Sustainable Lifestyle Calculator")

st.write(
    """
Track your daily sustainability habits,
calculate your Eco Score,
and monitor your progress over time.
"""
)

st.divider()


# Sidebar

st.sidebar.header("About")

st.sidebar.info(
    """
This application calculates an Eco Score
based on transportation,
electricity usage,
water usage,
recycling habits,
and plastic consumption.
"""
)

st.sidebar.divider()

history = load_history()

st.sidebar.metric(
    "Saved Records",
    record_count()
)



# User Inputs


st.header("Daily Lifestyle Inputs")

col1, col2 = st.columns(2)


# Left Column 

with col1:

    st.subheader("Transportation")

    car = st.number_input(
        "Car Travel (km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    bike = st.number_input(
        "Motorcycle Travel (km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    bus = st.number_input(
        "Bus Travel (km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    cycle = st.number_input(
        "Bicycle Travel (km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    walk = st.number_input(
        "Walking Distance (km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )


# Right Column 

with col2:

    st.subheader("Utilities")

    electricity = st.number_input(
        "Electricity Usage (kWh)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    water = st.number_input(
        "Water Usage (Litres)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    recycling = st.selectbox(
        "Recycling Habit",

        [
            "Never",
            "Sometimes",
            "Often",
            "Always"
        ]
    )

    plastic = st.number_input(
        "Single-use Plastic Items",
        min_value=0,
        value=0,
        step=1
    )


# Calculate Button

calculate_button = st.button(
    "Calculate Eco Score",
    use_container_width=True
)

# Calculate Results

if calculate_button:

    # Store user inputs

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

    # Calculate scores

    category_scores = calculate_scores(user_data)

    eco_score = calculate_eco_score(category_scores)

    achievement_level = get_level(eco_score)

    feedback = generate_feedback(category_scores)

    # Save record

    save_record(

        user_data,

        category_scores,

        eco_score,

        achievement_level,

        feedback

    )

    st.success("Eco Score calculated and saved successfully!")

    st.divider()


    # Results

    st.header("Results")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(

        "Eco Score",

        eco_score

    )

    metric2.metric(

        "Achievement Level",

        achievement_level

    )

    metric3.metric(

        "Records Saved",

        record_count()

    )

    st.divider()

   
    # Category Scores


    st.subheader("Category Scores")

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(

            "Transport",

            round(category_scores[0], 2)

        )

        st.metric(

            "Electricity",

            category_scores[1]

        )

        st.metric(

            "Water",

            category_scores[2]

        )

    with score_col2:

        st.metric(

            "Recycling",

            category_scores[3]

        )

        st.metric(

            "Plastic",

            category_scores[4]

        )

    st.divider()

   
    # Recommendations

    st.subheader("Recommendations")

    for recommendation in feedback:

        st.success(recommendation)

    st.divider()


    # User Inputs Summary
    
    st.subheader("Today's Inputs")

    st.table({

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

            car,

            bike,

            bus,

            cycle,

            walk,

            electricity,

            water,

            recycling,

            plastic

        ]

    })

# Dashboard

history = load_history()

if len(history) > 0:

    st.header("Sustainability Dashboard")

    df = prepare_dataframe(history)

   
    # Historical Records
   
    st.subheader("Historical Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # Graph Selection

    st.subheader("Progress Graph")

    graph_options = [

        "Eco Score",
        "Transport Score",
        "Electricity Score",
        "Water Score",
        "Recycling Score",
        "Plastic Score"

    ]

    selected_metrics = st.multiselect(

        "Select metrics to display",

        graph_options,

        default=["Eco Score"]

    )

    if selected_metrics:

        fig = create_progress_graph(

            df,

            selected_metrics

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    
    # Weekly Average
    
    st.subheader("Weekly Moving Average")

    weekly_fig = create_weekly_average_graph(df)

    st.plotly_chart(

        weekly_fig,

        use_container_width=True

    )

    st.divider()

  
    # Monthly Average
    
    st.subheader("Monthly Moving Average")

    monthly_fig = create_monthly_average_graph(df)

    st.plotly_chart(

        monthly_fig,

        use_container_width=True

    )

    st.divider()

   
    # Goal Tracking

    st.subheader("Goal Tracking")

    goal = st.slider(

        "Select your Eco Score Goal",

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

    
    # Weekly Goal Summary
   
    st.subheader("Weekly Goal Summary")

    summary = calculate_goal_summary(

        df,

        goal

    )

    st.dataframe(

        summary,

        use_container_width=True

    )

    st.divider()

    
    # Trend Analysis
    

    st.subheader("Trend Analysis")

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

   
    # Latest Record
   

    st.subheader("Latest Entry")

    latest = df.iloc[-1]

    latest_table = {

        "Field": [

            "Date",

            "Eco Score",

            "Achievement Level",

            "Transport",

            "Electricity",

            "Water",

            "Recycling",

            "Plastic"

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

else:

    st.info("No historical data available. Calculate your first Eco Score to begin.")