import json
import random
from pathlib import Path


class QuestionEngine:
    def __init__(self):
        data_path = Path(__file__).resolve().parents[2] / "data" / "questions.json"
        with open(data_path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def get_question(self, role: str) -> str:
        role = role.lower()
        if role not in self.questions:
            raise ValueError("Invalid interview role")

        return random.choice(self.questions[role])
