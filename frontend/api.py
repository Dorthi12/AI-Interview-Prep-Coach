import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------------- START INTERVIEW ----------------
def start_interview(profile, job, preferences):
    payload = {
        "role": job["role"],
        "domain": job["domain"],
        "difficulty": preferences["difficulty"],
        "mode": preferences["mode"]
    }
    res = requests.post(f"{BASE_URL}/interview/start", json=payload)
    res.raise_for_status()
    return res.json()


# ---------------- SUBMIT ANSWER ----------------
def submit_answer(session_id, answer):
    payload = {
        "session_id": session_id,
        "answer": answer
    }
    res = requests.post(f"{BASE_URL}/interview/answer", json=payload)
    res.raise_for_status()
    return res.json()


# ---------------- END INTERVIEW (RETURNS ANALYTICS + REPORT URL) ----------------
def end_interview(session_id):
    payload = {
        "session_id": session_id
    }
    res = requests.post(f"{BASE_URL}/interview/end", json=payload)
    res.raise_for_status()
    return res.json()


# ---------------- REPORT DOWNLOAD URL ----------------
def get_report_url(session_id):
    return f"{BASE_URL}/interview/report/{session_id}"
