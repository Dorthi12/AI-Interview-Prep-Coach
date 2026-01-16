from app.services.local_llm import LocalLLM


class ImprovementPlanEngine:
    def __init__(self):
        self.llm = LocalLLM()

    def generate_plan(self, evaluations: list[dict]) -> dict:
        """
        Generates a personalized improvement plan
        based on past evaluations.
        """

        if not evaluations:
            return {
                "summary": "No evaluations available yet.",
                "focus_areas": [],
                "action_items": []
            }

        # Aggregate signals
        avg_correctness = sum(e["correctness_score"] for e in evaluations) / len(evaluations)
        avg_confidence = sum(e["confidence_score"] for e in evaluations) / len(evaluations)
        avg_star = sum(e["star_score"] for e in evaluations) / len(evaluations)

        focus_areas = []
        action_items = []

        # Rule-based diagnosis
        if avg_correctness < 6:
            focus_areas.append("Technical understanding")
            action_items.append("Review core concepts related to recent questions.")
            action_items.append("Practice explaining concepts in simple terms.")

        if avg_confidence < 6:
            focus_areas.append("Confidence and clarity")
            action_items.append("Reduce filler words and hesitant phrases.")
            action_items.append("Practice answering aloud with structured responses.")

        if avg_star < 2:
            focus_areas.append("Answer structure (STAR method)")
            action_items.append("Practice framing answers using Situation, Task, Action, Result.")

        # LLM-enhanced coaching (optional but powerful)
        try:
            prompt = f"""
You are an interview coach.

Candidate performance summary:
- Average correctness score: {avg_correctness}/10
- Average confidence score: {avg_confidence}/10
- Average STAR score: {avg_star}/4

Generate:
1. A short improvement summary
2. 3 specific practice recommendations
3. 2 mock interview exercises

Respond concisely.
"""

            llm_response = self.llm.generate(prompt)

        except Exception:
            llm_response = "Focus on improving clarity, structure, and conceptual understanding."

        return {
            "summary": llm_response,
            "focus_areas": focus_areas,
            "action_items": action_items
        }
