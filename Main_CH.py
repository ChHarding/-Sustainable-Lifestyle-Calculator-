# Sustainable Lifestyle Calculator
# Version 1 CLI

import csv
import os
import math
import random
from bisect import bisect_right
from statistics import NormalDist

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib is not installed.")
    print("Please run: pip install matplotlib")
    exit()

try:
    import pandas as pd
except ImportError:
    pd = None


# Daily household transport impact anchors (4-person urban India context).
# These are used in fallback linear scoring (when quantile calibration is not provided).
TRANSPORT_BEST_IMPACT = 90
TRANSPORT_WORST_IMPACT = 240
# Daily household assumptions (4-person urban household context):
# lower is better, with average electricity around 6 kWh/day.
ELECTRICITY_BEST = 2
ELECTRICITY_WORST = 12
WATER_BEST = 60
WATER_WORST = 500
PLASTIC_BEST = 0
PLASTIC_WORST = 15

# Random data generation assumptions (per-day, household-level).
# Triangular mean = (low + high + mode) / 3
RANDOM_INPUT_ASSUMPTIONS = {
    "car": {"low": 20, "high": 40, "mode": 30},
    "bike": {"low": 25, "high": 45, "mode": 35},
    "bus": {"low": 20, "high": 60, "mode": 40},
    "cycle": {"low": 10, "high": 40, "mode": 22},
    "walk": {"low": 2, "high": 10, "mode": 5},
    "electricity": {"low": 1, "high": 11, "mode": 6},
    "water": {"low": 60, "high": 600, "mode": 250},
}

RECYCLING_OPTIONS = ["never", "sometimes", "often", "always"]
RECYCLING_WEIGHTS = [0.10, 0.40, 0.35, 0.15]
PLASTIC_ZERO_PROBABILITY = 0.12
PLASTIC_POISSON_LAMBDA = 4.5
PLASTIC_MAX_COUNT = 25


def triangular_mean(low, high, mode):
    return round((low + high + mode) / 3, 2)

# All numeric inputs are interpreted on a per-day basis.

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

    car_km = get_positive_float("Enter car travel distance (vehicle-km/day, household): ")
    bike_km = get_positive_float("Enter motorcycle travel distance (vehicle-km/day, household): ")
    bus_km = get_positive_float("Enter bus travel distance (passenger-km/day, household): ")
    cycle_km = get_positive_float("Enter bicycle travel distance (km/day, household): ")
    walk_km = get_positive_float("Enter walking distance (km/day, household): ")

    electricity = get_positive_float("Enter electricity usage (kWh/day): ")
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


def calculate_transport_impact(data):
    # Positive = less sustainable, negative = more sustainable.
    return (
        (data["car"] * 3.0)
        + (data["bike"] * 2.0)
        + (data["bus"] * 1.0)
        - (data["cycle"] * 1.0)
        - (data["walk"] * 1.5)
    )


def clamp(value, low, high):
    return max(low, min(high, value))


def inverse_linear_score(value, best_value, worst_value):
    normalized = (value - best_value) / (worst_value - best_value)
    normalized_clamped = clamp(normalized, 0, 1)
    sustainability_fraction = 1 - normalized_clamped
    score_out_of_100 = sustainability_fraction * 100
    return round(score_out_of_100, 2)


def quantile_score(value, sorted_values):
    if not sorted_values:
        return 0

    rank = bisect_right(sorted_values, value) / len(sorted_values)
    epsilon = 1e-6
    sustainability_percentile = clamp(1 - rank, epsilon, 1 - epsilon)
    z_score = NormalDist().inv_cdf(sustainability_percentile)

    score_out_of_100 = 50 + (15 * z_score)
    score_out_of_100 = clamp(score_out_of_100, 0, 100)
    return round(score_out_of_100, 2)


