import spacy
import webcolors
from nltk.corpus import wordnet as wn
import joblib
import sys
import os


this_dir = os.path.dirname(__file__) # Path to loader.py
# sys.path.append(os.path.join(this_dir, <rel_path_to_foo.py>))

# Load spaCy model
nlp = spacy.load('en_core_web_md')

# Define a custom clothing keyword list
custom_clothing_keywords = ["jeans", "shoes", "shirt", "trousers", "jacket", "dress", "blouse", "skirt",
                            "pants", "sneakers", "suit", "tie", "coat", "sweater", "hoodie", "boots", "trouser"]

# Define a list of color modifiers
color_modifiers = ["dark", "light", "bright", "pale"]


# WordNet check for clothing-related words
def is_clothing_item(word):
    """Check if the word is in the custom list or related to clothing using WordNet."""
    if word.lower() in custom_clothing_keywords:
        return True
    for synset in wn.synsets(word):
        if 'clothing' in synset.lexname() or 'wear' in synset.lexname():
            return True
    return False


# Use webcolors to find the closest color name for a given color word
def get_basic_color_name(color):
    try:
        return webcolors.name_to_rgb(color.lower())
    except ValueError:
        return None


def process_text(data):
    # Get prompt from request data object
    user_input = data["prompt"]

    # Process the input with spaCy
    doc = nlp(user_input)

    # Extract basic entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Detect context (e.g., "casual", "formal")
    context = "casual"
    if any(keyword in user_input.lower() for keyword in ["office", "formal", "business", "work"]):
        context = "formal"
    if any(keyword in user_input.lower() for keyword in ["smart casual", "Smart", "night event", "party",
                                                         "friends gathering"]):
        context = "smart casual"
    if any(keyword in user_input.lower() for keyword in ["family event", "casual"]):
        context = "casual"

    # Extract clothing items and colors dynamically
    clothing_items = []
    current_color = None
    color_modifier = None

    for token in doc:
        # Check if the word is a color modifier (e.g., "dark", "light")
        if token.text.lower() in color_modifiers:
            color_modifier = token.text.lower()

        # Detect basic color names using webcolors
        color = get_basic_color_name(token.text)
        if color:
            current_color = token.text.lower()

            # If there's a modifier (like "dark"), combine it with the color
            if color_modifier:
                current_color = f"{color_modifier} {current_color}"
                color_modifier = None  # Reset modifier after using it

        # Check if the word is a clothing item (either in the custom list or using WordNet)
        if token.pos_ == "NOUN" and is_clothing_item(token.text.lower()):
            item = {
                "item": token.text,
                "color": current_color if current_color else "unknown"  # Attach color to clothing item
            }
            clothing_items.append(item)
            current_color = None  # Reset after assigning the color to the item

    return {
        "input_text": user_input,
        "context": context,
        "entities": entities,
        "clothing_items": clothing_items  # Now includes both clothing items and colors
    }, 200


def process_text_with_model(data):
    # Load the trained model and vectorizer
    model = joblib.load(os.path.join(this_dir, "../models/poc_model.pkl"))
    vectorizer = joblib.load(os.path.join(this_dir,"../models/poc_vectorizer.pkl"))
    user_input = data["prompt"]

    # Transform input text
    X_input = vectorizer.transform([user_input])

    # Predict the context
    context = model.predict(X_input)[0]

    return {"input_text": user_input, "context": context}, 200

