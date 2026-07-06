# Sustainable Lifestyle Calculator
# Version 1 CLI

import csv
import os

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib is not installed.")
    print("Please run: pip install matplotlib")
    exit()


# Collect validated positive float input
def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


# Collect validated positive integer input
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Please enter a valid integer.")


# Collect user input
def get_user_data():
    print("\nWelcome to Sustainable Lifestyle Calculator")
    print("------------------------------------------")

    car_km = get_positive_float("Enter car travel distance (km): ")
    bike_km = get_positive_float("Enter motorcycle travel distance (km): ")
    bus_km = get_positive_float("Enter bus travel distance (km): ")
    cycle_km = get_positive_float("Enter bicycle travel distance (km): ")
    walk_km = get_positive_float("Enter walking distance (km): ")

    electricity = get_positive_float("Enter electricity usage (kWh): ")
    water = get_positive_float("Enter water usage (liters/day): ")

    print("\nRecycling habits: Never / Sometimes / Often / Always")
    recycling = input("Enter recycling habit: ").lower()

    plastic = get_positive_int("Number of single-use plastic items used: ")

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

    if data["electricity"] <= 100:
        electricity_score = 100
    elif data["electricity"] <= 300:
        electricity_score = 70
    else:
        electricity_score = 40

    if data["water"] <= 100:
        water_score = 100
    elif data["water"] <= 300:
        water_score = 70
    else:
        water_score = 40

    recycling_scores = {
        "never": 20,
        "sometimes": 50,
        "often": 80,
        "always": 100
    }

    recycling_score = recycling_scores.get(data["recycling"], 20)

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


# Determine level
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


# Generate category feedback
def generate_feedback(scores):
    feedback = []
    transport, electricity, water, recycling, plastic = scores

    if transport >= 80:
        feedback.append("Transportation: Excellent use of sustainable transport.")
    elif transport >= 50:
        feedback.append("Transportation: Moderate. Walk or cycle more.")
    else:
        feedback.append("Transportation: High carbon footprint.")

    if electricity >= 80:
        feedback.append("Electricity: Great energy efficiency.")
    elif electricity >= 50:
        feedback.append("Electricity: Moderate usage.")
    else:
        feedback.append("Electricity: High usage.")

    if water >= 80:
        feedback.append("Water: Excellent conservation.")
    elif water >= 50:
        feedback.append("Water: Moderate usage.")
    else:
        feedback.append("Water: High water usage.")

    if recycling >= 80:
        feedback.append("Recycling: Excellent.")
    elif recycling >= 50:
        feedback.append("Recycling: Good but improvable.")
    else:
        feedback.append("Recycling: Needs improvement.")

    if plastic >= 80:
        feedback.append("Plastic: Low plastic usage.")
    elif plastic >= 50:
        feedback.append("Plastic: Moderate usage.")
    else:
        feedback.append("Plastic: Reduce single-use plastic.")

    return feedback


# Save score to CSV
def save_score(score):
    file_exists = os.path.isfile("eco_scores.csv")

    with open("eco_scores.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["score"])

        writer.writerow([score])


# Load scores from CSV
def load_scores():
    scores = []

    if os.path.isfile("eco_scores.csv"):
        with open("eco_scores.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                scores.append(float(row[0]))

    return scores


# Plot progress graph
def plot_progress():
    scores = load_scores()

    if len(scores) == 0:
        print("No score history found.")
        return

    sessions = list(range(1, len(scores) + 1))

    plt.plot(sessions, scores, marker='o')
    plt.xlabel("Session")
    plt.ylabel("Eco Score")
    plt.title("Sustainability Progress Over Time")
    plt.grid(True)
    plt.show()


def calculate():
    user_data = get_user_data()
    scores = calculate_scores(user_data)
    eco_score = calculate_eco_score(scores)
    level = get_level(eco_score)
    feedback = generate_feedback(scores)

    save_score(eco_score)

    print("\n----- RESULTS -----")
    print("Eco Score:", eco_score)
    print("Achievement Level:", level)

    print("\nCategory Scores:")
    print("Transport:", round(scores[0], 2))
    print("Electricity:", scores[1])
    print("Water:", scores[2])
    print("Recycling:", scores[3])
    print("Plastic:", scores[4])

    print("\nDetailed Feedback:")
    for item in feedback:
        print("-", item)


# Main menu
def main():
    while True:
        print("\n1. Calculate Eco Score")
        print("2. View Progress Graph")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            calculate()
        elif choice == "2":
            plot_progress()
        elif choice == "3":
            print("Thank you for using Sustainable Lifestyle Calculator.")
            break
        else:
            print("Invalid choice.")


main()