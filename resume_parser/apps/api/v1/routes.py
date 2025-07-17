#resume_parser.aps.api.v1.routes.py
from fastapi import APIRouter, UploadFile, File
import os
from datetime import datetime
from resume_parser.apps.services.resume_pipeline import parse_resume_file

router = APIRouter()


@router.post("/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    path = f"temp/{filename}"
    os.makedirs("temp", exist_ok=True)

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        parsed = parse_resume_file(path)
        return parsed
    except Exception as e:
        return {"error": str(e)}
