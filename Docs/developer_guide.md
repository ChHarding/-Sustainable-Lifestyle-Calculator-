# Developer Guide

## Sustainable Lifestyle Calculator

**Author:** Sanika Halale

---

# 1. Project Overview

## Introduction

The Sustainable Lifestyle Calculator is a Streamlit-based application that helps users understand the environmental impact of their daily lifestyle choices. By entering information about transportation, electricity usage, water consumption, recycling habits and single-use plastic usage, users receive an Eco Score along with personalised recommendations for living more sustainably.

Unlike a simple score calculator, the application also stores previous assessments and provides an interactive dashboard where users can monitor their progress over time. The dashboard includes historical records, moving averages, goal tracking and trend analysis to encourage long-term sustainable behaviour.

This project was developed as part of the Python Programming course and demonstrates how Python can be used to build an interactive application that combines user input, data processing, persistent storage and data visualisation.

---

## Purpose of this Guide

This document is intended for anyone who needs to understand, maintain or extend the project after development.

While the README explains how to install and run the application, this guide focuses on the technical implementation of the project. It explains how the application is organised, how data flows through the system, and the responsibility of each module.

Reading this guide alongside the source code should help a new developer become familiar with the project more quickly and confidently make future modifications.

---

## Application Overview

The application follows a simple multi-page workflow.

1. The user starts on the **Intro** page.
2. The user enters sustainability data on the **Input** page.
3. The application calculates category scores and an overall Eco Score.
4. The results are displayed together with personalised recommendations.
5. Every assessment is saved to a CSV file.
6. The Dashboard displays historical data and interactive visualisations.

The application has been designed with a clear separation of responsibilities. User interface components, calculation logic, data management and visualisation are implemented in separate modules, making the project easier to understand and maintain.

---

# 2. Final Features Implemented

The final version of the Sustainable Lifestyle Calculator includes all of the core functionality that was planned during the design phase, along with several improvements that were introduced during development based on testing and usability feedback.

The application is organised into multiple pages, making it easier for users to complete the sustainability assessment and review their results. Rather than displaying everything on a single screen, each stage of the workflow focuses on a specific task.

The main features currently implemented are:

### Sustainability Assessment

- Collects user inputs related to transportation, electricity usage, water consumption, recycling habits and single-use plastic usage.
- Calculates individual sustainability scores for each category.
- Computes a weighted Eco Score using all category scores.
- Assigns an achievement level based on the final Eco Score.
- Generates personalised sustainability recommendations.

### Data Management

- Saves every completed assessment to a CSV file.
- Automatically creates the CSV file if it does not already exist.
- Maintains historical sustainability records that can be reused across multiple application sessions.

### Dashboard and Analytics

The dashboard allows users to analyse their historical sustainability performance using interactive visualisations.

The following analytics have been implemented:

- Progress Over Time graph
- Weekly Moving Average
- Monthly Moving Average
- Goal Tracking
- Weekly Goal Summary
- Sustainability Trend Analysis
- Historical Records table
- Latest Entry summary

### User Interface

The application uses a custom Streamlit interface that includes:

- Multi-page navigation
- Consistent styling across all pages
- Responsive layout using columns
- Metric cards
- Interactive Plotly charts
- Primary, secondary and tertiary call-to-action buttons
- Clear visual hierarchy and section grouping

### Testing Utility

A separate utility script is included to generate sixty days of realistic sustainability data. This allows the dashboard and analytics features to be tested without manually entering large amounts of data.

---

# 3. Installation and Developer Setup

This section explains the steps required to set up the project for development. It assumes that the developer has already cloned the repository and has a basic understanding of Python and Streamlit.

## System Requirements

The project was developed and tested using:

- Python 3.x
- Streamlit
- Pandas
- Plotly

The required libraries are listed in the `requirements.txt` file.

## Installing Dependencies

Install the required packages by running:

```bash
pip install -r requirements.txt
```

## Running the Application

Launch the application using:

```bash
streamlit run app.py
```

The application opens in a web browser and starts on the **Intro** page.

## Generating Sample Data

The dashboard is designed to display historical sustainability records. If no records are available, the dashboard will initially appear empty.

To generate sample data for testing, run:

```bash
python generate_sample_data.py
```

This creates sixty days of realistic sustainability records and stores them in `eco_scores.csv`.

## Project Organisation

The project has been organised so that each module has a specific responsibility.

- `app.py` acts as the application's entry point.
- The `ui` folder contains all user interface pages.
- `calculator.py` contains the scoring logic.
- `data_manager.py` manages data storage and retrieval.
- `visualization.py` creates the dashboard graphs and analytics.

Keeping these responsibilities separate makes the project easier to maintain and extend as new features are added.

---

