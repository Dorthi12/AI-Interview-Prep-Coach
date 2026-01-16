import uuid

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, role, domain, difficulty, mode):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "role": role,
            "domain": domain,
            "difficulty": difficulty,
            "mode": mode,
            "questions": [],
            "answers": [],
            "evaluations": [],   # ✅ ALWAYS INITIALIZED
            "start_time": None,
            "end_time": None
        }
        return self.sessions[session_id]

    def get_session(self, session_id):
        return self.sessions.get(session_id)
