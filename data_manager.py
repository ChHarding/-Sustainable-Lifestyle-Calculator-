"""
data_manager.py

Manages the application's sustainability records.

This module is responsible for creating, reading and updating
the CSV file used by the Sustainable Lifestyle Calculator.
It stores each completed sustainability assessment and
provides helper functions for retrieving historical data
throughout the application.
"""

import csv
import os
from datetime import datetime

CSV_FILE = "eco_scores.csv"


def create_csv():
    """
    Create the application's CSV file if it does not already exist.

    The CSV file is automatically created with the required
    column headings the first time the application is run.
    This ensures that data can be saved without requiring
    any manual setup.
    """

    # Create the CSV file only if it
    # does not already exist.
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
    Save a completed sustainability assessment.

    Each time the user calculates an Eco Score, the
    assessment is appended as a new row in the CSV file.
    This allows the application to maintain a history
    of previous sustainability records for visualisation
    and progress tracking.

    Args:
        data (dict):
            User-entered sustainability data.

        scores (tuple):
            Category scores calculated from the user's inputs.

        eco_score (float):
            Final weighted Eco Score.

        level (str):
            Sustainability achievement level.

        feedback (list):
            Personalised sustainability recommendations.

    Note:
        Recommendations are not stored in the CSV file.
        They are generated dynamically whenever a new
        assessment is calculated.
    """

    create_csv()

    # Append the latest assessment
    # to the existing CSV file.
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
    Load all saved sustainability records.

    The saved CSV file is read and converted into
    a list of dictionaries. Each dictionary represents
    one completed sustainability assessment.

    Returns:
        list:
            A list containing all saved sustainability
            records. Returns an empty list if no records
            are available.
    """

    create_csv()

    history = []

    try:

        # Read every saved assessment
        # from the CSV file.
        with open(CSV_FILE, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                history.append(row)

    except FileNotFoundError:

        return []

    return history


def record_count():
    """
    Count the total number of saved assessments.

    Returns:
        int:
            Total number of sustainability records
            currently stored in the CSV file.
    """

    history = load_history()

    return len(history)


def latest_record():
    """
    Retrieve the most recent sustainability assessment.

    Returns:
        dict | None:
            The latest saved record if one exists,
            otherwise None.
    """

    history = load_history()

    # Return None when no records
    # have been saved yet.
    if len(history) == 0:
        return None

    return history[-1]