def score_numeric_categories(transport_impact, electricity, water, plastic, quantile_distributions=None):
    if quantile_distributions is not None:
        transport_score = quantile_score(transport_impact, quantile_distributions["transport_impact"])
        electricity_score = quantile_score(electricity, quantile_distributions["electricity"])
        water_score = quantile_score(water, quantile_distributions["water"])
        plastic_score = quantile_score(plastic, quantile_distributions["plastic"])
    else:
        transport_score = inverse_linear_score(
            transport_impact,
            TRANSPORT_BEST_IMPACT,
            TRANSPORT_WORST_IMPACT,
        )
        electricity_score = inverse_linear_score(electricity, ELECTRICITY_BEST, ELECTRICITY_WORST)
        water_score = inverse_linear_score(water, WATER_BEST, WATER_WORST)
        plastic_score = inverse_linear_score(plastic, PLASTIC_BEST, PLASTIC_WORST)

    return transport_score, electricity_score, water_score, plastic_score


def set_quantile_calibration(simulated_dataset):
    transport_impacts = []
    electricity_values = []
    water_values = []
    plastic_values = []

    for row in simulated_dataset:
        transport_impacts.append(calculate_transport_impact(row))
        electricity_values.append(row["electricity"])
        water_values.append(row["water"])
        plastic_values.append(row["plastic"])

    quantile_distributions = {
        "transport_impact": sorted(transport_impacts),
        "electricity": sorted(electricity_values),
        "water": sorted(water_values),
        "plastic": sorted(plastic_values),
    }

    return quantile_distributions


def percentile(sorted_values, p):
    if not sorted_values:
        return 0
    if p <= 0:
        return sorted_values[0]
    if p >= 1:
        return sorted_values[-1]

    index = (len(sorted_values) - 1) * p
    low_index = int(index)
    high_index = min(low_index + 1, len(sorted_values) - 1)
    fraction = index - low_index

    return sorted_values[low_index] + (sorted_values[high_index] - sorted_values[low_index]) * fraction


def generate_random_user_data():
    # Daily transport ranges for a 4-person urban Indian household:
    # car ~20-40 vehicle-km/day, motorcycle ~25-45 vehicle-km/day,
    # bus ~40 passenger-km/day, bicycle ~10-40 km/day, walking ~2-10 km/day.
    def sample_poisson(lam):
        threshold = math.exp(-lam)
        product = 1.0
        count = 0

        while product > threshold:
            count += 1
            product *= random.random()

        return count - 1

    if random.random() < PLASTIC_ZERO_PROBABILITY:
        plastic_count = 0
    else:
        plastic_count = sample_poisson(PLASTIC_POISSON_LAMBDA)

    plastic_count = min(plastic_count, PLASTIC_MAX_COUNT)

    car_cfg = RANDOM_INPUT_ASSUMPTIONS["car"]
    bike_cfg = RANDOM_INPUT_ASSUMPTIONS["bike"]
    bus_cfg = RANDOM_INPUT_ASSUMPTIONS["bus"]
    cycle_cfg = RANDOM_INPUT_ASSUMPTIONS["cycle"]
    walk_cfg = RANDOM_INPUT_ASSUMPTIONS["walk"]
    electricity_cfg = RANDOM_INPUT_ASSUMPTIONS["electricity"]
    water_cfg = RANDOM_INPUT_ASSUMPTIONS["water"]

    return {
        "car": round(random.triangular(car_cfg["low"], car_cfg["high"], car_cfg["mode"]), 2),
        "bike": round(random.triangular(bike_cfg["low"], bike_cfg["high"], bike_cfg["mode"]), 2),
        "bus": round(random.triangular(bus_cfg["low"], bus_cfg["high"], bus_cfg["mode"]), 2),
        "cycle": round(random.triangular(cycle_cfg["low"], cycle_cfg["high"], cycle_cfg["mode"]), 2),
        "walk": round(random.triangular(walk_cfg["low"], walk_cfg["high"], walk_cfg["mode"]), 2),
        "electricity": round(
            random.triangular(electricity_cfg["low"], electricity_cfg["high"], electricity_cfg["mode"]), 2
        ),
        "water": round(random.triangular(water_cfg["low"], water_cfg["high"], water_cfg["mode"]), 2),
        "recycling": random.choices(RECYCLING_OPTIONS, weights=RECYCLING_WEIGHTS, k=1)[0],
        "plastic": plastic_count,
    }


