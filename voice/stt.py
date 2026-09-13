import speech_recognition as sr
from config import LANGUAGES, DEFAULT_LANGUAGE

def listen(lang_key: str = DEFAULT_LANGUAGE) -> str:
    """Captures microphone input and transcribes audio in the selected language."""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0
    stt_code = LANGUAGES.get(lang_key, LANGUAGES[DEFAULT_LANGUAGE])["stt_code"]

    with sr.Microphone() as source:
        print(f"\n[Listening in {LANGUAGES[lang_key]['name']}...] Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            print("[Processing speech...]")
            google_recognizer = getattr(recognizer, "recognize_google")
            query = google_recognizer(audio, language=stt_code)
            print(f"User Said: '{query}'")
            return query.lower()
        except sr.WaitTimeoutError:
            print("[!] Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("[!] Speech could not be understood.")
            return ""
        except sr.RequestError as e:
            print(f"[!] Speech recognition service error: {e}")
            return ""