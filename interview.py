from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.question_engine import QuestionEngine
from app.services.session_manager import SessionManager
from app.services.answer_evaluation import AnswerEvaluator
#from app.services.llm_question_generator import LLMQuestionGenerator
from app.services.local_llm import LocalLLM
from app.services.followup_engine import FollowUpEngine
from app.services.improvement_plan import ImprovementPlanEngine
from app.services.analytics_engine import AnalyticsEngine
from app.services.voice_engine import VoiceEngine

voice_engine = VoiceEngine()
router = APIRouter(prefix="/interview", tags=["Interview"])

question_engine = QuestionEngine()
session_manager = SessionManager()
answer_evaluator = AnswerEvaluator()
#llm_question_generator = LLMQuestionGenerator()
local_llm = LocalLLM()
followup_engine = FollowUpEngine()
improvement_engine = ImprovementPlanEngine()
analytics_engine = AnalyticsEngine()



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
    # 1️⃣ Create session
    session = session_manager.create_session(request.role.lower())
    session_id = session["session_id"]

    # 2️⃣ Ollama prompt (clean + interview-focused)
    prompt = f"""
You are a professional interview coach.

Generate ONE interview question for the role:
{request.role}

Guidelines:
- Clear and concise
- Realistic interview-style question
- Open-ended (not yes/no)
- Suitable for a mock interview

Return ONLY the question text.
"""

    # 3️⃣ Generate question using Ollama
    try:
        question = local_llm.generate(prompt)
        print("✅ Ollama question generated (start)")
    except Exception as e:
        # 4️⃣ Fallback (never break the system)
        print("⚠️ Ollama failed, using fallback:", e)
        question = question_engine.get_question(request.role)

    # 5️⃣ Store question in session
    session_manager.sessions[session_id]["questions"].append(question)

    # 6️⃣ Return response
    return {
        "session_id": session_id,
        "role": request.role.lower(),
        "question": question
    }
@router.post("/next", response_model=NextQuestionResponse)
def next_question(request: NextQuestionRequest):
    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    role = session["role"]
    previous_questions = session.get("questions", [])
    previous_answers = session.get("answers", [])

    # Build conversational context
    context = ""
    for i, q in enumerate(previous_questions):
        context += f"Q{i+1}: {q}\n"
        if i < len(previous_answers):
            context += f"A{i+1}: {previous_answers[i]}\n"

    prompt = f"""
You are an interview coach.

Role:
{role}

Conversation so far:
{context}

Generate ONE next interview question.

Rules:
- Do NOT repeat previous questions
- Increase depth or difficulty gradually
- Be realistic and conversational
- Ask only ONE question
- Return ONLY the question text
"""

    try:
        question = local_llm.generate(prompt)
        print("✅ Ollama question generated (next)")
    except Exception as e:
        print("⚠️ Ollama failed, using fallback:", e)
        question = question_engine.get_question(role)

    # Update session
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

    session["answers"].append(request.answer)
    session["evaluations"].append(evaluation)
    followup = followup_engine.generate_followup(
        question=question,
        answer=request.answer,
        correctness_score=evaluation["correctness_score"],
        confidence_score=evaluation["confidence_score"]
    )

    return {
        "session_id": request.session_id,
        "relevance_score": evaluation["relevance_score"],
        "correctness_score": evaluation["correctness_score"],
        "star_score": evaluation["star_score"],
        "confidence_score": evaluation["confidence_score"],
        "readiness_score": evaluation["readiness_score"],
        "feedback": evaluation["feedback"],
        "follow_up_question": followup
    }
@router.get("/improvement-plan/{session_id}")
def get_improvement_plan(session_id: str):
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    evaluations = session.get("evaluations", [])

    plan = improvement_engine.generate_plan(evaluations)

    return {
        "session_id": session_id,
        "improvement_plan": plan
    }

@router.get("/analytics/{session_id}")
def get_dashboard_analytics(session_id: str):
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    evaluations = session.get("evaluations", [])

    analytics = analytics_engine.generate_metrics(evaluations)

    return {
        "session_id": session_id,
        "analytics": analytics
    }
@router.post("/voice/speak")
def speak_question(text: str):
    voice_engine.text_to_speech(text)
    return {"status": "spoken"}
