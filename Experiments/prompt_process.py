# import spacy
# import webcolors
# from nltk.corpus import wordnet as wn
# import joblib
# import sys
# import os
#
# this_dir = os.path.dirname(__file__) # Path to loader.py
# # sys.path.append(os.path.join(this_dir, <rel_path_to_foo.py>))
# # Load spaCy model
# nlp = spacy.load('en_core_web_lg')
# # Define a custom clothing keyword list
# custom_clothing_keywords = ["jeans", "shoes", "shirt", "trousers", "jacket", "dress", "blouse", "skirt",
#                             "pants", "sneakers", "suit", "tie", "coat", "sweater", "hoodie", "boots", "trouser"]
# # Define a list of color modifiers
# color_modifiers = ["dark", "light", "bright", "pale"]
#
# # WordNet check for clothing-related words
# def is_clothing_item(word):
#     """Check if the word is in the custom list or related to clothing using WordNet."""
#     if word.lower() in custom_clothing_keywords:
#         return True
#     for synset in wn.synsets(word):
#         if 'clothing' in synset.lexname() or 'wear' in synset.lexname():
#             return True
#     return False
#
# # Use webcolors to find the closest color name for a given color word
# def get_basic_color_name(color):
#     try:
#         return webcolors.name_to_rgb(color.lower())
#     except ValueError:
#         return None
#
# def process_text(data):
#     # Get prompt from request data object
#     user_input = data["prompt"]
#     # Process the input with spaCy
#     doc = nlp(user_input)
#     # Extract basic entities
#     entities = [(ent.text, ent.label_) for ent in doc.ents]
#     # Detect context (e.g., "casual", "formal")
#     context = "casual"
#     if any(keyword in user_input.lower() for keyword in ["office", "formal", "business", "work"]):
#         context = "formal"
#     if any(keyword in user_input.lower() for keyword in ["smart casual", "Smart", "night event", "party",
#                                                          "friends gathering"]):
#         context = "smart casual"
#     if any(keyword in user_input.lower() for keyword in ["family event", "casual"]):
#         context = "casual"
#     # Extract clothing items and colors dynamically
#     clothing_items = []
#     current_color = None
#     color_modifier = None
#     for token in doc:
#         # Check if the word is a color modifier (e.g., "dark", "light")
#         if token.text.lower() in color_modifiers:
#             color_modifier = token.text.lower()
#         # Detect basic color names using webcolors
#         color = get_basic_color_name(token.text)
#         if color:
#             current_color = token.text.lower()
#             # If there's a modifier (like "dark"), combine it with the color
#             if color_modifier:
#                 current_color = f"{color_modifier} {current_color}"
#                 color_modifier = None  # Reset modifier after using it
#         # Check if the word is a clothing item (either in the custom list or using WordNet)
#         if token.pos_ == "NOUN" and is_clothing_item(token.text.lower()):
#             item = {
#                 "item": token.text,
#                 "color": current_color if current_color else "unknown"  # Attach color to clothing item
#             }
#             clothing_items.append(item)
#             current_color = None  # Reset after assigning the color to the item
#     return {
#         "input_text": user_input,
#         "context": context,
#         "entities": entities,
#         "clothing_items": clothing_items  # Now includes both clothing items and colors
#     }, 200
#
# def process_text_with_model(data):
#     # Load the trained model and vectorizer
#     model = joblib.load(os.path.join(this_dir, "../models/poc_model.pkl"))
#     vectorizer = joblib.load(os.path.join(this_dir,"../models/poc_vectorizer.pkl"))
#     user_input = data["prompt"]
#     # Transform input text
#     X_input = vectorizer.transform([user_input])
#     # Predict the context
#     context = model.predict(X_input)[0]
#     return {"input_text": user_input, "context": context}, 200
#
# # def process_text_with_multi_data_model(data):
# #     # Load model and vectorizer
# #     model = joblib.load("models/multi_task_model.pkl")
# #     vectorizer = joblib.load("models/multi_task_vectorizer.pkl")
# #     user_input = data["prompt"]
# #     X_input = vectorizer.transform([user_input])
# #     # Predict the category
# #     prediction = model.predict(X_input)[0]
# #     return {"input_text": user_input, "predicted_label": prediction}, 200
#
# def process_text_with_multi_data_model(data):
#     # Load model and vectorizer
#     model = joblib.load("models/Closit-Model-1.pickle")
#     vectorizer = joblib.load("models/Closit-Model-1-vectorizer.pickle")
#     user_input = data["prompt"]
#     X_input = vectorizer.transform([user_input])
#     # Predict the category
#     prediction = model.predict(X_input)[0]
#     return {"input_text": user_input, "predicted_label": prediction}, 200
#
# def predict_all(data):
#     user_input = data["prompt"]
#     # Load and predict with Dress Code model
#     dress_code_model = joblib.load("models/dress_code_model.pkl")
#     dress_code_vectorizer = joblib.load("models/dress_code_vectorizer.pkl")
#     dress_code_input = dress_code_vectorizer.transform([user_input])
#     dress_code_prediction = dress_code_model.predict(dress_code_input)[0]
#     # Load and predict with Weather model
#     weather_model = joblib.load("models/weather_model.pkl")
#     weather_vectorizer = joblib.load("models/weather_vectorizer.pkl")
#     weather_input = weather_vectorizer.transform([user_input])
#     weather_prediction = weather_model.predict(weather_input)[0]
#     # Load and predict with Occasion model
#     occasion_model = joblib.load("models/occasion_model.pkl")
#     occasion_vectorizer = joblib.load("models/occasion_vectorizer.pkl")
#     occasion_input = occasion_vectorizer.transform([user_input])
#     occasion_prediction = occasion_model.predict(occasion_input)[0]
#     return {
#         "input_text": user_input,
#         "predictions": {
#             "dress_code": dress_code_prediction,
#             "weather": weather_prediction,
#             "occasion": occasion_prediction
#         }
#     }
#
#
