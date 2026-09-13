import os

# Password Configuration
APP_PASSWORD = "Karl-El"
MAX_ATTEMPTS = 3

# Load API Key directly from API.txt or environment variables
def get_api_key():
    if os.path.exists("API.txt"):
        with open("API.txt", "r") as f:
            key = f.read().strip()
            if key and not key.startswith("YOUR_"):
                return key
    return os.getenv("GEMINI_API_KEY", "")

GEMINI_API_KEY = get_api_key()

# Multilingual Settings
DEFAULT_LANGUAGE = "en"

LANGUAGES = {
    "en": {
        "name": "English",
        "stt_code": "en-IN",
        "tts_voice": "en-IN-NeerjaNeural"
    },
    "hi": {
        "name": "Hindi",
        "stt_code": "hi-IN",
        "tts_voice": "hi-IN-SwaraNeural"
    },
    "es": {
        "name": "Spanish",
        "stt_code": "es-ES",
        "tts_voice": "es-ES-ElviraNeural"
    },
    "ur": {
        "name": "Urdu",
        "stt_code": "ur-PK",
        "tts_voice": "ur-PK-UzmaNeural"
    }
}