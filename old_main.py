import sys
from auth.security import authenticate_user
from voice.tts import speak
from voice.stt import listen
from config import LANGUAGES, DEFAULT_LANGUAGE

def main():
    # 1. Password Security Lock
    if not authenticate_user():
        sys.exit()

    current_lang = DEFAULT_LANGUAGE
    speak("Authentication successful. Hello, how can I assist you today?", current_lang)

    while True:
        print("\n------------------------------------------")
        print("Available languages: [en] English | [hi] Hindi | [es] Spanish | [ur] Urdu")
        print(f"Active Language: {LANGUAGES[current_lang]['name']}")
        
        command = listen(current_lang)

        if not command:
            continue

        # Language Switch Triggers
        if "switch to hindi" in command or "हिंदी" in command:
            current_lang = "hi"
            speak("अब मैं हिंदी में बात करूंगा।", current_lang)
            continue
        elif "switch to spanish" in command or "español" in command:
            current_lang = "es"
            speak("Ahora hablaré en español.", current_lang)
            continue
        elif "switch to urdu" in command or "اردو" in command:
            current_lang = "ur"
            speak("اب میں اردو میں بات کروں گا۔", current_lang)
            continue
        elif "switch to english" in command:
            current_lang = "en"
            speak("Switched back to English.", current_lang)
            continue

        # Exit Triggers
        if any(word in command for word in ["exit", "stop", "quit", "bye", "बंद करो"]):
            speak("Goodbye! Have a great day.", current_lang)
            break

if __name__ == "__main__":
    main()