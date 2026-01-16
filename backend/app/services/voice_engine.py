import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def speech_to_text(self, audio_file_path: str) -> str:
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio)
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
        except Exception:
            self.engine = None

    def text_to_speech(self, text: str):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()