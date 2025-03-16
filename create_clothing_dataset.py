import pandas as pd

# Expanded dataset
clothing_items_data = [
    {"Clothing_Item": "Long Sleeve Shirt", "Dress_Codes": ["Formal", "Business Casual", "Smart Casual"], "Occasions": ["Office", "Meetings", "Dinner"]},
    {"Clothing_Item": "Short Sleeve Shirt", "Dress_Codes": ["Business Casual", "Smart Casual", "Casual"], "Occasions": ["Office", "Casual Outing", "Lunch"]},
    {"Clothing_Item": "Long Sleeve T-Shirt", "Dress_Codes": ["Casual", "Sporty", "Streetwear"], "Occasions": ["Casual Outing", "Sports Events", "Travel"]},
    {"Clothing_Item": "Short Sleeve T-Shirt", "Dress_Codes": ["Casual", "Sporty", "Beachwear"], "Occasions": ["Beach", "Gym", "Casual Outing"]},
    {"Clothing_Item": "Jean", "Dress_Codes": ["Casual", "Smart Casual"], "Occasions": ["Casual Outing", "Office", "Travel"]},
    {"Clothing_Item": "Trouser", "Dress_Codes": ["Formal", "Business Casual"], "Occasions": ["Office", "Formal Events", "Meetings"]},
    {"Clothing_Item": "Hoodie", "Dress_Codes": ["Casual", "Sporty", "Streetwear"], "Occasions": ["Casual Outing", "Sports Events", "Travel"]},
    {"Clothing_Item": "Short", "Dress_Codes": ["Casual", "Sporty", "Beachwear"], "Occasions": ["Beach", "Gym", "Casual Outing"]},
    {"Clothing_Item": "Leather Shoes", "Dress_Codes": ["Formal", "Business Casual"], "Occasions": ["Office", "Formal Events", "Meetings"]},
    {"Clothing_Item": "Casual Shoes", "Dress_Codes": ["Casual", "Smart Casual"], "Occasions": ["Casual Outing", "Travel", "Everyday Wear"]},
]

clothing_weather_conditions = [
    {"Material": "Cotton", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Linen", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Polyester", "Weather_Condition": ["Mild", "Cold"]},
    {"Material": "Denim", "Weather_Condition": ["Mild", "Cold"]},
    {"Material": "Wool", "Weather_Condition": ["Cold"]},
    {"Material": "Fleece", "Weather_Condition": ["Cold"]},
    {"Material": "Leather", "Weather_Condition": ["Any"]},
    {"Material": "Synthetic", "Weather_Condition": ["Any"]},
    {"Material": "Silk", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Rayon", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Nylon", "Weather_Condition": ["Mild", "Cold"]},
    {"Material": "Hemp", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Bamboo", "Weather_Condition": ["Hot", "Mild"]},
    {"Material": "Cashmere", "Weather_Condition": ["Cold"]},
    {"Material": "Flannel", "Weather_Condition": ["Cold"]},
    {"Material": "Corduroy", "Weather_Condition": ["Mild", "Cold"]},
    {"Material": "Canvas", "Weather_Condition": ["Any"]},
]

# Convert to DataFrame
clothing_item_data_frame = pd.DataFrame(clothing_items_data)
weather_condition_data_frame = pd.DataFrame(clothing_weather_conditions)

# Save dataset to CSV
clothing_item_data_frame.to_csv("./dataSets/expanded_clothing_dataset.csv", index=False)
weather_condition_data_frame.to_csv("./dataSets/expanded_weather_dataset.csv", index=False)

# Display the dataset
print(clothing_item_data_frame)
print(weather_condition_data_frame)
