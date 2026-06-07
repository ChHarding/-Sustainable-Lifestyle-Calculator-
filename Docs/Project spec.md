## Sustainable Lifestyle Calculator

## Project Overview
The Sustainable Lifestyle Calculator is a Python-based application that helps users understand the environmental impact of their everyday habits. Many people want to live more sustainably but are unsure how activities such as transportation choices, electricity consumption, water usage, recycling habits, and plastic usage affect the environment. This project aims to make sustainability easier to understand by converting daily activities into a measurable sustainability score.
The calculator will ask users to enter information about their lifestyle habits. The system will then calculate scores for different sustainability categories and combine them into an overall Eco Score. Based on the final score, users will receive an achievement level and personalized feedback that encourages environmentally friendly behavior.
The project connects with my personal interest in sustainability, waste reduction, composting, and eco-friendly living. I am interested in creating tools that increase awareness of environmental issues and encourage people to make small positive changes in their daily lives.
For Version 1, the project will run as a Command Line Interface (CLI) application in Python. Users will enter data through simple text prompts. The program will calculate scores, save results to a CSV file, and generate charts using Python libraries such as pandas and matplotlib.
In the future, the project could be expanded into a graphical dashboard using Streamlit or a web interface where users can track sustainability habits over longer periods and view more detailed reports.

## Use Case
A user wants to understand how environmentally friendly their weekly habits are. They open the Sustainable Lifestyle Calculator and enter information about:
•	Distance traveled by car, motorcycle, bus, bicycle, and walking
•	Electricity consumption
•	Water consumption
•	Recycling habits
•	Single-use plastic usage
The calculator analyzes these activities using predefined sustainability scores and category weights. It then generates an Eco Score between 0 and 100, assigns an achievement level, and provides suggestions for improvement.
For example:
“You achieved Eco-Friendly status this week. Your recycling habits helped improve your score. Reducing single-use plastic usage could increase your sustainability rating even further.”

# Users and Stakeholders
# Primary Users
•	Students
•	Families
•	Sustainability-conscious individuals
•	People interested in tracking eco-friendly habits
# Secondary Stakeholders
•	Environmental clubs
•	Schools
•	Community sustainability programs
•	NGOs promoting environmental awareness

# Problem It Solves
Many people want to adopt sustainable habits but do not have a simple way to measure the environmental impact of their daily activities. Most individuals are unaware of how transportation choices, electricity consumption, water usage, recycling behavior, and plastic usage contribute to sustainability.
This project increases awareness by collecting sustainability-related information, converting it into measurable scores, and providing meaningful feedback. The goal is to encourage users to make better environmental decisions through simple tracking and visualization.

# Primary Interaction
The user:
1.	Opens the program.
2.	Enters transportation information.
3.	Enters electricity usage.
4.	Enters water consumption.
5.	Selects recycling habits.
6.	Enters single-use plastic usage.
7.	Receives category scores.
8.	Receives a final Eco Score.
9.	Receives an achievement level.
10.	Views charts and sustainability recommendations.
This creates a habit-building feedback loop where users can monitor their progress and improve their sustainability practices over time.

# Task Vignette 1 – Entering Sustainability Data
A user wants to check their sustainability performance for the current week. The program asks them to enter information about transportation, electricity usage, water consumption, recycling habits, and plastic usage. The user answers each question and submits their data.
The system stores the information and prepares it for score calculation.
Technical Notes
•	User input collected through Python input() statements.
•	Transportation measured in kilometers.
•	Electricity measured in kWh.
•	Water measured in liters per day.
•	Recycling stored as text values:
o	Never
o	Sometimes
o	Often
o	Always
•	Plastic usage stored as number of items.

# Task Vignette 2 – Calculating Sustainability Scores
After entering data, the program calculates scores for each category. Transportation activities receive positive or negative impact values based on environmental friendliness.
Example transportation impact values:
•	Car = -3
•	Motorcycle = -2
•	Bus = -1
•	Bicycle = +1
•	Walking = +1.5
The system combines these category scores and applies category weights to generate a final Eco Score.
Technical Notes
•	Scores stored in Python dictionaries.
•	Category weights stored as variables.
•	Simple mathematical calculations used.
•	Final score normalized to a value between 0 and 100.
Example weights:
•	Transportation = 30%
•	Electricity = 20%
•	Water = 15%
•	Recycling = 20%
•	Plastic Usage = 15%
Weights can be adjusted later if needed.