def get_feedback_baseline_scores():
    assumed_means = {
        "car": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["car"]),
        "bike": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["bike"]),
        "bus": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["bus"]),
        "cycle": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["cycle"]),
        "walk": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["walk"]),
    }

    transport_impact = calculate_transport_impact(assumed_means)
    electricity_avg = triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["electricity"])
    water_avg = triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["water"])

    # Mean of zero-inflated Poisson is (1-p_zero) * lambda.
    plastic_avg = (1 - PLASTIC_ZERO_PROBABILITY) * PLASTIC_POISSON_LAMBDA

    transport_score, electricity_score, water_score, plastic_score = score_numeric_categories(
        transport_impact,
        electricity_avg,
        water_avg,
        plastic_avg,
    )

    recycling_levels = {
        "never": 0,
        "sometimes": 1,
        "often": 2,
        "always": 3,
    }
    expected_recycling_level = sum(
        recycling_levels[level] * weight
        for level, weight in zip(RECYCLING_OPTIONS, RECYCLING_WEIGHTS)
    )
    recycling_value = 3 - expected_recycling_level
    recycling_score = inverse_linear_score(recycling_value, 0, 3)

    return {
        "transport": transport_score,
        "electricity": electricity_score,
        "water": water_score,
        "recycling": recycling_score,
        "plastic": plastic_score,
    }


