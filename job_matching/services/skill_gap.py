# job_matching/services/skill_gap.py

from typing import List, Dict

class SkillGapAnalyzer:
    @staticmethod
    def compute(user_skills: List[str], role_skills: List[str]) -> List[str]:
        user_skills_cleaned = set(s.strip().lower().replace(" ", "_") for s in user_skills)
        role_skills_cleaned = set(s.strip().lower().replace(" ", "_") for s in role_skills)
        return list(role_skills_cleaned - user_skills_cleaned)

    @staticmethod
    def analyze_multiple(user_skills: List[str], role_skill_map: Dict[str, List[str]]) -> Dict[str, List[str]]:
        result = {}
        for role, skills in role_skill_map.items():
            result[role] = SkillGapAnalyzer.compute(user_skills, skills)
        return result
