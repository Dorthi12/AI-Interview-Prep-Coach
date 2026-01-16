import base64
from pathlib import Path

def set_background(image_path: str):
    img = Path(image_path).read_bytes()
    encoded = base64.b64encode(img).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


import streamlit as st
import time

from api import (
    start_interview,
    submit_answer,
    end_interview,
    get_report_url,
)

st.set_page_config(
    page_title="AI Interview Prep Coach",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
h1, h2, h3 {
    text-align: center;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background: rgba(0,0,0,0.55);
    border-radius: 18px;
    padding: 30px;
    margin: 20px auto;
    max-width: 900px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

.star {
    position: fixed;
    font-size: 22px;
    animation: floatUp 2s ease-out forwards;
}

@keyframes floatUp {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-120px); }
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Interview Prep Coach",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- GLOBAL CSS ----
st.markdown(""" 
<style>
h1, h2, h3 {
    text-align: center;
}
...
</style>
""", unsafe_allow_html=True)

# ✅ CENTERED TITLE (THIS LINE)
st.markdown("<h1>🎤 AI Interview Preparation Coach</h1>", unsafe_allow_html=True)



# ---------------- CONSTANTS ----------------
DOMAINS = {
    "Software / IT": ["DSA", "Development", "System Design"],
    "AI / ML / Data": ["ML Theory", "Coding", "Case Studies"],
    "Electronics (ECE/EEE)": ["Core Theory", "Embedded", "VLSI"],
    "Mechanical": ["Core Theory", "Design", "Manufacturing"],
    "Civil": ["Core Theory", "Structures", "Planning"],
    "Commerce / Finance": ["Accounting", "Finance", "Economics"],
    "Arts / Humanities": ["Theory", "Writing", "Analysis"],
    "Management / MBA": ["Case Study", "Strategy", "Behavioral"],
    "Core Sciences": ["Theory", "Numericals", "Research"],
    "Other / Custom": ["General"]
}

def suggest_roles(domain, company):
    domain_roles = {
        "Software / IT": ["Software Engineer", "Backend Developer", "Frontend Developer"],
        "AI / ML / Data": ["Data Scientist", "ML Engineer", "AI Researcher"],
        "Electronics (ECE/EEE)": ["Embedded Engineer", "VLSI Engineer", "Hardware Engineer"],
        "Mechanical": ["Design Engineer", "Manufacturing Engineer", "Thermal Engineer"],
        "Civil": ["Site Engineer", "Structural Engineer", "Planning Engineer"],
        "Commerce / Finance": ["Accountant", "Financial Analyst", "Auditor"],
        "Arts / Humanities": ["Content Writer", "Research Analyst", "Policy Analyst"],
        "Management / MBA": ["Business Analyst", "Product Manager", "Consultant"],
        "Core Sciences": ["Research Assistant", "Scientist", "Lab Analyst"]
    }
    roles = domain_roles.get(domain, ["General Role"])
    return [f"{r} ({company})" if company else r for r in roles]

# ---------------- SESSION STATE ----------------
DEFAULT_STATE = {
    "step": 1,
    "profile": {},
    "job": {},
    "preferences": {},
    "session_id": None,
    "question": None,
    "start_time": None,
    "summary": None,
    "last_result": None,        # stores evaluation result
    "awaiting_next": False,     # controls Next Question button
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Background control
if st.session_state.step == 6:
    set_background("assets/interviewendpage.avif")   # evaluation page
else:
    set_background("assets/interviewpagesbackground.jpg")

# ---------------- STEP 1: PERSONAL INFO ----------------

if st.session_state.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", 16, 60)
    education = st.text_input("Highest Education")
    profession = st.text_input("Current Profession")

    st.markdown("</div>", unsafe_allow_html=True)

    import random

    if st.button("Next"):
        for _ in range(15):
            st.markdown(
                f"<div class='star' style='left:{random.randint(10, 90)}%;'>⭐</div>",
                unsafe_allow_html=True
            )

        st.session_state.profile = {
            "name": name,
            "age": age,
            "education": education,
            "profession": profession,
        }
        time.sleep(0.6)
        st.session_state.step = 2
        st.rerun()


# ---------------- STEP 2: JOB DETAILS ----------------
elif st.session_state.step == 2:
    st.subheader("🎯 Job Target")

    company = st.text_input("Company Name")
    domain = st.selectbox("Select Your Domain", list(DOMAINS.keys()))
    role = st.selectbox("Target Role", suggest_roles(domain, company))

    if st.button("Next"):
        st.session_state.job = {
            "role": role,
            "company": company,
            "domain": domain,
        }
        st.session_state.step = 3
        st.rerun()

# ---------------- STEP 3: JOB OVERVIEW ----------------
elif st.session_state.step == 3:
    st.subheader("📌 Job Overview")
    job = st.session_state.job

    st.info(f"""
**Role:** {job['role']}  
**Company:** {job['company']}  
**Domain:** {job['domain']}
""")

    if st.button("Continue"):
        st.session_state.step = 4
        st.rerun()

# ---------------- STEP 4: PREFERENCES ----------------
elif st.session_state.step == 4:
    st.subheader("⚙️ Preparation Preferences")

    mode = st.radio(
        "What do you want to prepare?",
        DOMAINS[st.session_state.job["domain"]]
    )
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    if st.button("Start Interview"):
        data = start_interview(
            st.session_state.profile,
            st.session_state.job,
            {"mode": mode, "difficulty": difficulty},
        )

        st.session_state.session_id = data["session_id"]
        st.session_state.question = data["question"]
        st.session_state.start_time = time.time()
        st.session_state.step = 5
        st.rerun()

# ---------------- STEP 5: INTERVIEW LOOP ----------------
elif st.session_state.step == 5:
    st.subheader("🧠 Interview Session")

    elapsed = int(time.time() - st.session_state.start_time)
    st.info(f"⏱ Time elapsed: {elapsed} seconds")

    st.markdown(f"### ❓ Question\n{st.session_state.question}")

    # Disable answer box if waiting for next question
    answer = st.text_area(
        "Your Answer",
        height=180,
        disabled=st.session_state.awaiting_next
    )

    col1, col2 = st.columns(2)

    # ---------- SUBMIT ANSWER ----------
    with col1:
        if st.button("Submit Answer", disabled=st.session_state.awaiting_next):
            result = submit_answer(
                st.session_state.session_id,
                answer
            )

            # store evaluation
            st.session_state.last_result = result
            st.session_state.pending_question = result["follow_up_question"]
            st.session_state.awaiting_next = True

            st.rerun()

    # ---------- END INTERVIEW ----------
    with col2:
        if st.button("End Interview"):
            summary = end_interview(st.session_state.session_id)
            st.session_state.summary = summary
            st.session_state.step = 6
            st.rerun()

    # ---------- SHOW EVALUATION ----------
    if st.session_state.last_result:
        result = st.session_state.last_result

        st.success("Answer evaluated")

        cols = st.columns(3)

        with cols[0]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Correctness", result["correctness_score"])
            st.markdown("</div>", unsafe_allow_html=True)

        with cols[1]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Confidence", result["confidence_score"])
            st.markdown("</div>", unsafe_allow_html=True)

        with cols[2]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Readiness", result["readiness_score"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("**Feedback:**")
        for f in result["feedback"]:
            st.write("-", f)

        st.divider()

        # ---------- NEXT QUESTION BUTTON ----------
        if st.session_state.awaiting_next:
            if st.button("➡️ Next Question"):
                st.session_state.question = st.session_state.pending_question
                st.session_state.pending_question = None
                st.session_state.awaiting_next = False
                st.session_state.last_result = None
                st.session_state.start_time = time.time()
                st.rerun()

# ---------------- STEP 6: FINAL SUMMARY ----------------
elif st.session_state.step == 6:
    st.subheader("📊 Interview Summary")

    summary = st.session_state.summary
    analytics = summary["analytics"]
    improvement = summary["improvement"]

    st.success("Interview completed successfully")

    # ---------- OVERALL PERFORMANCE ----------
    st.markdown("## ⭐ Overall Performance")

    cols = st.columns(3)
    cols[0].metric("Correctness", analytics["averages"]["correctness"])
    cols[1].metric("Confidence", analytics["averages"]["confidence"])
    cols[2].metric("Readiness", analytics["averages"]["readiness"])

    st.divider()

    # ---------- PERSONALIZED FEEDBACK ----------
    st.markdown("## 🎯 Personalized Feedback")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚠️ Focus Areas")
        if improvement.get("focus_areas"):
            for area in improvement["focus_areas"]:
                st.markdown(f"- {area}")
        else:
            st.write("No focus areas identified.")

    with col2:
        st.markdown("### 🛠 Action Items")
        if improvement.get("action_items"):
            for action in improvement["action_items"]:
                st.markdown(f"- {action}")
        else:
            st.write("No action items available.")

    # ---------- FINAL RECOMMENDATION ----------
    st.markdown("## 🧠 Final Recommendation")
    st.info(improvement.get("summary", "Keep practicing consistently."))

    st.divider()

    # ---------- REPORT DOWNLOAD ----------
    st.markdown("## 📄 Interview Report")
    st.markdown(
        f"[⬇️ Download Interview Report]({get_report_url(st.session_state.session_id)})"
    )

    if st.button("🔁 Restart Interview"):
        st.session_state.clear()
        st.rerun()

    # ---------- RESTART ----------
    if st.button("🔁 Start New Interview"):
        st.session_state.clear()
        st.rerun()
