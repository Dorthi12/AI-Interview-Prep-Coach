from fastapi import FastAPI
from app.routers import interview

app = FastAPI(
    title="AI Interview Prep Coach",
    version="1.0.0"
)

# ✅ THIS IS CRITICAL
app.include_router(interview.router)

@app.get("/")
def root():
    return {"status": "Backend running"}
