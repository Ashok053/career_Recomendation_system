from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any

from courses.model_loader import load_models
from courses.recommend import recommend_top_n_courses

router = APIRouter(tags=["Course Recommendation"])

vectorizer, df_courses = load_models()

@router.get("/course-recommendation")
async def recommend_courses(
    keywords: List[str] = Query(..., description="List of skill keywords")
) -> Dict[str, Any]:
    try:
        coursera = recommend_top_n_courses(keywords, df_courses, vectorizer, top_n=5)

        return {
            "message": "Success",
            "course_recommendations": {
                "coursera": coursera.to_dict(orient="records"),

            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Course recommendation failed: {str(e)}")
