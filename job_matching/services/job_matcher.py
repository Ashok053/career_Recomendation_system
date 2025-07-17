# job_matching/services/job_matcher.py

import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class JobMatcher:
    def __init__(self, edited_df: pd.DataFrame, model_dir: str = 'models'):
        self.edited_df = edited_df.copy()
        self.edited_df['Cleaned_Description'] = self.edited_df['Cleaned_Description'].fillna('').astype(str)
        self.vectorizer = joblib.load(f'{model_dir}/tfidf_vectorizer.pkl')

    def match(self, user_skills: List[str], top_k: int = 5) -> List[dict]:
        resume_text = " ".join(user_skills)
        all_docs = self.edited_df['Cleaned_Description'].tolist() + [resume_text]
        vectors = self.vectorizer.transform(all_docs)
        scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
        self.edited_df['tfidf_score'] = scores
        top_jobs = self.edited_df.sort_values(by='tfidf_score', ascending=False).head(top_k)
        return top_jobs[['Job Title', 'tfidf_score']].to_dict(orient='records')
