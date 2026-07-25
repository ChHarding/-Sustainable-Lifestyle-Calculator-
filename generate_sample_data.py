"""
generate_sample_data.py

Generate sample sustainability records for testing.

This utility script creates 60 days of realistic sustainability
data and stores it in the application's CSV file. The generated
data can be used to test dashboard visualisations, trend analysis,
and other features without manually entering records.
"""

import csv
import random
from datetime import datetime, timedelta

from calculator import (
    calculate_scores,
    calculate_eco_score,
    get_level,
)

CSV_FILE = "eco_scores.csv"

# ----------------------------------------------------
# Create a Fresh CSV File
# ----------------------------------------------------
# Replace any existing data with a new CSV file
# containing only the required column headings.

with open(CSV_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Date",
        "Car",
        "Bike",
        "Bus",
        "Cycle",
        "Walk",
        "Electricity",
        "Water",
        "Recycling",
        "Plastic",
        "Transport Score",
        "Electricity Score",
        "Water Score",
        "Recycling Score",
        "Plastic Score",
        "Eco Score",
        "Achievement Level",
    ])

# Generate sample data for the
# previous 60 calendar days.
start_date = datetime.now() - timedelta(days=59)

for day in range(60):

    date = start_date + timedelta(days=day)

    # ----------------------------------------------------
    # Generate Random Sustainability Data
    # ----------------------------------------------------
    # Create realistic input values that closely
    # resemble everyday lifestyle habits.

    data = {

        "car": random.randint(0, 8),
        "bike": random.randint(0, 3),
        "bus": random.randint(0, 5),
        "cycle": random.randint(0, 4),
        "walk": random.randint(0, 8),

        # Monthly-style values are generated to
        # match the assumptions used by the calculator.
        "electricity": random.randint(80, 350),

        "water": random.randint(80, 350),

        "recycling": random.choice([
            "never",
            "sometimes",
            "often",
            "always"
        ]),

        "plastic": random.randint(0, 8)

    }

    # Calculate the sustainability scores
    # for the generated sample data.

    scores = calculate_scores(data)

    eco_score = calculate_eco_score(scores)

    level = get_level(eco_score)

    # Save the generated record
    # to the CSV file.

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([

            date.strftime("%Y-%m-%d"),

            data["car"],
            data["bike"],
            data["bus"],
            data["cycle"],
            data["walk"],

            data["electricity"],
            data["water"],
            data["recycling"],
            data["plastic"],

            scores[0],
            scores[1],
            scores[2],
            scores[3],
            scores[4],

            eco_score,
            level

        ])

print("✅ 60 days of sample data generated successfully!")