import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

# Load datasets
df1 = pd.read_csv("dataSets/sample_dataset_1.csv")  # Dress Code Dataset
df2 = pd.read_csv("dataSets/sample_dataset_2.csv")  # Material - Weather Dataset
df3 = pd.read_csv("dataSets/sample_dataset_3.csv")  # Clothing Items - Occasion Dataset

# Print the column names and first few rows for debugging
print("====================================")
print("DF1 columns:", df1.columns)
print("DF2 columns:", df2.columns)
print("DF3 columns:", df3.columns)

# Check the content of clothing_items column in df3
print("====================================")
print("Clothing Items in DF3:", df3['clothing_items'].head())

# Check for any missing values in the clothing_items column
print("====================================")
print("Missing values in clothing_items:", df3['clothing_items'].isnull().sum())

# Standardize dataset formats
df1['category'] = 'dress_code'
df2['category'] = 'weather'
df3['category'] = 'occasion'

# Rename columns to match
df1.rename(columns={'context': 'dress_code'}, inplace=True)
df2.rename(columns={'weather': 'weather'}, inplace=True)
df3.rename(columns={'occasion': 'occasion', 'clothing_items': 'clothing_items'}, inplace=True)

# Print out the first few rows of the renamed datasets
print("====================================")
print(df1.to_string())
print("====================================")
print(df2.to_string())
print("====================================")
print(df3.to_string())
# print(df3.to_string())

# Merge datasets
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# Check the columns and first few rows after concatenation
print("====================================")
print("Combined DF columns:", combined_df.columns)
print("====================================")
print(combined_df.to_string())

# Check if the 'clothing_items' column is correctly populated
print("====================================")
print("Clothing Items in Combined DF:", combined_df['clothing_items'].head())

# Check for NaN values in the 'text' column
# print(combined_df['text'].isnull().sum())  # If it prints a non-zero value, we need to handle it

# Option 1: Drop rows with NaN values
# combined_df.dropna(subset=['text'], inplace=True)

# Option 2: Or, replace NaN values with an empty string
# combined_df['text'].fillna("", inplace=True)

# Combine all labels into one single DataFrame
combined_df['combined_label'] = combined_df['dress_code'] + ',' + combined_df['weather'] + ',' + combined_df['occasion'] + ',' + combined_df['clothing_items']

# Check the final combined dataframe
print("====================================")
print(combined_df.head())

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(combined_df['text'])

# Separate labels
y = combined_df['combined_label']

# Apply SMOTE for oversampling
# sm = SMOTE(random_state=42, k_neighbors=5)
# X_res, y_res = sm.fit_resample(X, y)

# Split into train-test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=1))

# Save the model and vectorizer
joblib.dump(model, "models/multi_task_model.pkl")
joblib.dump(vectorizer, "models/multi_task_vectorizer.pkl")
