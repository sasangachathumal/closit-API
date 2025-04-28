# Closit: Clothing Item Recommendation System (Backend API)

## Project Overview
Closit is an intelligent clothing recommendation system designed to suggest suitable 
clothing items based on user prompt considering a variety of factors such as the occasion, dress codes, and personal 
wardrobe items. It provides personalized suggestions for clothing items and colors, helping users make better 
choices when getting dressed. The system allows users to input prompt describing the event or situation 
and receives clothing recommendations, considering the user’s existing wardrobe and suggesting new items when necessary.

## Features
- Clothing Recommendations: Suggests clothing items based on the prompt and matched to user's wardrobe.
- Predict Clothing Item Attributes: When user save clothing item predict clothing item suitable dress codes, occasions, weather conditions.
- Interactive Clothing save Tool: Allow user to save clothing items in the system wardrobe using innovative and interactive tool. 
- Dress Code Prediction: Predicts the appropriate dress code (formal, casual, etc.) based on user input.
- Wardrobe Lookup: Checks if the user already owns the suggested clothing items in their wardrobe.

## Technology and Tools
- Python
- Flask
- SQL Alchemy
- JWT
- spacy
- pandas
- seaborn
- matplotlib colors
- fuzzywuzzy
- werkzeug.security
- marshmallow

## How to Set Up and Run the Project
### Prerequisites
- Python 3.x
- SQLite database

### Setting Up the API
1. Clone the repository
   ```bash
   git clone https://github.com/sasangachathumal/closit-API.git
2. Navigate to the project directory
   ```bash
   cd closit-API
3. Set up a Python virtual environment (If required)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
4. Install the required dependencies
   ```bash
   pip install -r requirements.txt
5. Set up the database and clearn dataset
   - The SQLite database is pre-configured, but you need to initialize the tables.
   - Run the following script to set up the database
   ```bash
   python application_init.py
6. Run the Flask application
   ```bash
   python server.py