def simulate_score_calculation(simulation_count, output_file="simulation_summary.csv", plot_results=True):
    if pd is None:
        print("Pandas is not installed.")
        print("Please run: pip install pandas")
        return

    if simulation_count <= 0:
        print("Simulation count must be greater than 0.")
        return

    simulated_dataset = [generate_random_user_data() for _ in range(simulation_count)]
    quantile_distributions = set_quantile_calibration(simulated_dataset)

    sorted_transport_impacts = quantile_distributions["transport_impact"]
    p5_transport_impact = round(percentile(sorted_transport_impacts, 0.05), 2)
    p95_transport_impact = round(percentile(sorted_transport_impacts, 0.95), 2)

    run_rows = []

    for run_number, simulated_data in enumerate(simulated_dataset, start=1):
        transport_impact = calculate_transport_impact(simulated_data)
        scores = calculate_scores(simulated_data, quantile_distributions)
        eco_score = calculate_eco_score(scores)
        level = get_level(eco_score)

        run_rows.append(
            {
                "run": run_number,
                "eco_score": round(eco_score, 2),
                "transport_score": round(scores[0], 2),
                "electricity_score": round(scores[1], 2),
                "water_score": round(scores[2], 2),
                "recycling_score": round(scores[3], 2),
                "plastic_score": round(scores[4], 2),
                "level": level,
                "transport_impact": round(transport_impact, 2),
            }
        )

    runs_df = pd.DataFrame(run_rows)

    category_averages = {
        "transport": round(runs_df["transport_score"].mean(), 2),
        "electricity": round(runs_df["electricity_score"].mean(), 2),
        "water": round(runs_df["water_score"].mean(), 2),
        "recycling": round(runs_df["recycling_score"].mean(), 2),
        "plastic": round(runs_df["plastic_score"].mean(), 2),
    }

    level_counts = runs_df["level"].value_counts().to_dict()

    summary_rows = [
        {"metric": "simulation_count", "value": simulation_count},
        {"metric": "calibration_mode", "value": "normal_quantile_mapping"},
        {"metric": "eco_score_average", "value": round(runs_df["eco_score"].mean(), 2)},
        {"metric": "eco_score_min", "value": round(runs_df["eco_score"].min(), 2)},
        {"metric": "eco_score_max", "value": round(runs_df["eco_score"].max(), 2)},
        {"metric": "transport_impact_5th_percentile", "value": p5_transport_impact},
        {"metric": "transport_impact_95th_percentile", "value": p95_transport_impact},
        {"metric": "category_average_transport", "value": category_averages["transport"]},
        {"metric": "category_average_electricity", "value": category_averages["electricity"]},
        {"metric": "category_average_water", "value": category_averages["water"]},
        {"metric": "category_average_recycling", "value": category_averages["recycling"]},
        {"metric": "category_average_plastic", "value": category_averages["plastic"]},
        {"metric": "level_Unsustainable", "value": level_counts.get("Unsustainable", 0)},
        {"metric": "level_Beginner", "value": level_counts.get("Beginner", 0)},
        {"metric": "level_Improving", "value": level_counts.get("Improving", 0)},
        {"metric": "level_Eco-Friendly", "value": level_counts.get("Eco-Friendly", 0)},
        {
            "metric": "level_Sustainability Champion",
            "value": level_counts.get("Sustainability Champion", 0),
        },
        {"metric": "assumed_avg_car_km_day", "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["car"])},
        {"metric": "assumed_avg_bike_km_day", "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["bike"])},
        {
            "metric": "assumed_avg_bus_passenger_km_day",
            "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["bus"]),
        },
        {
            "metric": "assumed_avg_cycle_km_day",
            "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["cycle"]),
        },
        {
            "metric": "assumed_avg_walk_km_day",
            "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["walk"]),
        },
        {
            "metric": "assumed_avg_electricity_kwh_day",
            "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["electricity"]),
        },
        {
            "metric": "assumed_avg_water_liters_day",
            "value": triangular_mean(**RANDOM_INPUT_ASSUMPTIONS["water"]),
        },
    ]

    summary_df = pd.DataFrame(summary_rows)
    inputs_df = pd.DataFrame(simulated_dataset)
    inputs_df.insert(0, "run", range(1, len(inputs_df) + 1))

    output_base_name, _ = os.path.splitext(output_file)
    runs_file = output_base_name + "_runs.csv"
    inputs_file = output_base_name + "_inputs.csv"

    summary_df.to_csv(output_file, index=False)
    runs_df.to_csv(runs_file, index=False)
    inputs_df.to_csv(inputs_file, index=False)

    if plot_results:
        score_columns = [
            "eco_score",
            "transport_score",
            "electricity_score",
            "water_score",
            "recycling_score",
            "plastic_score",
        ]

        fig, axes = plt.subplots(2, 3, figsize=(14, 8))

        for index, column_name in enumerate(score_columns):
            row = index // 3
            col = index % 3
            axis = axes[row][col]
            axis.hist(runs_df[column_name], bins=20, color="tab:blue", alpha=0.8, edgecolor="white")
            axis.set_title(column_name.replace("_", " ").title())
            axis.set_xlabel("Score")
            axis.set_ylabel("Frequency")
            axis.grid(True, alpha=0.2)

        fig.suptitle("Score Distributions Across Simulations")
        plt.tight_layout()
        plt.show()

    print("Simulation complete.")
    print("Summary saved to:", output_file)
    print("Per-run results saved to:", runs_file)
    print("Per-run random inputs saved to:", inputs_file)
    print("Scoring mode: normal-quantile mapping (numeric categories).")
    print("Transport impact percentiles (for reference):")
    print("5th percentile:", p5_transport_impact, "95th percentile:", p95_transport_impact)

# Calculate category scores
def calculate_scores(data, quantile_distributions=None):
    transport_impact = calculate_transport_impact(data)
    transport_score, electricity_score, water_score, plastic_score = score_numeric_categories(
        transport_impact,
        data["electricity"],
        data["water"],
        data["plastic"],
        quantile_distributions
    )

    recycling_levels = {
        "never": 0,
        "sometimes": 1,
        "often": 2,
        "always": 3
    }
    recycling_level = recycling_levels.get(data["recycling"], 0) # 0 to 4

    # Convert level to a "consumption-like" value (higher = worse)
    # so we can reuse inverse_linear_score consistently.
    recycling_value = 3 - recycling_level
    recycling_score = inverse_linear_score(recycling_value, 0, 3)

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

    baselines = get_feedback_baseline_scores()

    def get_thresholds(category_name, band=15):
        baseline = baselines[category_name]
        high_threshold = min(100, baseline + band)
        moderate_threshold = max(0, baseline - band)
        return high_threshold, moderate_threshold

    transport_high, transport_moderate = get_thresholds("transport")
    electricity_high, electricity_moderate = get_thresholds("electricity")
    water_high, water_moderate = get_thresholds("water")
    recycling_high, recycling_moderate = get_thresholds("recycling")
    plastic_high, plastic_moderate = get_thresholds("plastic")

    if transport >= transport_high:
        feedback.append("Transportation: Excellent use of sustainable transport.")
    elif transport >= transport_moderate:
        feedback.append("Transportation: Moderate. Walk or cycle more.")
    else:
        feedback.append("Transportation: High carbon footprint.")

    if electricity >= electricity_high:
        feedback.append("Electricity: Great energy efficiency.")
    elif electricity >= electricity_moderate:
        feedback.append("Electricity: Moderate usage.")
    else:
        feedback.append("Electricity: High usage.")

    if water >= water_high:
        feedback.append("Water: Excellent conservation.")
    elif water >= water_moderate:
        feedback.append("Water: Moderate usage.")
    else:
        feedback.append("Water: High water usage.")

    if recycling >= recycling_high:
        feedback.append("Recycling: Excellent.")
    elif recycling >= recycling_moderate:
        feedback.append("Recycling: Good but improvable.")
    else:
        feedback.append("Recycling: Needs improvement.")

    if plastic >= plastic_high:
        feedback.append("Plastic: Low plastic usage.")
    elif plastic >= plastic_moderate:
        feedback.append("Plastic: Moderate usage.")
    else:
        feedback.append("Plastic: Reduce single-use plastic.")

    return feedback


# Save score to CSV
def save_score(score):
    # Backward-compatible helper for any legacy call sites.
    empty_scores = ("", "", "", "", "")
    empty_user_data = {
        "car": "",
        "bike": "",
        "bus": "",
        "cycle": "",
        "walk": "",
        "electricity": "",
        "water": "",
        "recycling": "",
        "plastic": "",
    }
    save_score_with_details(score, empty_scores, empty_user_data)


def save_score_with_details(eco_score, scores, user_data):
    file_path = "eco_scores_.csv"
    expected_header = [
        "eco_score",
        "transport_score",
        "electricity_score",
        "water_score",
        "recycling_score",
        "plastic_score",
        "car",
        "bike",
        "bus",
        "cycle",
        "walk",
        "electricity",
        "water",
        "recycling",
        "plastic",
    ]

    if os.path.isfile(file_path):
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            current_header = next(reader, [])
            legacy_rows = list(reader)

        if current_header != expected_header:
            migrated_rows = []
            if current_header:
                score_index = 0
                if "eco_score" in current_header:
                    score_index = current_header.index("eco_score")
                elif "score" in current_header:
                    score_index = current_header.index("score")

                for row in legacy_rows:
                    migrated_row = [""] * len(expected_header)
                    if score_index < len(row):
                        migrated_row[0] = row[score_index]
                    migrated_rows.append(migrated_row)

            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(expected_header)
                writer.writerows(migrated_rows)

    else:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(expected_header)

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                eco_score,
                scores[0],
                scores[1],
                scores[2],
                scores[3],
                scores[4],
                user_data["car"],
                user_data["bike"],
                user_data["bus"],
                user_data["cycle"],
                user_data["walk"],
                user_data["electricity"],
                user_data["water"],
                user_data["recycling"],
                user_data["plastic"],
            ]
        )


