from fastapi import FastAPI
from app.routers import interview

app = FastAPI(title="AI Interview Prep Coach")

app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "AI Interview Prep Coach backend is running"}
