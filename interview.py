from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.question_engine import QuestionEngine
from app.services.session_manager import SessionManager

router = APIRouter(prefix="/interview", tags=["Interview"])

question_engine = QuestionEngine()
session_manager = SessionManager()


# ---------- MODELS ----------

class InterviewStartRequest(BaseModel):
    role: str


class InterviewStartResponse(BaseModel):
    session_id: str
    role: str
    question: str


class NextQuestionRequest(BaseModel):
    session_id: str


class NextQuestionResponse(BaseModel):
    session_id: str
    question_number: int
    question: str


# ---------- ROUTES ----------

@router.post("/start", response_model=InterviewStartResponse)
def start_interview(request: InterviewStartRequest):
    try:
        session = session_manager.create_session(request.role.lower())
        question = question_engine.get_question(request.role)

        session_id = session["session_id"]
        session_manager.sessions[session_id]["questions"].append(question)

        return {
            "session_id": session_id,
            "role": request.role.lower(),
            "question": question
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/next", response_model=NextQuestionResponse)
def next_question(request: NextQuestionRequest):
    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    question = question_engine.get_question(session["role"])

    session["questions"].append(question)
    session["current_index"] += 1

    return {
        "session_id": request.session_id,
        "question_number": session["current_index"] + 1,
        "question": question
    }