# 4. User Interaction and Application Flow

## User Journey

The application follows a simple step-by-step workflow that guides users through a sustainability assessment before presenting their results and historical progress.

```
                 Start Application
                        │
                        ▼
                 Intro Page
                        │
        Calculate My Eco Score
                        │
                        ▼
              Input Sustainability Data
                        │
          Click "Calculate Eco Score"
                        │
                        ▼
            Score Calculation Engine
                        │
                        ▼
         Save Record to eco_scores.csv
                        │
                        ▼
                Results Page
                        │
            View Dashboard (Optional)
                        │
                        ▼
          Dashboard and Analytics
```

Each page has a specific responsibility, making the workflow straightforward for users while keeping the code organised for future development.

---

## Code Walkthrough

This section explains what happens internally as the user moves through the application.

### Step 1 – Application Launch

The application starts from **app.py**, which serves as the main entry point.

When the application is launched, Streamlit configures the page settings and creates a session state variable named `page`. This variable is used throughout the application to control navigation between pages.

If no page has been selected yet, the application automatically loads the Intro page.

```
app.py
        │
        ▼
show_intro()
```

---

### Step 2 – Intro Page

The Intro page is implemented in **ui/intro.py**.

Its primary purpose is to introduce the application and guide users towards starting a sustainability assessment.

This page also displays:

- Project overview
- Feature highlights
- Number of saved sustainability records
- Navigation buttons

If historical records already exist, users can also access the Dashboard directly from this page.

---

### Step 3 – Input Page

Selecting **Calculate My Eco Score** opens the Input page.

The Input page collects all information required for the sustainability assessment, including:

- Transportation habits
- Electricity usage
- Water consumption
- Recycling habits
- Single-use plastic usage

After the user submits the form, all inputs are organised into a dictionary before being passed to the calculation functions.

```
User Inputs
      │
      ▼
calculate_scores()
      │
      ▼
calculate_eco_score()
      │
      ▼
get_level()
      │
      ▼
generate_feedback()
```

The calculated values are temporarily stored in Streamlit's session state so they can be accessed by other pages without requiring the calculations to be repeated.

---

### Step 4 – Saving the Assessment

After the calculations are completed, the application stores the results using **data_manager.py**.

The `save_record()` function appends the assessment to `eco_scores.csv`.

Each saved record includes:

- Date
- User inputs
- Category scores
- Final Eco Score
- Achievement level

The recommendation messages are not stored because they are generated dynamically whenever a new assessment is completed.

---

### Step 5 – Results Page

Once the record has been saved, the application automatically navigates to the Results page.

This page displays:

- Final Eco Score
- Achievement level
- Category-wise scores
- Personalised recommendations
- Today's sustainability inputs
- Eco Score progress graph

The progress graph is created using functions from **visualization.py**, which converts the saved CSV data into interactive Plotly charts.

---

### Step 6 – Dashboard

The Dashboard provides a historical view of the user's sustainability performance.

When the Dashboard loads, the application:

1. Reads all saved records from `eco_scores.csv`.
2. Converts the records into a pandas DataFrame.
3. Generates interactive visualisations.
4. Calculates summary statistics and sustainability trends.

The dashboard currently includes:

- Progress Over Time
- Weekly Moving Average
- Monthly Moving Average
- Goal Tracking
- Weekly Goal Summary
- Trend Analysis
- Historical Records
- Latest Entry Summary

This separation between data processing and user interface allows the dashboard to remain easy to extend as additional analytics are added.


---

# 5. Project Architecture and Module Responsibilities

The project follows a modular structure where each file has a specific responsibility. Separating the user interface, calculation logic, data management and visualisation makes the application easier to understand, maintain and extend.

## Overall Architecture

```
                           app.py
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     intro.py          input_page.py        results.py
                              │                   │
                              ▼                   │
                      calculator.py               │
                              │                   │
                              ▼                   │
                      data_manager.py             │
                              │                   │
                              ▼                   ▼
                     eco_scores.csv      visualization.py
                              │
                              ▼
                        dashboard.py
```

The application follows a simple layered structure:

- **app.py** controls navigation.
- **UI modules** display information and collect user input.
- **calculator.py** performs all sustainability calculations.
- **data_manager.py** manages persistent storage.
- **visualization.py** prepares analytics and dashboard graphs.

Each layer has a single responsibility, making the project easier to modify without affecting unrelated components.

---

## Module Responsibilities

