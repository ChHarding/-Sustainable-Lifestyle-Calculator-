"""
visualization.py

Contains all graph and analytics functions for the
Sustainable Lifestyle Calculator.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Prepare Data

def prepare_dataframe(history):
    """
    Convert CSV history into a clean pandas DataFrame.

    Args:
        history (list): Records loaded from CSV.

    Returns:
        DataFrame
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

    for column in numeric_columns:

        df[column] = pd.to_numeric(df[column])

    df["Date"] = pd.to_datetime(df["Date"])

    return df


# Interactive Graph

def create_progress_graph(df, selected_metrics):
    """
    Create interactive Plotly graph.
    """

    fig = go.Figure()

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

        hovermode="x unified"

    )

    return fig


# Weekly Moving Average

def create_weekly_average_graph(df):
    """
    Create weekly moving average graph.
    """

    weekly = df.copy()

    weekly["Weekly Average"] = (

        weekly["Eco Score"]

        .rolling(window=7)

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

    return fig


# Monthly Moving Average

def create_monthly_average_graph(df):
    """
    Create monthly moving average graph.
    """

    monthly = df.copy()

    monthly["Monthly Average"] = (

        monthly["Eco Score"]

        .rolling(window=30)

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

    return fig


# Goal Graph

def create_goal_graph(df, goal):
    """
    Create graph with user goal line.
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

    fig.add_hline(

        y=goal,

        line_dash="dash",

        annotation_text="Goal"

    )

    fig.update_layout(

        title="Eco Score vs Goal"

    )

    return fig


# Weekly Goal Analysis


def calculate_goal_summary(df, goal):
    """
    Calculate weekly above/below goal counts.
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


# Trend Analysis

def calculate_trend(df):
    """
    Determine whether Eco Score is improving,
    declining or stable.
    """

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