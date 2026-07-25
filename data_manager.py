"""
data_manager.py

Handles saving and loading sustainability records.
"""

import csv
import os
from datetime import datetime

CSV_FILE = "eco_scores.csv"


def create_csv():
    """
    Create the CSV file with headers if it doesn't exist.
    """

    if not os.path.exists(CSV_FILE):

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
                "Achievement Level"

            ])


def save_record(data, scores, eco_score, level, feedback):
    """
    Save one sustainability record to the CSV file.

    Args:
        data (dict): User inputs.
        scores (tuple): Category scores.
        eco_score (float): Final Eco Score.
        level (str): Sustainability level.
        feedback (list): Recommendation messages.

    Note:
        Recommendations are NOT stored.
        They are generated dynamically whenever the app loads.
    """

    create_csv()

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([

            datetime.now().strftime("%Y-%m-%d"),

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


def load_history():
    """
    Load all saved records.

    Returns:
        list: List of dictionaries.
    """

    create_csv()

    history = []

    try:

        with open(CSV_FILE, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                history.append(row)

    except FileNotFoundError:

        return []

    return history


def record_count():
    """
    Returns the number of saved records.
    """

    history = load_history()

    return len(history)


def latest_record():
    """
    Returns the latest saved record.

    Returns:
        dict or None
    """

    history = load_history()

    if len(history) == 0:
        return None

    return history[-1]