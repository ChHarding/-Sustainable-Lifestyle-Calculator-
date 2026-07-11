"""
calculator.py

Contains all score calculations for the Sustainable Lifestyle Calculator.
"""


# Calculate category scores

def calculate_scores(data):
    """
    Calculate all sustainability category scores.

    Args:
        data (dict): User lifestyle inputs.

    Returns:
        tuple: Transport, Electricity, Water,
               Recycling and Plastic scores.
    """

    transport_score = (
        (data["car"] * -3)
        + (data["bike"] * -2)
        + (data["bus"] * -1)
        + (data["cycle"] * 1)
        + (data["walk"] * 1.5)
    )

    transport_score = max(0, min(100, transport_score + 50))

    # Electricity Score

    if data["electricity"] <= 100:
        electricity_score = 100

    elif data["electricity"] <= 300:
        electricity_score = 70

    else:
        electricity_score = 40

    # Water Score

    if data["water"] <= 100:
        water_score = 100

    elif data["water"] <= 300:
        water_score = 70

    else:
        water_score = 40

    # Recycling Score

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

    # Plastic Score

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



# Eco Score

def calculate_eco_score(scores):
    """
    Calculate the overall Eco Score.

    Args:
        scores (tuple): Category scores.

    Returns:
        float: Eco Score.
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


# Achievement Level

def get_level(score):
    """
    Determine sustainability level.
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



# Feedback Generator

def generate_feedback(scores):
    """
    Generate personalised recommendations.
    """

    feedback = []

    transport, electricity, water, recycling, plastic = scores

    # Transport

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

    # Electricity

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

    # Water

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

    # Recycling

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

    # Plastic

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