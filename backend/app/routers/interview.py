from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import time

from app.services.session_manager import SessionManager
from app.services.answer_evaluation import AnswerEvaluator
from app.services.analytics_engine import AnalyticsEngine
from app.services.improvement_plan import ImprovementPlanEngine
from app.services.report_generator import PDFReportGenerator
from app.services.local_llm import LocalLLM

router = APIRouter(prefix="/interview", tags=["Interview"])

session_manager = SessionManager()
answer_evaluator = AnswerEvaluator()
analytics_engine = AnalyticsEngine()
improvement_engine = ImprovementPlanEngine()
report_generator = PDFReportGenerator()
llm = LocalLLM()

# ---------- MODELS ----------

class StartInterviewRequest(BaseModel):
    role: str
    domain: str
    difficulty: str
    mode: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class EndInterviewRequest(BaseModel):
    session_id: str

# ---------- ROUTES ----------

@router.post("/start")
def start_interview(req: StartInterviewRequest):
    session = session_manager.create_session(
        role=req.role,
        domain=req.domain,
        difficulty=req.difficulty,
        mode=req.mode,
    )

    prompt = f"""
You are a professional technical interviewer.

Generate ONE clear interview question.

Role: {req.role}
Domain: {req.domain}
Difficulty: {req.difficulty}
Focus: {req.mode}

Rules:
- Ask only ONE question
- Open-ended
- Interview style
- No explanation
"""

    try:
        question = llm.generate(prompt).strip()
    except Exception as e:
        raise HTTPException(500, f"LLM failed to generate question: {e}")

    session["questions"].append(question)

    return {
        "session_id": session["session_id"],
        "question_number": 1,
        "question": question,
    }

@router.post("/answer")
def submit_answer(req: AnswerRequest):
    session = session_manager.get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Invalid session ID")

    last_question = session["questions"][-1]
    session["answers"].append(req.answer)

    evaluation = answer_evaluator.evaluate(last_question, req.answer)
    session["evaluations"].append(evaluation)

    followup_prompt = f"""
You are a senior interviewer.

Previous Question:
{last_question}

Candidate Answer:
{req.answer}

Evaluation Summary:
Correctness: {evaluation['correctness_score']}
Confidence: {evaluation['confidence_score']}

Ask ONE deeper follow-up interview question.
No explanations.
"""

    try:
        followup_question = llm.generate(followup_prompt).strip()
    except Exception as e:
        raise HTTPException(500, f"LLM failed to generate follow-up: {e}")

    session["questions"].append(followup_question)

    return {
        "relevance_score": evaluation["relevance_score"],
        "correctness_score": evaluation["correctness_score"],
        "confidence_score": evaluation["confidence_score"],
        "readiness_score": evaluation["readiness_score"],
        "feedback": evaluation["feedback"],
        "follow_up_question": followup_question,
    }

@router.post("/end")
def end_interview(req: EndInterviewRequest):
    session = session_manager.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid session")

    analytics = analytics_engine.generate_metrics(session["evaluations"])
    improvement = improvement_engine.generate_plan(session["evaluations"])

    pdf_path = report_generator.generate(
        session=session,
        analytics=analytics,
        improvement=improvement
    )

    return {
        "analytics": analytics,
        "improvement": improvement,
        "report_url": f"/interview/report/{req.session_id}"
    }

@router.get("/report/{session_id}")
def download_report(session_id: str):
    path = report_generator.get_path(session_id)
    return FileResponse(path, filename="Interview_Report.pdf")
