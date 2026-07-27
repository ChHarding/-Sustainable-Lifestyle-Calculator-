"""
visualization.py

Creates the charts and analytics used by the
Sustainable Lifestyle Calculator.

This module converts historical sustainability records
into interactive visualisations that help users monitor
their Eco Score over time. It also provides helper
functions for calculating trends, moving averages and
goal tracking statistics displayed in the dashboard.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def prepare_dataframe(history):
    """
    Convert saved sustainability records into a pandas DataFrame.

    The records loaded from the CSV file are converted into
    a DataFrame so they can be analysed and visualised.
    Numeric columns are converted to the appropriate data
    type and the date column is parsed as a datetime object.

    Args:
        history (list):
            Sustainability records loaded from the CSV file.

    Returns:
        pandas.DataFrame:
            A cleaned DataFrame ready for analysis and
            visualisation.
    """

    if len(history) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(history)

    numeric_columns = [

        "Transport Score",
        "Electricity Score",
        "Water Score",
        "Recycling Score",
        "Plastic Score",
        "Eco Score"

    ]

    # Convert score columns to numeric values
    # so mathematical operations can be performed.
    for column in numeric_columns:

        df[column] = pd.to_numeric(df[column])

    # Convert the saved date into
    # a pandas datetime object.
    df["Date"] = pd.to_datetime(df["Date"])

    return df


def create_progress_graph(df, selected_metrics):
    """
    Create an interactive progress chart.

    The graph displays one or more sustainability
    metrics across time, allowing users to monitor
    changes in their Eco Score and related values.

    Args:
        df (DataFrame):
            Prepared sustainability data.

        selected_metrics (list):
            List of metrics to display.

    Returns:
        plotly.graph_objects.Figure:
            Interactive progress chart.
    """

    fig = go.Figure()

    # Add one line for each
    # selected sustainability metric.
    for metric in selected_metrics:

        fig.add_trace(

            go.Scatter(

                x=df["Date"],
                y=df[metric],
                mode="lines+markers",
                name=metric

            )

        )

    fig.update_layout(

        title="Progress Over Time",

        xaxis_title="Date",

        yaxis_title="Score",

        hovermode="x unified",

        template="plotly_white"

    )

    return fig


def create_weekly_average_graph(df):
    """
    Create a weekly moving average graph.

    The moving average smooths daily fluctuations
    and helps users identify short-term trends in
    their sustainability performance.

    Args:
        df (DataFrame):
            Prepared sustainability data.

    Returns:
        plotly.graph_objects.Figure:
            Weekly moving average chart.
    """

    weekly = df.copy()

    weekly["Weekly Average"] = (

        weekly["Eco Score"]

        .rolling(window=7, min_periods=1)

        .mean()

    )

    fig = px.line(

        weekly,

        x="Date",

        y=[

            "Eco Score",
            "Weekly Average"

        ],

        title="Weekly Moving Average"

    )

    fig.update_traces(mode="lines+markers")

    fig.update_layout(template="plotly_white")

    return fig


def create_monthly_average_graph(df):
    """
    Create a monthly moving average graph.

    This graph highlights longer-term sustainability
    trends by averaging Eco Scores over a 30-day period.

    Args:
        df (DataFrame):
            Prepared sustainability data.

    Returns:
        plotly.graph_objects.Figure:
            Monthly moving average chart.
    """

    monthly = df.copy()

    monthly["Monthly Average"] = (

        monthly["Eco Score"]

        .rolling(window=30, min_periods=1)

        .mean()

    )

    fig = px.line(

        monthly,

        x="Date",

        y=[

            "Eco Score",
            "Monthly Average"

        ],

        title="Monthly Moving Average"

    )

    fig.update_traces(mode="lines+markers")

    fig.update_layout(template="plotly_white")

    return fig


def create_goal_graph(df, goal):
    """
    Create an Eco Score goal tracking graph.

    The graph compares the user's Eco Score against
    a target value selected within the dashboard.

    Args:
        df (DataFrame):
            Prepared sustainability data.

        goal (int):
            User-selected target Eco Score.

    Returns:
        plotly.graph_objects.Figure:
            Goal tracking chart.
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["Eco Score"],

            mode="lines+markers",

            name="Eco Score"

        )

    )

    # Display the user's selected
    # target Eco Score as a reference line.
    fig.add_hline(

        y=goal,

        line_dash="dash",

        line_color="royalblue",

        annotation_text="Goal"

    )

    fig.update_layout(

        title="Eco Score vs Goal"

    )

    return fig


def calculate_goal_summary(df, goal):
    """
    Calculate weekly goal achievement statistics.

    For each calendar week, determine how many
    recorded Eco Scores were above or below the
    selected target.

    Args:
        df (DataFrame):
            Prepared sustainability data.

        goal (int):
            User-selected target Eco Score.

    Returns:
        pandas.DataFrame:
            Weekly summary of goal achievements.
    """

    temp = df.copy()

    temp["Above Goal"] = temp["Eco Score"] >= goal

    temp["Week"] = (

        temp["Date"]

        .dt.isocalendar()

        .week

    )

    summary = (

        temp

        .groupby("Week")["Above Goal"]

        .agg(

            Above=lambda x: x.sum(),

            Below=lambda x: (~x).sum()

        )

        .reset_index()

    )

    return summary


def calculate_trend(df):
    """
    Analyse the user's recent sustainability trend.

    The average Eco Score from the most recent seven
    records is compared with the previous seven records
    to determine whether the user's sustainability
    performance is improving, declining or remaining stable.

    Args:
        df (DataFrame):
            Prepared sustainability data.

    Returns:
        str:
            A short description of the current trend.
    """

    # At least two weeks of history are required
    # for a meaningful comparison.
    if len(df) < 14:

        return "Not enough data."

    recent = (

        df["Eco Score"]

        .tail(7)

        .mean()

    )

    previous = (

        df["Eco Score"]

        .iloc[-14:-7]

        .mean()

    )

    if recent > previous:

        return "Improving 📈"

    elif recent < previous:

        return "Declining 📉"

    else:

        return "Stable ➡"