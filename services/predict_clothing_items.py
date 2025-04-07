import spacy
from fuzzywuzzy import process
import pandas as pd
import csv
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Men's clothing items (limited list)
CLOTHING_ITEMS = [
    "long sleeve shirt", "short sleeve shirt", "long sleeve t-shirt", "short sleeve t-shirt",
    "jean", "trouser", "hoodie", "short", "leather shoes", "casual shoes",
    "shirt", "t-shirt", "shoes"
]

# Basic color names
COLOR_LIST = [
    "white", "black", "blue", "green", "red", "yellow", "orange", "pink", "brown", "grey", "gray",
    "navy", "maroon", "beige", "cream", "purple", "light yellow", "dark blue", "sky blue"
]

# Load occasion keywords from CSV
def load_occasion_keywords_from_csv():
    occasion_keywords = {}
    with open('../dataSets/occasion_keywords.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword = row['keyword'].strip().lower()
            occasion = row['occasion'].strip()
            occasion_keywords[keyword] = occasion
    return occasion_keywords

# Extract from prompt using keyword mapping
def extract_occasions_from_keywords(prompt):
    occasion_keywords = load_occasion_keywords_from_csv()
    prompt_lower = prompt.lower()
    matched = set()
    for keyword, occasion in occasion_keywords.items():
        if keyword in prompt_lower:
            matched.add(occasion)
    return matched

# Fallback using spaCy NER
def extract_occasions_with_ner(prompt):
    doc = nlp(prompt)
    matched = set()
    for ent in doc.ents:
        if ent.label_ in ["EVENT", "ORG", "WORK_OF_ART"]:
            matched.add(ent.text.title())
    return matched

# Combined Hybrid Function
def get_matched_occasions(prompt):
    keyword_matches = extract_occasions_from_keywords(prompt)
    ner_matches = extract_occasions_with_ner(prompt)
    all_matches = keyword_matches.union(ner_matches)
    return list(all_matches)

def fuzzy_color_match(text):
    words = text.lower().split()
    matched_colors = []
    for word in words:
        best_match, score = process.extractOne(word, COLOR_LIST)
        if score > 85:
            matched_colors.append(best_match)
    return list(set(matched_colors))

def clean_prompt(prompt):
    # Clean prompt
    cleaned_prompt = prompt.lower()
    cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_prompt)
    cleaned_prompt = ' '.join([w for w in cleaned_prompt.split() if w not in STOP_WORDS])
    return cleaned_prompt

def extract_info(prompt):
    cleaned_prompt = clean_prompt(prompt)
    doc = nlp(cleaned_prompt)

    # Extract clothing items
    found_items = [item for item in CLOTHING_ITEMS if item in cleaned_prompt]

    # Extract colors using fuzzy match
    found_colors = fuzzy_color_match(cleaned_prompt)

    # Extract occasion using keyword mapping and NER Model
    found_occasions = get_matched_occasions(cleaned_prompt)

    # Extract time expressions
    time_expressions = [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]

    return {
        "clothing_items": list(set(found_items)),
        "colors": list(set(found_colors)),
        "occasions": list(set(found_occasions)),
        "time": time_expressions
    }

def load_dress_code_rules():
    df = pd.read_csv('../dataSets/dress_code_rules.csv')
    return dict(zip(df['occasion'], df['dress_code']))


def predict_dress_code(info):
    occasions = info.get("occasions", [])
    predicted_dress_codes = set()

    rules = load_dress_code_rules()

    for occasion in occasions:
        if occasion in rules:
            predicted_dress_codes.add(rules[occasion])

    if not predicted_dress_codes:
        predicted_dress_codes.add("Casual")  # Default fallback

    return list(predicted_dress_codes)

def load_clothing_items():
    df = pd.read_csv('../dataSets/dress_code_clothing_items.csv')
    return df

def predict_clothing_items(dress_codes):
    df = load_clothing_items()
    matched_items = df[df['dress_code'].isin(dress_codes)]['clothing_item'].unique()
    return list(matched_items)

text = "Next week is our project release and I have to do a presentation. What should I wear?"
info = extract_info(text)
print(info)

dress_codes = predict_dress_code(info)
print("Predicted Dress Code(s):", dress_codes)

clothing_items = predict_clothing_items(dress_codes)
print("Recommended Clothing Items:", clothing_items)
