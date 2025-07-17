import os
import joblib
import pandas as pd

# Absolute path to project root from this file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")  # 🔥 'model' is at the project root

VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer_course.joblib")
COURSES_DF_PATH = os.path.join(MODEL_DIR, "coursera_courses.pkl")

# Globals to cache loaded model and data
_vectorizer = None
_courses_df = None

def load_vectorizer():
    global _vectorizer
    if _vectorizer is None:
        _vectorizer = joblib.load(VECTORIZER_PATH)
    return _vectorizer

def load_courses_df():
    global _courses_df
    if _courses_df is None:
        _courses_df = pd.read_pickle(COURSES_DF_PATH)
    return _courses_df

def load_models():
    """
    Load vectorizer and courses dataframe once, cache them.
    """
    vectorizer = load_vectorizer()
    df = load_courses_df()
    return vectorizer, df
