class AnalyticsEngine:
    def generate_metrics(self, evaluations: list[dict]) -> dict:
        if not evaluations:
            return {
                "summary": "No data available yet.",
                "trends": {},
                "averages": {}
            }

        correctness = [e["correctness_score"] for e in evaluations]
        confidence = [e["confidence_score"] for e in evaluations]
        star = [e["star_score"] for e in evaluations]
        readiness = [e["readiness_score"] for e in evaluations]

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
