from app.services.local_llm import LocalLLM


class FollowUpEngine:
    def __init__(self):
        self.llm = LocalLLM()

    def generate_followup(
        self,
        question: str,
        answer: str,
        correctness_score: int,
        confidence_score: int
    ) -> str:
        """
        Generate ONE realistic follow-up question like a human interviewer.
        Domain-agnostic.
        """

        prompt = f"""
You are an interviewer.

Original question:
{question}

Candidate answer:
{answer}

Evaluation summary:
- Correctness score: {correctness_score}/10
- Confidence score: {confidence_score}/10

Based on this, generate ONE follow-up question.

Rules:
- If answer is weak → ask for clarification or example
- If answer is strong → ask for deeper reasoning or trade-offs
- Be natural and conversational
- Do NOT repeat the original question
- Output ONLY the follow-up question
"""

        try:
            followup = self.llm.generate(prompt)
            return followup.strip()
        except Exception:
            return "Can you explain that in a bit more detail?"
