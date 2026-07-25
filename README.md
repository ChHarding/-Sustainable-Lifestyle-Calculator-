# Sustainable Lifestyle Calculator

## Overview

The Sustainable Lifestyle Calculator is a Streamlit-based application that helps users evaluate their daily environmental impact by calculating an Eco Score based on their lifestyle habits. The application provides personalized sustainability recommendations, stores historical records, and visualizes progress using interactive charts.

---

## Features

- Calculate an overall Eco Score based on daily activities
- Transportation sustainability assessment
- Electricity and water usage evaluation
- Recycling habit analysis
- Single-use plastic usage tracking
- Personalized sustainability recommendations
- Historical data storage using CSV
- Interactive dashboard with Plotly visualizations
- Weekly and monthly moving averages
- Goal tracking
- Trend analysis
- 60-day sample data generator for analytics demonstration

---

## Technologies Used

- Python
- Streamlit
- Plotly
- Pandas
- CSV
- Object-Oriented Programming principles

---

## Project Structure

```
Sustainable_Lifestyle_Calculator/
│
├── app.py
├── calculator.py
├── data_manager.py
├── visualization.py
├── generate_sample_data.py
├── eco_scores.csv
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── Docs/
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Sample Data

To generate sample sustainability records for testing dashboards and analytics:

```bash
python generate_sample_data.py
```

This creates 60 days of realistic sustainability data in `eco_scores.csv`.

---

## Dashboard

The dashboard includes:

- Historical Records
- Progress Over Time
- Weekly Moving Average
- Monthly Moving Average
- Goal Tracking
- Weekly Goal Summary
- Trend Analysis
- Latest Entry Summary

---

## Author

Sanika Halale

---

## License

This project is released under the MIT License.