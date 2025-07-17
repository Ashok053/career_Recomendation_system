#main entry file
from fastapi import FastAPI

from job_matching.api.routes import router as job_matching_router
from api.routes.gateway import router as gateway_router
from api.routes.course_route import router as course_router

app = FastAPI(
    title="Career Recommendation Platform API",
    version="1.0.0"
)

# Include main API routes
app.include_router(gateway_router)         # Resume, job match, and course recommendation (offline)
app.include_router(job_matching_router)    # Job matching routes
app.include_router(course_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Career Recommendation API"}
