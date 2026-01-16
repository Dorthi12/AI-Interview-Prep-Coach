🧠 AI Interview Prep Coach – Backend

A local LLM-powered interview coaching backend that simulates real interview behavior by dynamically generating questions, evaluating answers, asking intelligent follow-ups, tracking performance analytics, and generating personalized improvement plans — without relying on paid APIs.

🚀 Features

🎯 Interview Simulation

Dynamic interview question generation using Ollama (Mistral)
Context-aware next questions (no repetition)
Adaptive difficulty progression

🧪 Answer Evaluation

Semantic relevance scoring
STAR method structure detection
Confidence analysis (language strength & fillers)
LLM-based generalized correctness evaluation (domain-agnostic)
Readiness score calculation

🔁 Conversational Follow-Ups

Follow-up questions generated based on:
Answer quality
Correctness
Confidence level
Mimics real interviewer behavior (“Why?”, “Explain more”, “Trade-offs?”)

📊 Analytics Dashboard (Backend)

Performance trends over time
Average correctness, confidence, STAR, readiness
Session-level analytics for visualization

🧭 Personalized Improvement Plan

Identifies weak areas across the session
Generates actionable improvement steps
Combines rule-based diagnostics + LLM coaching

🎤 Voice Support

Text-to-Speech (TTS) for interview questions
Audio-file-based Speech-to-Text (STT)
Live microphone input gated (optional, OS-dependent)

Tech Stack

FastAPI – Backend framework
Ollama (Mistral) – Local LLM inference
Python 3.11+
SpeechRecognition – STT (file-based)
pyttsx3 – Text-to-Speech
Uvicorn – ASGI server