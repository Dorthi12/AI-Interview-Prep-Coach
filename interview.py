from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.question_engine import QuestionEngine
from app.services.session_manager import SessionManager
from app.services.answer_evaluation import AnswerEvaluator


router = APIRouter(prefix="/interview", tags=["Interview"])

question_engine = QuestionEngine()
session_manager = SessionManager()
answer_evaluator = AnswerEvaluator()



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

class SubmitAnswerResponse(BaseModel):
    session_id: str
    relevance_score: float
    star_score : int
    confidence_score : int
    readiness_score: float
    feedback: list[str]

class SubmitAnswerRequest(BaseModel):
    session_id: str

    answer: str




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
@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_answer(request: SubmitAnswerRequest):
    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    # SAFETY: ensure answers list exists
    if "answers" not in session:
        session["answers"] = []

    # store answer
    session["answers"].append(request.answer)

    # ensure question exists
    if not session.get("questions"):
        raise HTTPException(status_code=400, detail="No question found for this session")

    question = session["questions"][-1]

    # evaluate answer
    evaluation = answer_evaluator.evaluate(question, request.answer)

    return {
        "session_id": request.session_id,
        "relevance_score": evaluation["relevance_score"],
        "star_score": evaluation["star_score"],
        "confidence_score": evaluation["confidence_score"],
        "readiness_score": evaluation["readiness_score"],
        "feedback": evaluation["feedback"]
    }
