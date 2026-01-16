import os
from fpdf import FPDF
from datetime import datetime

REPORT_DIR = "reports"


class PDFReportGenerator:
    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)

    def generate(self, session: dict, analytics: dict, improvement: dict) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # ---------- TITLE ----------
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "AI Interview Evaluation Report", ln=True, align="C")
        pdf.ln(5)

        # ---------- META ----------
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Role: {session['role']}", ln=True)
        pdf.cell(0, 8, f"Domain: {session['domain']}", ln=True)
        pdf.cell(0, 8, f"Difficulty: {session['difficulty']}", ln=True)
        pdf.cell(0, 8, f"Mode: {session['mode']}", ln=True)

        start = session.get("start_time")
        end = session.get("end_time")
        if start and end:
            duration = int(end - start)
            pdf.cell(0, 8, f"Interview Duration: {duration} seconds", ln=True)

        pdf.ln(6)

        # ---------- QUESTION-WISE EVALUATION ----------
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Question-wise Evaluation", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", size=11)

        for idx, evaluation in enumerate(session["evaluations"]):
            question = session["questions"][idx]
            answer = session["answers"][idx]

            pdf.multi_cell(0, 8, f"Q{idx+1}: {question}")
            pdf.multi_cell(0, 8, f"Answer: {answer}")

            pdf.cell(
                0, 8,
                f"Correctness: {evaluation['correctness_score']} | "
                f"Confidence: {evaluation['confidence_score']} | "
                f"Readiness: {evaluation['readiness_score']}",
                ln=True
            )

            pdf.multi_cell(
                0, 8,
                "Feedback:\n- " + "\n- ".join(evaluation["feedback"])
            )

            pdf.ln(4)

        # ---------- ANALYTICS ----------
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Overall Performance Analytics", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", size=11)
        averages = analytics.get("averages", {})

        for metric, value in averages.items():
            pdf.cell(0, 8, f"{metric.capitalize()}: {value}", ln=True)

        pdf.ln(5)

        # ---------- IMPROVEMENT PLAN ----------
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Strengths & Improvement Areas", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", size=11)

        pdf.cell(0, 8, "Strengths:", ln=True)
        for s in improvement.get("strengths", []):
            pdf.cell(0, 8, f"- {s}", ln=True)

        pdf.ln(3)

        pdf.cell(0, 8, "Areas to Improve:", ln=True)
        for w in improvement.get("weaknesses", []):
            pdf.cell(0, 8, f"- {w}", ln=True)

        pdf.ln(4)

        pdf.multi_cell(
            0, 8,
            f"Final Recommendation:\n{improvement.get('recommendation', '')}"
        )

        # ---------- SAVE ----------
        filename = f"{session['session_id']}.pdf"
        path = os.path.join(REPORT_DIR, filename)
        pdf.output(path)

        return path

    def get_path(self, session_id: str) -> str:
        return os.path.join(REPORT_DIR, f"{session_id}.pdf")
