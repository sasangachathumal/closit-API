import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
from imblearn.over_sampling import SMOTE
from collections import Counter


def train_classifier_with_smote(dataset_path, text_column, label_column, model_name):
    # Load the dataset
    df = pd.read_csv(dataset_path)

    # Extract features and labels
    X = df[text_column]
    y = df[label_column]

    # Convert text to numerical features using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Apply SMOTE to balance the data
    sm = SMOTE(random_state=42, k_neighbors=5)
    X_res, y_res = sm.fit_resample(X, y)
    print(f"Class distribution after SMOTE for {model_name}: {Counter(y_res)}")

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

    # Train the model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Classification Report for {model_name}:")
    print(classification_report(y_test, y_pred, zero_division=1))

    # Save the model and vectorizer
    joblib.dump(model, f"models/{model_name}_model.pkl")
    joblib.dump(vectorizer, f"models/{model_name}_vectorizer.pkl")


# Train separate classifiers
train_classifier_with_smote("dataSets/sample_dataset_1.csv", "text", "context", "dress_code")
train_classifier_with_smote("dataSets/sample_dataset_2.csv", "text", "weather", "weather")
train_classifier_with_smote("dataSets/sample_dataset_3.csv", "text", "occasion", "occasion")
