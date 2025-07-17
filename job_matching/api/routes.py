# job_matching/api/v1/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from job_matching.services.pipeline import run_pipeline

router = APIRouter()

class ResumeInput(BaseModel):
    skills: List[str]

@router.post("/job-matching/")
def match_job_and_analyze(input: ResumeInput) -> Dict[str, Any]:
    if not input.skills:
        raise HTTPException(status_code=400, detail="Skills list cannot be empty")

    return run_pipeline(input.skills)
