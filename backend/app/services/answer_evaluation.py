import re
from app.services.semantic_evaluator import SemanticEvaluator
from app.services.star_evaluation import STAREvaluator

class AnswerEvaluator:
    def __init__(self):
        self.semantic = SemanticEvaluator()
        self.star = STAREvaluator()

    def evaluate(self, question: str, answer: str) -> dict:
        # ---- Semantic relevance (0–10) ----
        relevance = self.semantic.similarity(question, answer)

        # ---- Length heuristic ----
        length_score = min(len(answer.split()) / 25, 1.0) * 10

        # ---- Confidence heuristic ----
        confidence_keywords = [
            "I implemented", "I optimized", "I designed",
            "I used", "I analyzed", "I led", "I built"
        ]
        confidence_score = sum(
            1 for k in confidence_keywords if k.lower() in answer.lower()
        )
        confidence_score = min(confidence_score * 2, 10)

        # ---- Correctness proxy ----
        correctness_score = round(
            (relevance * 0.6 + length_score * 0.4), 2
        )

        # ---- STAR evaluation (LLM) ----
        star_eval = self.star.evaluate(question, answer)
        star_score = star_eval["star_score"]

        # ---- Readiness score ----
        readiness_score = round(
            (correctness_score * 0.5 + confidence_score * 0.2 + star_score * 0.3),
            2
        )

        # ---- Feedback ----
        feedback = []
        if relevance < 5:
            feedback.append("Answer lacks alignment with the question.")
        if length_score < 5:
            feedback.append("Answer is too brief. Add more explanation.")
        if confidence_score < 4:
            feedback.append("Use more assertive, experience-based statements.")
        if star_score < 5:
            feedback.append("Structure your answer better using the STAR method.")
        if not feedback:
            feedback.append("Strong answer with good structure and clarity.")

        return {
            "relevance_score": round(relevance, 2),
            "correctness_score": correctness_score,
            "confidence_score": confidence_score,
            "star_score": star_score,
            "star_breakdown": star_eval["breakdown"],
            "readiness_score": readiness_score,
            "feedback": feedback
        }
