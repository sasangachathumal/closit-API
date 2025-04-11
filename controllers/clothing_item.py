from database.models import db, Users, ClothingItem, ClothingItemWeather, ClothingItemOccasion, ClothingItemDressCode

def get_user_wardrobe(user_id):
    clothing_items_array = []
    # fetch the clothing items of user
    clothing_items = ClothingItem.query.filter_by(userId=user_id).all()
    if len(clothing_items) <= 0:
        return clothing_items_array

    for clothingItem in clothing_items:
        # fetch the clothing item dress codes
        clothing_item_dress_codes = ClothingItemDressCode.query.filter_by(clothingItemId=clothingItem.id).all()
        # fetch the clothing item occasions
        clothing_item_occasions = ClothingItemOccasion.query.filter_by(clothingItemId=clothingItem.id).all()
        # fetch the clothing item weathers
        clothing_item_weathers = ClothingItemWeather.query.filter_by(clothingItemId=clothingItem.id).all()
        # create dress code array
        clothing_item_dress_codes_array = [dc.dressCode for dc in clothing_item_dress_codes]
        # create occasion array
        clothing_item_occasions_array = [oc.occasion for oc in clothing_item_occasions]
        # create weather array
        clothing_item_weather_array = [w.weather for w in clothing_item_weathers]
        clothing_items_array.append(
            {
                'id': clothingItem.id,
                'userId': clothingItem.userId,
                'category': clothingItem.category,
                'colorCode': clothingItem.colorCode,
                'material': clothingItem.material,
                'dressCodes': clothing_item_dress_codes_array,
                'occasions': clothing_item_occasions_array,
                'weather': clothing_item_weather_array
            }
        )
    return clothing_items_array

def get_all_clothing_items_by_user(user_id):
    return ClothingItem.query.filter_by(userId=user_id).all()

# fetch the clothing item
def get_clothing_item_by_id(clothing_id):
    return ClothingItem.query.filter_by(id=clothing_id).first()

# fetch the clothing item dress codes
def get_all_dress_codes_by_clothing_id(clothing_id):
    return ClothingItemDressCode.query.filter_by(clothingItemId=clothing_id).all()

# fetch the clothing item occasions
def get_all_occasions_by_clothing_id(clothing_id):
    return ClothingItemOccasion.query.filter_by(clothingItemId=clothing_id).all()

# fetch the clothing item weathers
def get_all_weather_conditions_by_clothing_id(clothing_id):
    return ClothingItemWeather.query.filter_by(clothingItemId=clothing_id).all()

def save_new_dress_code(dress_code, clothing_id):
    db.session.add(
        ClothingItemDressCode(
            clothingItemId=clothing_id,
            dressCode=dress_code
        )
    )
    db.session.flush()

def save_new_occasion(occasion, clothing_id):
    db.session.add(
        ClothingItemOccasion(
            clothingItemId=clothing_id,
            occasion=occasion
        )
    )
    db.session.flush()

def save_new_weather_condition(weather, clothing_id):
    db.session.add(
        ClothingItemWeather(
            clothingItemId=clothing_id,
            weather=weather
        )
    )
    db.session.flush()

def save_new_clothing_item(data, user_id, clothing_attributes):
    new_clothing_item = ClothingItem(
        userId=user_id,
        category=data['category'],
        colorCode=data['colorCode'],
        material=data['material']
    )
    db.session.add(new_clothing_item)
    # Flush to get the new User
    db.session.flush()

    if new_clothing_item.id:
        # create clothing item dress codes
        for dressCode in clothing_attributes['Dress_Codes']:
            save_new_dress_code(dressCode, new_clothing_item.id)
        # create clothing item occasions
        for occasion in clothing_attributes['Occasions']:
            save_new_occasion(occasion, new_clothing_item.id)
        # create clothing item weather
        for weather in clothing_attributes['Weather_Conditions']:
            save_new_weather_condition(weather, new_clothing_item.id)
    # Commit changes to the database
    db.session.commit()

    return new_clothing_item

def match_recommendations_to_wardrobe(wardrobe, predicted_items, filters):
    matched = []
    missing = []

    for item in predicted_items:
        found = False
        for wardrobe_item in wardrobe:
            if wardrobe_item["category"].lower() != item.lower():
                continue

            # Match dress code
            if filters.get("dress_codes"):
                if not set(wardrobe_item["dressCodes"]) & set(filters["dress_codes"]):
                    continue

            # Match occasion
            if filters.get("occasions"):
                if not set(wardrobe_item["occasions"]) & set(filters["occasions"]):
                    continue

            # Optional: Match weather
            if filters.get("weather"):
                if not set(wardrobe_item["weather"]) & set(filters["weather"]):
                    continue

            # Optional: color match
            if filters.get("colors"):
                if wardrobe_item["colorCode"] not in filters["colors"]:
                    continue

            # Optional: material match
            if filters.get("materials"):
                if wardrobe_item["material"] not in filters["materials"]:
                    continue

            matched.append(wardrobe_item)
            found = True
            break

        if not found:
            missing.append(item)

    return matched, missing
