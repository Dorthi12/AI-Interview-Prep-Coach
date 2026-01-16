class AnalyticsEngine:
    def generate_metrics(self, evaluations: list[dict]) -> dict:
        if not evaluations:
            return {
                "summary": "No data available yet.",
                "trends": {},
                "averages": {},
                "total_questions": 0
            }

        # ✅ SAFE extraction (no KeyError)
        correctness = [e.get("correctness_score", 0) for e in evaluations]
        confidence = [e.get("confidence_score", 0) for e in evaluations]
        star = [e.get("star_score", 0) for e in evaluations]  # fallback = 0
        readiness = [e.get("readiness_score", 0) for e in evaluations]

        return {
            "summary": "Interview performance analytics",
            "averages": {
                "correctness": round(sum(correctness) / len(correctness), 2),
                "confidence": round(sum(confidence) / len(confidence), 2),
                "star": round(sum(star) / len(star), 2),
                "readiness": round(sum(readiness) / len(readiness), 2),
            },
            "trends": {
                "correctness": correctness,
                "confidence": confidence,
                "star": star,
                "readiness": readiness
            },
            "total_questions": len(evaluations)
        }
