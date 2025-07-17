
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import os

from resume_parser.apps.services.resume_pipeline import parse_resume_file
from job_matching.services.pipeline import run_pipeline
from courses.model_loader import load_models
from courses.recommend import recommend_top_n_courses

router = APIRouter(tags=["Resume + Job Matching + Course Recommendation"])

# Load model once
vectorizer, df_courses = load_models()

@router.post("/full-analysis/")
async def full_resume_analysis(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        filename = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(filename, "wb") as f:
            f.write(await file.read())

        # Resume Parsing
        parsed = parse_resume_file(filename)
        skills = parsed.get("extracted_skills", [])
        if not skills:
            raise ValueError("No skills extracted from resume.")

        # Job Matching + Skill Gap
        job_results = run_pipeline(skills)

        # Extract all missing skills
        missing_skills = []
        for gaps in job_results.get("skill_gap_analysis", {}).values():
            missing_skills.extend(gaps)

        unique_missing_skills = list(set(missing_skills))



        # Course Recommendations
        coursera_courses = recommend_top_n_courses(unique_missing_skills, df_courses, vectorizer, top_n=5)

        return {
            "parsed_resume": parsed,
            **job_results,
            "course_recommendations": {
                "coursera": coursera_courses.to_dict(orient="records"),

            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")
