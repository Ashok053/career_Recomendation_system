# train_models.py

import pandas as pd
import os
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Paths
DATA_DIR = 'data'
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

# Load Data
skill_df = pd.read_csv(f'{DATA_DIR}/skill_df.csv')
edited_df = pd.read_csv(f'{DATA_DIR}/edited_df.csv')

# Preprocess skill_df
skill_df['Skills'] = skill_df['Skills'].apply(lambda x: [s.strip().lower().replace(" ", "_") for s in eval(x)])
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(skill_df['Skills'])

# Nearest Neighbors Model
nn_model = NearestNeighbors(n_neighbors=3, metric='cosine')
nn_model.fit(X)

# Save Role Prediction Assets
joblib.dump(mlb, f'{MODEL_DIR}/skill_binarizer.pkl')
joblib.dump(nn_model, f'{MODEL_DIR}/nn_model.pkl')

# TF-IDF Vectorizer on job descriptions
edited_df['Cleaned_Description'] = edited_df['description'].fillna('').astype(str)
tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit(edited_df['Cleaned_Description'])

# Save TF-IDF
joblib.dump(tfidf, f'{MODEL_DIR}/tfidf_vectorizer.pkl')

print("✅ Models trained and saved successfully.")
