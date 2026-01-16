from fastapi import APIRouter, HTTPException
from app.services.answer_evaluation import AnswerEvaluator
from app.services.followup_engine import FollowUpEngine
from app.services.session_manager import SessionManager

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

answer_evaluator = AnswerEvaluator()
followup_engine = FollowUpEngine()
session_manager = SessionManager()

@router.post("/answer")
def evaluate_answer(payload: dict):
    session_id = payload.get("session_id")
    answer = payload.get("answer")

    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = session["questions"][-1]

    evaluation = answer_evaluator.evaluate(question, answer)
    followup = followup_engine.generate_followup(
        question,
        answer,
        evaluation["correctness_score"],
        evaluation["confidence_score"]
    )

    session["answers"].append(answer)
    session["evaluations"].append(evaluation)

    return {
        "score": evaluation["correctness_score"],
        "feedback": evaluation["feedback"],
        "followup_question": followup
    }
