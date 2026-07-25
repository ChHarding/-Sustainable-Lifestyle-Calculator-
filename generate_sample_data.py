"""
generate_sample_data.py

Generates 60 days of realistic sample sustainability data
for testing graphs and analytics.
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

# Delete old CSV and create a fresh one
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


start_date = datetime.now() - timedelta(days=59)

for day in range(60):

    date = start_date + timedelta(days=day)

    data = {

        "car": random.randint(0, 8),
        "bike": random.randint(0, 3),
        "bus": random.randint(0, 5),
        "cycle": random.randint(0, 4),
        "walk": random.randint(0, 8),

        # Monthly-style values to match your current calculator
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

    scores = calculate_scores(data)

    eco_score = calculate_eco_score(scores)

    level = get_level(eco_score)

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