# Task Vignette 3 – Viewing Results and Feedback
Once the Eco Score has been calculated, the program displays the user’s sustainability level and provides recommendations.
The user can see whether they are performing well or whether certain habits need improvement.
Example feedback:
“Your transportation choices contributed positively to your score. Consider reducing single-use plastics to further improve your sustainability rating.”
Technical Notes
Achievement levels:
•	0–20 = Unsustainable
•	21–40 = Beginner
•	41–60 = Improving
•	61–80 = Eco-Friendly
•	81–100 = Sustainability Champion
Feedback generated using simple if-else statements.

# Task Vignette 4 – Viewing Progress Charts
The user can save weekly sustainability data and view charts showing progress over time. The charts help visualize changes in sustainability habits.
The user can compare scores from different weeks and identify trends.
Technical Notes
•	Data stored in CSV files.
•	pandas used to read and manage data.
•	matplotlib used to generate charts.
•	Simple line charts and pie charts will be created.

# Interface Possibility
Version 1 Interface:
•	Command Line Interface (CLI)
•	Implemented using Python input and print statements
Future Interface Possibilities:
•	Streamlit Dashboard
•	Web-based interface
•	Sustainability tracking dashboard
•	Interactive charts and reports

# Data and Processing
 # Input Data
Transportation
•	Car distance (km)
•	Motorcycle distance (km)
•	Bus distance (km)
•	Bicycle distance (km)
•	Walking distance (km)
Electricity consumption (kWh)
Water consumption (liters per day)
Recycling
•	Never
•	Sometimes
•	Often
•	Always
Number of single-use plastic items

# Processing
The system will:
1.	Collect user inputs.
2.	Calculate category scores.
3.	Apply category weights.
4.	Generate a final Eco Score.
5.	Assign an achievement level.
6.	Generate sustainability feedback.
7.	Save results to a CSV file.
8.	Create visualizations.


# Output
The program will display:
•	Category scores
•	Eco Score
•	Achievement level
•	Sustainability feedback
•	Weekly charts
•	Sustainability reports
Example:
Eco Score: 76
Achievement Level: Eco-Friendly
Recommendation: Reduce single-use plastic usage and continue using public transportation.

# Technical Flow
User Input
↓
Data Validation
↓
Category Score Calculation
↓
Weighted Score Calculation
↓
Eco Score Generation
↓
Achievement Level Assignment
↓
Feedback Generation
↓
Save to CSV File
↓
Generate Charts
↓
Display Results

Planned Python Modules
•	pandas
•	matplotlib
•	csv

# Data Storage
weekly_data.csv
Columns:
•	Date
•	Car_km
•	Motorcycle_km
•	Bus_km
•	Bicycle_km
•	Walk_km
•	Electricity_kWh
•	Water_Liters
•	Recycling
•	Plastic_Items
•	EcoScore
•	AchievementLevel

# Challenge
The biggest challenge will be creating a sustainability scoring system that is fair, meaningful, and easy to understand.
Another challenge is deciding how much each sustainability category should contribute to the final Eco Score. The scoring system should remain simple while still encouraging positive environmental behavior.

# What I Can Do Myself
•	Design the user experience.
•	Create the sustainability categories.
•	Develop the scoring logic.
•	Build the Python CLI application.
•	Create charts and visualizations using matplotlib.
•	Organize the data flow.
•	Design future dashboard concepts.

# Final Self Assessment
The biggest change from my original sketch is the addition of weighted category scoring, achievement levels, and configurable impact values. The project has evolved from a simple sustainability tracker into a sustainability scoring and feedback system.
The biggest potential problem is designing a scoring system that produces meaningful results while remaining simple enough to implement.
I feel reasonably confident about implementing this project because it builds on the Python concepts I learned in previous coursework, such as variables, conditionals, loops, dictionaries, and simple calculations.
Since I am still a beginner programmer and do not have a computer science background, I may need occasional guidance with some technical aspects such as data storage, CSV file management, data visualization, and organizing the overall program structure. 
However, I believe the project is achievable with further practice, learning, and support when needed.
