"""
calculator.py

Contains the scoring logic for the Sustainable Lifestyle Calculator.

This module converts a user's daily lifestyle habits into individual
sustainability category scores and combines them to calculate the
overall Eco Score. It also determines the user's achievement level
and generates personalised recommendations based on the calculated
results.
"""


def calculate_scores(data):
    """
    Calculate the sustainability score for each category.

    The user's lifestyle inputs are converted into individual
    scores for transportation, electricity usage, water
    consumption, recycling habits and plastic usage.

    Args:
        data (dict):
            Dictionary containing the user's lifestyle inputs.

    Returns:
        tuple:
            Transport, Electricity, Water, Recycling and
            Plastic scores, each ranging from 0 to 100.
    """

    # ----------------------------------------------------
    # Transportation Score
    # ----------------------------------------------------
    # Different modes of transport contribute differently
    # to the sustainability score. Walking and cycling
    # increase the score, while motorised transport
    # reduces it.

    transport_score = (
        (data["car"] * -3)
        + (data["bike"] * -2)
        + (data["bus"] * -1)
        + (data["cycle"] * 1)
        + (data["walk"] * 1.5)
    )

    # Keep the transport score within the valid range.
    transport_score = max(0, min(100, transport_score + 50))

    # ----------------------------------------------------
    # Electricity Score
    # ----------------------------------------------------
    # Lower electricity consumption results
    # in a higher sustainability score.

    if data["electricity"] <= 100:
        electricity_score = 100

    elif data["electricity"] <= 300:
        electricity_score = 70

    else:
        electricity_score = 40

    # ----------------------------------------------------
    # Water Score
    # ----------------------------------------------------
    # Lower daily water usage is rewarded
    # with a higher sustainability score.

    if data["water"] <= 100:
        water_score = 100

    elif data["water"] <= 300:
        water_score = 70

    else:
        water_score = 40

    # ----------------------------------------------------
    # Recycling Score
    # ----------------------------------------------------
    # Convert the user's recycling habit into
    # a predefined sustainability score.

    recycling_scores = {

        "never": 20,
        "sometimes": 50,
        "often": 80,
        "always": 100

    }

    recycling_score = recycling_scores.get(
        data["recycling"].lower(),
        20
    )

    # ----------------------------------------------------
    # Plastic Usage Score
    # ----------------------------------------------------
    # Fewer single-use plastic items result
    # in a higher sustainability score.

    if data["plastic"] <= 2:
        plastic_score = 100

    elif data["plastic"] <= 5:
        plastic_score = 70

    else:
        plastic_score = 30

    return (

        transport_score,
        electricity_score,
        water_score,
        recycling_score,
        plastic_score

    )


def calculate_eco_score(scores):
    """
    Calculate the overall Eco Score.

    The Eco Score is calculated using a weighted average
    of all five sustainability categories. Transportation
    contributes the largest proportion of the final score.

    Args:
        scores (tuple):
            The category scores returned by
            calculate_scores().

    Returns:
        float:
            Final Eco Score between 0 and 100.
    """

    transport, electricity, water, recycling, plastic = scores

    eco_score = (

        transport * 0.30
        + electricity * 0.20
        + water * 0.15
        + recycling * 0.20
        + plastic * 0.15

    )

    return round(eco_score, 2)


def get_level(score):
    """
    Determine the user's sustainability achievement level.

    The achievement level is based on the final Eco Score
    and is used throughout the application to provide
    meaningful feedback to the user.

    Args:
        score (float):
            Final Eco Score.

    Returns:
        str:
            Achievement level corresponding to the Eco Score.
    """

    if score <= 20:
        return "Unsustainable"

    elif score <= 40:
        return "Beginner"

    elif score <= 60:
        return "Improving"

    elif score <= 80:
        return "Eco-Friendly"

    else:
        return "Sustainability Champion"


def generate_feedback(scores):
    """
    Generate personalised sustainability recommendations.

    Recommendations are created by evaluating the user's
    performance in each sustainability category. Every
    category contributes one suggestion to help users
    understand their strengths and identify areas for
    improvement.

    Args:
        scores (tuple):
            Category scores returned by calculate_scores().

    Returns:
        list:
            A list of personalised sustainability
            recommendations.
    """

    feedback = []

    transport, electricity, water, recycling, plastic = scores

    # ----------------------------------------------------
    # Transportation Feedback
    # ----------------------------------------------------

    if transport >= 80:

        feedback.append(
            "Excellent use of sustainable transport."
        )

    elif transport >= 50:

        feedback.append(
            "Walk or cycle more to improve transport sustainability."
        )

    else:

        feedback.append(
            "Reduce private vehicle usage."
        )

    # ----------------------------------------------------
    # Electricity Feedback
    # ----------------------------------------------------

    if electricity >= 80:

        feedback.append(
            "Excellent energy efficiency."
        )

    elif electricity >= 50:

        feedback.append(
            "Try reducing electricity consumption."
        )

    else:

        feedback.append(
            "Electricity usage is high."
        )

    # ----------------------------------------------------
    # Water Feedback
    # ----------------------------------------------------

    if water >= 80:

        feedback.append(
            "Excellent water conservation."
        )

    elif water >= 50:

        feedback.append(
            "Reduce daily water usage."
        )

    else:

        feedback.append(
            "Water consumption is high."
        )

    # ----------------------------------------------------
    # Recycling Feedback
    # ----------------------------------------------------

    if recycling >= 80:

        feedback.append(
            "Excellent recycling habits."
        )

    elif recycling >= 50:

        feedback.append(
            "Recycle more frequently."
        )

    else:

        feedback.append(
            "Improve recycling habits."
        )

    # ----------------------------------------------------
    # Plastic Usage Feedback
    # ----------------------------------------------------

    if plastic >= 80:

        feedback.append(
            "Low single-use plastic consumption."
        )

    elif plastic >= 50:

        feedback.append(
            "Reduce plastic usage further."
        )

    else:

        feedback.append(
            "Avoid single-use plastics."
        )

    return feedback