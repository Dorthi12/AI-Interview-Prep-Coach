import uuid


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, role: str) -> dict:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "role": role,
            "questions": [],
            "answers": [],
            "evaluations": [],
            "current_index": 0
        }
        return {
            "session_id": session_id,
            "role": role
        }

    def get_session(self, session_id: str) -> dict:
        return self.sessions.get(session_id)
