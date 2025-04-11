import pandas as pd
import ast
import os

this_dir = os.path.dirname(__file__)
def clean_and_eval(column_value):
    """
    Cleans and evaluates a string representation of a list.
    """
    try:
        # Remove extraneous characters and evaluate
        cleaned_value = column_value.strip("[]").replace("'", "").split(", ")
        return cleaned_value
    except Exception as e:
        print(f"Error evaluating {column_value}: {e}")
        return []

# Rule-based prediction function
def get_attributes(category, color_code, material):
    """
    Predict dress codes, occasions, and weather conditions based on input clothing category, material, and color.
    """
    # Load the dataset
    clothing_item_data_frame = pd.read_csv(os.path.join(this_dir, "../dataSets/expanded_clothing_dataset.csv"))
    weather_condition_data_frame = pd.read_csv(os.path.join(this_dir, "../dataSets/expanded_weather_dataset.csv"))

    # Get dress codes and occasions and weather conditions from dataset
    clothing_row = clothing_item_data_frame[clothing_item_data_frame["Clothing_Item"].str.lower() == category.lower()]
    weather_row = weather_condition_data_frame[weather_condition_data_frame["Material"].str.lower() == material.lower()]
    if clothing_row.empty:
        return "Invalid category: No matching dress codes or occasions found."

    dress_codes_str = clothing_row["Dress_Codes"].values[0]
    occasions_str = clothing_row["Occasions"].values[0]
    weather_conditions_str = weather_row["Weather_Condition"].values[0]

    dress_codes = clean_and_eval(dress_codes_str)
    occasions = clean_and_eval(occasions_str)
    weather_conditions = clean_and_eval(weather_conditions_str)

    # Validation: Ensure all inputs are logical
    if not dress_codes or not occasions:
        return "Invalid category: No matching dress codes or occasions found."
    if not weather_conditions:
        return "Invalid material: No matching weather conditions found."
    if not (color_code.startswith("#") and len(color_code) in [4, 7]):  # Hex validation
        return "Invalid color code: Must be a valid hex code."

    return {
        "Dress_Codes": dress_codes,
        "Occasions": occasions,
        "Weather_Conditions": weather_conditions
    }
