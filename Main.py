# Sustainable Lifestyle Calculator

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib is not installed.")
    print("Please run: pip install matplotlib")
    exit()


# Collect user input
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


# Calculate category scores
def calculate_scores(data):
    transport_score = (
        (data["car"] * -3) +
        (data["bike"] * -2) +
        (data["bus"] * -1) +
        (data["cycle"] * 1) +
        (data["walk"] * 1.5)
    )

    transport_score = max(0, min(100, transport_score + 50))

    # Electricity score
    if data["electricity"] <= 100:
        electricity_score = 100
    elif data["electricity"] <= 300:
        electricity_score = 70
    else:
        electricity_score = 40

    # Water score
    if data["water"] <= 100:
        water_score = 100
    elif data["water"] <= 300:
        water_score = 70
    else:
        water_score = 40

    # Recycling score
    recycling_scores = {
        "never": 20,
        "sometimes": 50,
        "often": 80,
        "always": 100
    }

    recycling_score = recycling_scores.get(data["recycling"], 20)

    # Plastic score
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


# Calculate final eco score
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


# Determine sustainability level
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


# Generate category-wise feedback
def generate_feedback(scores):
    feedback = []

    transport, electricity, water, recycling, plastic = scores

    # Transportation feedback
    if transport >= 80:
        feedback.append("Transportation: Excellent use of sustainable transport.")
    elif transport >= 50:
        feedback.append("Transportation: Moderate. Consider walking or cycling more.")
    else:
        feedback.append("Transportation: High carbon footprint. Reduce car usage.")

    # Electricity feedback
    if electricity >= 80:
        feedback.append("Electricity: Great energy efficiency.")
    elif electricity >= 50:
        feedback.append("Electricity: Moderate consumption.")
    else:
        feedback.append("Electricity: High energy usage. Save electricity where possible.")

    # Water feedback
    if water >= 80:
        feedback.append("Water: Excellent conservation habits.")
    elif water >= 50:
        feedback.append("Water: Moderate water consumption.")
    else:
        feedback.append("Water: High usage. Try conserving water.")

    # Recycling feedback
    if recycling >= 80:
        feedback.append("Recycling: Excellent recycling habits.")
    elif recycling >= 50:
        feedback.append("Recycling: Good, but there is room for improvement.")
    else:
        feedback.append("Recycling: Needs improvement.")

    # Plastic feedback
    if plastic >= 80:
        feedback.append("Plastic: Excellent reduction in plastic usage.")
    elif plastic >= 50:
        feedback.append("Plastic: Moderate usage.")
    else:
        feedback.append("Plastic: Reduce single-use plastics.")

    return feedback


# Plot weekly sustainability progress
def plot_progress(current_score):
    # Sample historical data (simulated weekly scores)
    weekly_scores = [42, 48, 53, 57, 60, 64, 68, 72, 75, current_score]
    weeks = list(range(1, 11))

    plt.plot(weeks, weekly_scores, marker='o')
    plt.xlabel("Week")
    plt.ylabel("Eco Score")
    plt.title("Weekly Sustainability Progress")
    plt.grid(True)
    plt.show()


def main():
    user_data = get_user_data()
    scores = calculate_scores(user_data)
    eco_score = calculate_eco_score(scores)
    level = get_level(eco_score)
    feedback = generate_feedback(scores)

    print("\n----- RESULTS -----")
    print("Eco Score:", eco_score)
    print("Achievement Level:", level)

    print("\nDetailed Feedback:")
    for item in feedback:
        print("-", item)

    plot_progress(eco_score)
main()