| Module | Responsibility |
|---------|----------------|
| **app.py** | Entry point of the application. Configures Streamlit and manages navigation between pages. |
| **ui/intro.py** | Displays the application's landing page and guides users to begin a sustainability assessment or open the dashboard. |
| **ui/input_page.py** | Collects sustainability data from the user and starts the scoring process. |
| **calculator.py** | Calculates category scores, computes the Eco Score, determines the achievement level and generates personalised recommendations. |
| **data_manager.py** | Creates the CSV file, stores completed assessments and retrieves historical records. |
| **ui/results.py** | Presents the calculated Eco Score, category scores, recommendations and summary of the current assessment. |
| **visualization.py** | Converts historical data into DataFrames and creates all dashboard charts, moving averages and analytics. |
| **ui/dashboard.py** | Displays historical sustainability records, analytics, trend analysis and goal tracking. |
| **ui/styles.py** | Applies a consistent visual style across every page of the application. |
| **generate_sample_data.py** | Generates sample sustainability records for testing the dashboard and visualisations. |

---

## Data Flow

The application's data flows through the modules in a predictable sequence.

```
User Input
      │
      ▼
input_page.py
      │
      ▼
calculator.py
      │
      ▼
data_manager.py
      │
      ▼
eco_scores.csv
      │
      ▼
visualization.py
      │
      ▼
dashboard.py
```

The calculation logic is intentionally separated from the user interface. This allows the scoring functions to remain independent of Streamlit, making them easier to understand, test and reuse.

Similarly, all visualisation logic has been isolated within `visualization.py`. This keeps the dashboard page focused on presenting information rather than performing data analysis.

---

## Session State

The application uses Streamlit's **session state** to manage navigation and temporarily store the most recent sustainability assessment.

The following values are stored in the session state after each calculation:

- Current page
- User inputs
- Category scores
- Eco Score
- Achievement level
- Personalised recommendations

Using session state allows information to be shared between pages without recalculating the results each time the user navigates through the application.

---

## Design Decisions

Several design decisions were made to keep the project simple and maintainable.

- The project uses a modular structure instead of placing all code in a single file.
- Sustainability calculations are isolated from the user interface.
- Historical data is stored in a CSV file to avoid the additional complexity of setting up a database.
- Plotly was selected for visualisations because it provides interactive charts that integrate well with Streamlit.
- A shared styling module ensures a consistent interface across all pages without duplicating CSS.

---

# 6. Known Issues

At the time of submission, no major issues were identified that prevent the application from functioning as intended. However, there are a few limitations that could be improved in future versions.

## Minor Limitations

- Sustainability records are stored in a CSV file rather than a database. While this approach is simple and suitable for this project, it may become less efficient if a large number of records are stored.

- The dashboard currently displays information for a single user only. There is no support for multiple user accounts or personalised profiles.

- The scoring model is based on predefined sustainability assumptions and weightings. These values provide a reasonable demonstration but are not intended to represent an official environmental assessment.

- The application currently runs locally through Streamlit and is not deployed as a public web application.

## Major Issues

No major issues are currently known. All core functionality, including score calculation, data storage, dashboard analytics and navigation, works as expected.

---

# 7. Future Work

Although the application meets all of its current objectives, there are several opportunities to expand the project in future versions.

Possible improvements include:

- Allow users to create individual accounts and maintain separate sustainability histories.
- Replace CSV storage with a relational database such as SQLite or PostgreSQL.
- Export sustainability reports as PDF documents.
- Add authentication for user login and profile management.
- Introduce additional sustainability categories such as food consumption, renewable energy usage or carbon footprint estimation.
- Allow users to customise sustainability goals and compare long-term progress.
- Integrate external environmental datasets or public sustainability APIs to provide more accurate recommendations.
- Deploy the application to a cloud platform such as Streamlit Community Cloud so that it can be accessed online.

These enhancements would improve scalability, usability and make the application suitable for a wider audience.

---

# 8. Ongoing Development and Maintenance

Although this project was developed as a university assignment, its modular structure makes it relatively easy to maintain and extend.

Developers adding new features should follow the existing project structure by keeping responsibilities separated across different modules. User interface components should remain inside the `ui` folder, calculation logic should continue to be implemented in `calculator.py`, data storage should be managed through `data_manager.py`, and all visualisation functions should remain within `visualization.py`.

Maintaining this separation of responsibilities will help keep the project organised as additional features are introduced.

If future scoring methods or sustainability categories are added, updating the calculation functions and visualisation module should be sufficient without requiring significant changes to the user interface.

---

# Conclusion

The Sustainable Lifestyle Calculator demonstrates how Python can be used to build a complete interactive application that combines user input, data processing, persistent storage and data visualisation.

The project was intentionally designed using a modular architecture to improve readability, maintainability and future scalability. Separating the application into dedicated modules has made the code easier to understand and allows future developers to modify individual components without affecting the rest of the system.

Overall, the project provides a practical example of applying Python programming concepts to solve a real-world sustainability problem while maintaining a clear and organised software structure.