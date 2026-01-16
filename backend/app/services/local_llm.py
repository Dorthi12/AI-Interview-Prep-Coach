import requests
import json


class LocalLLM:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    # ---------- Generic text generation ----------
    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    # ---------- GENERALIZED CORRECTNESS EVALUATION ----------
    def evaluate_correctness(self, question: str, answer: str) -> dict:
        """
        Domain-agnostic correctness evaluation.
        Works for technical, behavioral, HR, management, ANY domain.
        """

        prompt = f"""
You are an expert interviewer.

Question:
{question}

Candidate answer:
{answer}

Evaluate the answer ONLY with respect to the question.

Respond STRICTLY in JSON format:
{{
  "verdict": "Yes | Partially | No",
  "missing_points": [],
  "incorrect_points": [],
  "score": 0-10
}}

Rules:
- Do NOT rewrite the answer
- Do NOT assume the domain
- Be concise
"""

        raw_response = self.generate(prompt)

        # Try to parse JSON safely
        try:
            start = raw_response.find("{")
            end = raw_response.rfind("}") + 1
            json_text = raw_response[start:end]

            return json.loads(json_text)

        except Exception:
            # Safe fallback (never crash the system)
            return {
                "verdict": "Partially",
                "missing_points": [],
                "incorrect_points": [],
                "score": 5
            }
