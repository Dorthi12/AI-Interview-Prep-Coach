import re


class AnswerEvaluator:
    def evaluate(self, question: str, answer: str) -> dict:
        question_tokens = set(re.findall(r"\w+", question.lower()))
        answer_tokens = set(re.findall(r"\w+", answer.lower()))

        overlap = question_tokens.intersection(answer_tokens)
        relevance_score = min(len(overlap) / max(len(question_tokens), 1), 1.0)

        feedback = []

        # relevance feedback
        if relevance_score < 0.2:
            feedback.append("Answer is weakly related to the question.")
        else:
            feedback.append("Answer is relevant to the question.")

        # length check
        if len(answer.split()) < 20:
            feedback.append("Try to elaborate your answer with more details.")

        # STAR structure detection
        star_score = 0
        star_keywords = {
            "situation": ["situation", "context", "background"],
            "task": ["task", "responsibility", "goal"],
            "action": ["action", "implemented", "worked", "developed"],
            "result": ["result", "outcome", "impact", "improved"]
        }

        for _, keywords in star_keywords.items():
            if any(word in answer.lower() for word in keywords):
                star_score += 1

        if star_score >= 3:
            feedback.append("Answer follows a good STAR structure.")
        elif star_score >= 1:
            feedback.append("Answer has partial structure; try using the STAR method.")
        else:
            feedback.append("Consider structuring your answer using the STAR method.")

        # Confidence analysis
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


        return {
            "relevance_score": round(relevance_score * 10, 2),
            "star_score": star_score,
            "confidence_score": confidence_score,
            "feedback": feedback
        }

# STAR method =
#
# * Situation
#
# * Task
#
# * Action
#
# * Result

