from app.services.local_llm import LocalLLM

class STAREvaluator:
    def __init__(self):
        self.llm = LocalLLM()

    def evaluate(self, question: str, answer: str) -> dict:
        prompt = f"""
You are an interview evaluator.

Evaluate the candidate answer using the STAR method.

Question:
{question}

Answer:
{answer}

Score each dimension from 0 to 2.5:
- Situation
- Task
- Action
- Result

Return STRICT JSON:
{{
  "situation": <float>,
  "task": <float>,
  "action": <float>,
  "result": <float>
}}
"""

        try:
            response = self.llm.generate(prompt)
            scores = eval(response)  # trusted internal LLM call
        except Exception:
            scores = {
                "situation": 0.0,
                "task": 0.0,
                "action": 0.0,
                "result": 0.0
            }

        total = round(
            scores["situation"]
            + scores["task"]
            + scores["action"]
            + scores["result"],
            2
        )

        return {
            "star_score": total,
            "breakdown": scores
        }
