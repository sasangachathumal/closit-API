import json
import os
import random
import spacy
import re

this_dir = os.path.dirname(__file__)

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# basic synonym dictionary
synonyms = {
    "hiya": "hi",
    "thanks": "thank you",
    "bye": "goodbye",
    "morning": "hello",
    "what is your name": "what's your name",
    "who are you": "who are you"
}

# Load intents from JSON file
def load_intents():
    path = os.path.join(this_dir, '../dataSets/intents.json')
    with open(path, "r") as file:
        data = json.load(file)
        return data["intents"]


# Clean and normalize text
def preprocess(text):
    # Replace synonyms
    for word, replacement in synonyms.items():
        text = text.lower().replace(word, replacement)

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Process with spaCy
    doc = nlp(text)

    # Filter tokens: keep only lemmatized, alphabetic, non-stopword
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)


# Function to get the best matching intent using similarit
def predict_intent(prompt):
    user_input_clean = preprocess(prompt)
    doc1 = nlp(user_input_clean)

    intents = load_intents()

    best_score = 0.0
    best_tag = None

    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_clean = preprocess(pattern)
            doc2 = nlp(pattern_clean)
            # Ignore empty patterns (just in case)
            if not pattern_clean.strip():
                continue
            similarity = doc1.similarity(doc2)
            # Add an extra condition: pattern and prompt must not be too different in length
            length_difference = abs(len(user_input_clean) - len(pattern_clean))

            if similarity > best_score and length_difference < 20:
                best_score = similarity
                best_tag = intent["tag"]

    return best_tag if best_score > 0.8 else "unknown"


# Function to get a random response for a matched intent
def get_response(tag):
    intents = load_intents()
    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return tag

def fallback():
    intents = load_intents()
    # Return a random fallback response
    for intent in intents:
        if intent["tag"] == "fallback":
            return random.choice(intent["responses"])
    return "I'm not sure how to respond to that."  # hard fallback

def get_intent_response(prompt):
    tag = predict_intent(prompt)
    response = get_response(tag)
    return response
