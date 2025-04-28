import pandas as pd

import init_data_array.data as data

def create_dataset_csv_files():
    # Convert to DataFrame
    dress_code_rules_df = pd.DataFrame(data.system_init_rules.dress_code_rules)
    clothing_item_dataset_df = pd.DataFrame(data.system_init_rules.clothing_item_dataset)
    material_weather_dataset_df = pd.DataFrame(data.system_init_rules.material_weather_dataset)
    occasion_color_palettes_df = pd.DataFrame(data.system_init_rules.occasion_color_palettes)
    occasion_keywords_df = pd.DataFrame(data.system_init_rules.occasion_keywords)
    dress_code_clothing_item_df = pd.DataFrame(data.system_init_rules.dress_code_clothing_item)

    # Save dataset to CSV
    dress_code_rules_df.to_csv(data.csv_file_names.dress_code_rules, index=False)
    clothing_item_dataset_df.to_csv(data.csv_file_names.clothing_item_dataset, index=False)
    material_weather_dataset_df.to_csv(data.csv_file_names.material_weather_dataset, index=False)
    occasion_color_palettes_df.to_csv(data.csv_file_names.occasion_color_palettes, index=False)
    occasion_keywords_df.to_csv(data.csv_file_names.occasion_keywords, index=False)
    dress_code_clothing_item_df.to_csv(data.csv_file_names.dress_code_clothing_item, index=False)
