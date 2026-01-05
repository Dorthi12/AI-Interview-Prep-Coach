import re
from app.services.local_llm import LocalLLM


class AnswerEvaluator:
    def __init__(self):
        # Local LLM (Ollama)
        self.llm = LocalLLM()

    # ---------------- OPTIONAL RULE-BASED BOOST ---------------- #
    def check_correctness(self, question: str, answer: str) -> int:
        q = question.lower()
        a = answer.lower()

        score = 0

        # Example rule: REST vs SOAP (OPTIONAL ONLY)
        if "rest" in q and "soap" in q:
            required = ["http", "stateless"]
            optional = ["json", "xml", "wsdl"]
            red_flags = ["rest uses xml only", "soap is stateless"]

            for r in required:
                if r in a:
                    score += 1

            for o in optional:
                if o in a:
                    score += 1

            for rf in red_flags:
                if rf in a:
                    score -= 2

        return max(0, min(score, 3))  # small boost only

    # ---------------- MAIN EVALUATION ---------------- #
    def evaluate(self, question: str, answer: str) -> dict:
        feedback = []

        # ---------- Semantic relevance ----------
        question_tokens = set(re.findall(r"\w+", question.lower()))
        answer_tokens = set(re.findall(r"\w+", answer.lower()))

        overlap = question_tokens.intersection(answer_tokens)
        relevance_score = min(len(overlap) / max(len(question_tokens), 1), 1.0)

        if relevance_score < 0.2:
            feedback.append("Answer is weakly related to the question.")
        else:
            feedback.append("Answer is relevant to the question.")

        if len(answer.split()) < 20:
            feedback.append("Try to elaborate your answer with more details.")

        # ---------- STAR structure ----------
        star_keywords = {
            "situation": ["situation", "context", "background"],
            "task": ["task", "responsibility", "goal"],
            "action": ["action", "implemented", "worked", "developed", "designed"],
            "result": ["result", "outcome", "impact", "improved"]
        }

        star_score = sum(
            1 for keywords in star_keywords.values()
            if any(word in answer.lower() for word in keywords)
        )

        if star_score >= 3:
            feedback.append("Answer follows a good STAR structure.")
        elif star_score >= 1:
            feedback.append("Answer has partial structure; try using the STAR method.")
        else:
            feedback.append("Consider structuring your answer using the STAR method.")

        # ---------- Confidence ----------
        filler_words = ["um", "uh", "basically", "like", "you know"]
        weak_phrases = ["i think", "maybe", "probably", "not sure"]
        strong_verbs = ["led", "implemented", "designed", "optimized", "built"]

        answer_lower = answer.lower()

        filler_count = sum(answer_lower.count(w) for w in filler_words)
        weak_count = sum(answer_lower.count(w) for w in weak_phrases)
        strong_count = sum(1 for v in strong_verbs if v in answer_lower)

        confidence_score = max(0, min(10, 5 + strong_count - filler_count - weak_count))

        if filler_count > 0 or weak_count > 0:
            feedback.append("Reduce filler words and weak phrases to sound more confident.")

        if strong_count > 0:
            feedback.append("Good use of action-oriented language.")

        # ---------- LLM-BASED GENERALIZED CORRECTNESS ----------
        try:
            llm_result = self.llm.evaluate_correctness(question, answer)
            correctness_score = llm_result.get("score", 5)

            feedback.append(f"Correctness verdict: {llm_result.get('verdict', 'Partially')}")

            for p in llm_result.get("missing_points", []):
                feedback.append(f"Missing point: {p}")

            for p in llm_result.get("incorrect_points", []):
                feedback.append(f"Incorrect point: {p}")

        except Exception:
            correctness_score = 5
            feedback.append("Correctness evaluation unavailable (LLM not running).")

        # ---------- OPTIONAL RULE-BASED BOOST ----------
        correctness_score += self.check_correctness(question, answer)
        correctness_score = max(0, min(correctness_score, 10))

        # ---------- Readiness ----------
        readiness_score = (
            (relevance_score * 10) * 0.4 +
            (star_score / 4 * 100) * 0.3 +
            (confidence_score * 10) * 0.3
        )

        readiness_score = round(readiness_score, 2)

        return {
            "relevance_score": round(relevance_score * 10, 2),
            "star_score": star_score,
            "confidence_score": confidence_score,
            "correctness_score": correctness_score,
            "readiness_score": readiness_score,
            "feedback": feedback
        }
