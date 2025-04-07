# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report
# import joblib
# from collections import Counter
# from imblearn.over_sampling import SMOTE
#
# # Load the dataset
# df = pd.read_csv("dataSets/sample_dataset_1.csv")
#
# # Extract features and labels
# X = df['text']
# y = df['context']
#
# # Convert text to numerical features using TF-IDF
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(X)
#
# # Synthetic Minority Oversampling Technique
# sm = SMOTE(random_state=42, k_neighbors=5)
# X_res, y_res = sm.fit_resample(X, y)
#
# # Split into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
#
#
# print(Counter(y_train))
# # Train a Logistic Regression model
# model = LogisticRegression()
# model.fit(X_train, y_train)
#
# # Evaluate the model
# y_pred = model.predict(X_test)
# # print(classification_report(y_test, y_pred))
#
# print(classification_report(y_test, model.predict(X_test), zero_division=1))
#
#
# # Save the model and vectorizer for Flask integration
# joblib.dump(model, "models/poc_model.pkl")
# joblib.dump(vectorizer, "models/poc_vectorizer.pkl")