# Load scores from CSV
def load_scores():
    scores = []

    if os.path.isfile("eco_scores.csv"):
        with open("eco_scores.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)

            score_index = 0
            if header:
                if "eco_score" in header:
                    score_index = header.index("eco_score")
                elif "score" in header:
                    score_index = header.index("score")

            for row in reader:
                if score_index < len(row) and row[score_index] != "":
                    scores.append(float(row[score_index]))

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


def run_calculation(user_data):
    scores = calculate_scores(user_data)
    eco_score = calculate_eco_score(scores)
    level = get_level(eco_score)
    feedback = generate_feedback(scores)

    save_score_with_details(eco_score, scores, user_data)

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


def calculate():
    user_data = get_user_data()
    run_calculation(user_data)


def calculate_auto_user():
    user_data = generate_random_user_data()

    print("\nUsing auto-generated user data:")
    print(user_data)

    run_calculation(user_data)


# Main menu
def main():
    while True:
        print("\n1. Calculate Eco Score")
        print("2. View Progress Graph")
        print("3. Run Score Simulation")
        print("4. Calculate Eco Score (Auto User)")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            calculate()
        elif choice == "2":
            plot_progress()
        elif choice == "3":
            simulation_count = get_positive_int("Enter number of simulations to run: ")
            simulate_score_calculation(simulation_count)
        elif choice == "4":
            calculate_auto_user()
        elif choice == "5":
            print("Thank you for using Sustainable Lifestyle Calculator.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()