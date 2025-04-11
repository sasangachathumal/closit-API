import logging
from flask import jsonify
from database.models import db
import os
import csv
from itertools import product

this_dir = os.path.dirname(__file__)

# enable logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Convert missing categories to dicts so we can assign color
def create_missing_clothing_items_obj(missing_categories, filters):
    return [
        {
            "category": category,
            "occasions": filters.get("occasions", []),
            "dressCodes": filters.get("dress_codes", []),
        }
        for category in missing_categories
    ]

# error handlers
def sql_alchemy_error_handlers(e):
    db.session.rollback()
    logger.error(f"Database error: {str(e)}")
    return jsonify({'error': 'Database error'}), 500

def exception_handlers(e):
    logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500

def update_dress_code_rules(new_data):
    # Read existing combinations from the CSV
    existing_combinations = set()
    if os.path.exists(os.path.join(this_dir, '../dataSets/dress_code_rules.csv')):
        with open(os.path.join(this_dir, '../dataSets/dress_code_rules.csv'), mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_combinations.add((row['occasion'], row['dress_code']))

    # Generate all combinations from DB data
    new_combinations = set(product(new_data['occasions'], new_data['dressCodes']))
    # Identify missing combinations
    missing_combinations = new_combinations - existing_combinations
    # If there missing combinations append to CSV
    if missing_combinations:
        print("Adding new combinations:")
        with open(os.path.join(this_dir, '../dataSets/dress_code_rules.csv'), mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['occasion', 'dress_code'])
            # If file was just created, write header
            if os.stat(os.path.join(this_dir, '../dataSets/dress_code_rules.csv')).st_size == 0:
                writer.writeheader()
            for occasion, dress_code in missing_combinations:
                print(occasion)
                print(dress_code)
                # Save to CSV
                writer.writerow({'occasion': occasion, 'dress_code': dress_code})
