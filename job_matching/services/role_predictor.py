# job_matching/services/role_predictor.py

import joblib
from typing import List
import pandas as pd

class RolePredictor:
    def __init__(self, skill_df: pd.DataFrame, model_dir: str = 'models'):
        self.skill_df = skill_df.copy()
        self.skill_df['Skills'] = self.skill_df['Skills'].apply(lambda x: [s.strip().lower().replace(" ", "_") for s in eval(x)])
        self.skill_df['Roles'] = self.skill_df['Roles'].apply(lambda x: [s.strip().lower().replace(" ", "_") for s in str(x).split(',')])

        self.mlb = joblib.load(f'{model_dir}/skill_binarizer.pkl')
        self.nn_model = joblib.load(f'{model_dir}/nn_model.pkl')

    def predict_roles(self, user_skills: List[str]) -> List[str]:
        user_cleaned = [s.strip().lower().replace(" ", "_") for s in user_skills]
        valid_skills = [s for s in user_cleaned if s in self.mlb.classes_]
        if not valid_skills:
            return []
        user_vec = self.mlb.transform([valid_skills])
        _, indices = self.nn_model.kneighbors(user_vec)
        roles = set()
        for idx in indices[0]:
            roles.update(self.skill_df.iloc[idx]['Roles'])
        return list(roles)

    def get_required_skills_for_role(self, role: str) -> List[str]:
        match = self.skill_df[self.skill_df['Roles'].apply(lambda r: role in r)]
        return match.iloc[0]['Skills'] if not match.empty else []
