# Sustainable Lifestyle Calculator
# Version 1 - CLI App


# This function collects all user input
def get_user_data():
    print("Welcome to Sustainable Lifestyle Calculator")
    print("------------------------------------------")

    car_km = float(input("Enter car travel distance (km): "))
    bike_km = float(input("Enter motorcycle travel distance (km): "))
    bus_km = float(input("Enter bus travel distance (km): "))
    cycle_km = float(input("Enter bicycle travel distance (km): "))
    walk_km = float(input("Enter walking distance (km): "))

    electricity = float(input("Enter electricity usage (kWh): "))
    water = float(input("Enter water usage (liters/day): "))

    print("\nRecycling habits: Never / Sometimes / Often / Always")
    recycling = input("Enter recycling habit: ").lower()

    plastic = int(input("Number of single-use plastic items used: "))

    # Return everything in dictionary for easier access
    return {
        "car": car_km,
        "bike": bike_km,
        "bus": bus_km,
        "cycle": cycle_km,
        "walk": walk_km,
        "electricity": electricity,
        "water": water,
        "recycling": recycling,
        "plastic": plastic
    }


# Calculates score for each category
def calculate_scores(data):

    # Transportation score based on impact values
    transport_score = (
        (data["car"] * -3) +
        (data["bike"] * -2) +
        (data["bus"] * -1) +
        (data["cycle"] * 1) +
        (data["walk"] * 1.5)
    )

    # Limit transport score between 0 and 100
    transport_score = max(0, min(100, transport_score + 50))

    # Electricity scoring
    if data["electricity"] <= 100:
        electricity_score = 100
    elif data["electricity"] <= 300:
        electricity_score = 70
    else:
        electricity_score = 40

    # Water scoring
    if data["water"] <= 100:
        water_score = 100
    elif data["water"] <= 300:
        water_score = 70
    else:
        water_score = 40

    # Recycling scoring
    recycling_scores = {
        "never": 20,
        "sometimes": 50,
        "often": 80,
        "always": 100
    }

    recycling_score = recycling_scores.get(data["recycling"], 20)

    # Plastic scoring
    if data["plastic"] <= 2:
        plastic_score = 100
    elif data["plastic"] <= 5:
        plastic_score = 70
    else:
        plastic_score = 30

    return transport_score, electricity_score, water_score, recycling_score, plastic_score


# Combines category scores into final eco score
def calculate_eco_score(scores):
    transport, electricity, water, recycling, plastic = scores

    eco_score = (
        transport * 0.30 +
        electricity * 0.20 +
        water * 0.15 +
        recycling * 0.20 +
        plastic * 0.15
    )

    return round(eco_score, 2)


# Determines achievement level
def get_level(score):
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


# Generates recommendation text
def generate_feedback(score, plastic, recycling):
    feedback = []

    if plastic > 5:
        feedback.append("Try reducing single-use plastic usage.")

    if recycling in ["never", "sometimes"]:
        feedback.append("Improving recycling habits can boost your score.")

    if score > 80:
        feedback.append("Excellent work! Keep maintaining these habits.")

    if len(feedback) == 0:
        feedback.append("Good progress. Small improvements can help further.")

    return " ".join(feedback)


def main():
    user_data = get_user_data()

    scores = calculate_scores(user_data)

    eco_score = calculate_eco_score(scores)

    level = get_level(eco_score)

    feedback = generate_feedback(
        eco_score,
        user_data["plastic"],
        user_data["recycling"]
    )

    print("\n----- RESULTS -----")
    print("Eco Score:", eco_score)
    print("Achievement Level:", level)
    print("Feedback:", feedback)


main()