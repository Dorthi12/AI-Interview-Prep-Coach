import re


class AnswerEvaluator:
    def evaluate(self, question: str, answer: str) -> dict:
        question_tokens = set(re.findall(r"\w+", question.lower()))
        answer_tokens = set(re.findall(r"\w+", answer.lower()))

        overlap = question_tokens.intersection(answer_tokens)
        relevance_score = min(len(overlap) / max(len(question_tokens), 1), 1.0)

        feedback = []
        if relevance_score < 0.2:
            feedback.append("Answer is weakly related to the question.")
        else:
            feedback.append("Answer is relevant to the question.")

        if len(answer.split()) < 20:
            feedback.append("Try to elaborate your answer with more details.")

        return {
            "relevance_score": round(relevance_score * 10, 2),
            "feedback": feedback
        }
