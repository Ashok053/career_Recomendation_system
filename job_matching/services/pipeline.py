
# job_matching/services/pipeline.py

import pandas as pd
from typing import List, Dict, Any
import os

from job_matching.services.role_predictor import RolePredictor
from job_matching.services.skill_gap import SkillGapAnalyzer
from job_matching.services.job_matcher import JobMatcher

# Define paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../data'))
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../models'))

# Load data
skill_df = pd.read_csv(os.path.join(DATA_DIR, 'skill_df_41.csv'))
edited_df = pd.read_csv(os.path.join(DATA_DIR, 'edited_df.csv'))

# Load trained models via services
role_model = RolePredictor(skill_df, model_dir=MODEL_DIR)
job_matcher = JobMatcher(edited_df, model_dir=MODEL_DIR)

def run_pipeline(user_skills: List[str]) -> Dict[str, Any]:
    """
    Main pipeline function for job role prediction, skill gap analysis, and job matching.
    """
    # Step 1: Predict Top Roles
    top_roles = role_model.predict_roles(user_skills)

    # Step 2: For each role, find missing skills
    role_skill_map = {
        role: role_model.get_required_skills_for_role(role) for role in top_roles
    }

    # Step 3: Compute Skill Gaps
    skill_gaps = SkillGapAnalyzer.analyze_multiple(user_skills, role_skill_map)

    # Step 4: Recommend Matching Jobs
    matched_jobs = job_matcher.match(user_skills)

    return {
        "top_roles": top_roles,
        "skill_gap_analysis": skill_gaps,
        "recommended_jobs": matched_jobs,
        "message": "Success"
    }
