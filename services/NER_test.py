import requests
import random
from transformers import pipeline

# Load pretrained NER model (Example: SpaCy, BERT-based NER model from Hugging Face)
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

# Sample wardrobe database (Replace this with actual DB query)
user_wardrobe = [
    {"category": "shirt", "color": "white", "material": "cotton", "dress_codes": ["business formal"],
     "occasions": ["job interview"], "weather": ["cold", "moderate"]},
    {"category": "trousers", "color": "black", "material": "wool", "dress_codes": ["business formal"],
     "occasions": ["job interview"], "weather": ["cold", "moderate"]},
    {"category": "shoes", "color": "black", "material": "leather", "dress_codes": ["business formal"],
     "occasions": ["job interview"], "weather": ["cold", "moderate"]},
]

# Weather-based clothing adjustments
weather_clothing_adjustments = {
    "cold": ["hoodie", "trousers", "boots"],
    "hot": ["t-shirt", "shorts", "sneakers"],
    "rainy": ["waterproof jacket", "trousers", "waterproof shoes"],
    "windy": ["windbreaker", "jeans", "sneakers"],
    "snowy": ["coat", "trousers", "boots"],
    "humid": ["light t-shirt", "shorts", "sneakers"],
    "foggy": ["sweater", "jeans", "boots"],
    "stormy": ["raincoat", "trousers", "waterproof shoes"]
}

# Clothing options categorized by dress code
clothing_item_mapping = {
    "business formal": ["shirt", "trousers", "blazer", "shoes"],
    "formal": ["shirt", "trousers", "dress shoes"],
    "casual": ["t-shirt", "jeans", "sneakers"],
    "smart casual": ["shirt", "jeans", "loafers"],
    "business casual": ["shirt", "trousers", "blazer", "shoes"],
    "sportswear": ["t-shirt", "shorts", "running shoes"],
    "beachwear": ["t-shirt", "shorts", "sandals"],
    "black formal": ["black shirt", "black trousers", "shoes"],
    "cocktail attire": ["shirt", "trousers", "dress shoes"],
    "resort casual": ["linen shirt", "shorts", "sandals"]
}

# Keyword mapping for occasion & dress code extraction
keyword_mapping = {
    "job interview": "business formal",
    "wedding": "formal",
    "party": "smart casual",
    "gym": "sportswear",
    "beach": "beachwear",
    "meeting": "business casual",
    "casual outing": "casual",
    "dinner": "cocktail attire"
}


# Function to extract details using NER + Keyword Mapping
def extract_details_from_prompt(user_prompt):
    extracted_details = {"occasion": "general", "dress_code": "casual"}

    # Extract Named Entities (NER Model)
    ner_results = ner_pipeline(user_prompt)

    # Process NER Results
    for entity in ner_results:
        word = entity["word"].lower()
        if word in keyword_mapping:
            extracted_details["occasion"] = word
            extracted_details["dress_code"] = keyword_mapping[word]

    return extracted_details


# Fetch weather data (Replace with an actual API Key)
def get_weather(city):
    API_KEY = "fd8ad02cb1d2f2f552bd87d4f9728f24"  # Replace with your API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        weather_conditions = data["weather"][0]["main"].lower()

        # Map OpenWeather API conditions to predefined categories
        weather_mapping = {
            "clear": "hot",
            "clouds": "moderate",
            "rain": "rainy",
            "drizzle": "rainy",
            "thunderstorm": "stormy",
            "snow": "snowy",
            "mist": "foggy",
            "smoke": "foggy",
            "haze": "humid",
            "dust": "windy",
            "fog": "foggy"
        }
        return weather_mapping.get(weather_conditions, "moderate")
    except Exception as e:
        print(f"⚠️ Weather API Error: {e}")
        return "moderate"  # Default to moderate weather


# Search algorithm to find the best outfit
def find_best_outfit(extracted_info, weather):
    dress_code = extracted_info["dress_code"]
    base_clothing = clothing_item_mapping.get(dress_code, ["t-shirt", "jeans", "sneakers"])

    if weather in weather_clothing_adjustments:
        adjusted_clothing = list(set(base_clothing + weather_clothing_adjustments[weather]))
    else:
        adjusted_clothing = base_clothing

    # Scoring system to prioritize best matches
    clothing_scores = {item: 10 if item in base_clothing else 5 for item in adjusted_clothing}

    # Sort and return best & alternative suggestions
    best_outfit = sorted(clothing_scores, key=clothing_scores.get, reverse=True)

    return best_outfit[:4], best_outfit[4:7]  # Top 4 as best match, next 3 as alternatives


# Check user's wardrobe and prioritize owned clothing
def check_wardrobe(predicted_outfit):
    owned_items = [item["category"] for item in user_wardrobe]
    recommended_from_wardrobe = [item for item in predicted_outfit if item in owned_items]
    need_to_buy = [item for item in predicted_outfit if item not in owned_items]

    return recommended_from_wardrobe, need_to_buy


# Main function: integrate all parts
def recommend_outfit(user_prompt, city):
    extracted_info = extract_details_from_prompt(user_prompt)
    weather_info = get_weather(city)

    extracted_info["weather"] = weather_info

    # Get best outfit and alternatives
    best_match, alternatives = find_best_outfit(extracted_info, extracted_info["weather"])

    # Check wardrobe
    owned_clothes, clothes_to_buy = check_wardrobe(best_match)

    return {
        "occasion": extracted_info["occasion"],
        "dress_code": extracted_info["dress_code"],
        "weather": extracted_info["weather"],
        "best_outfit": best_match,
        "alternative_suggestions": alternatives,
        "wardrobe_suggestions": owned_clothes,
        "items_to_buy": clothes_to_buy
    }


# Example usage
user_prompt = "I have a job interview tomorrow morning. What should I wear?"
city = "Colombo"
final_recommendation = recommend_outfit(user_prompt, city)

# Output the final results
print("🎯 Best Outfit:", final_recommendation["best_outfit"])
print("🔄 Alternative Suggestions:", final_recommendation["alternative_suggestions"])
print("👕 Items in Your Wardrobe:", final_recommendation["wardrobe_suggestions"])
print("🛒 Items to Buy:", final_recommendation["items_to_buy"])
print("🌤 Weather Condition:", final_recommendation["weather"])
