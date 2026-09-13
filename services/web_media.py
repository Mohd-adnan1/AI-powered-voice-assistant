import webbrowser
import pywhatkit
from pywhatkit.whats import sendwhatmsg_instantly
from voice.tts import speak

def handle_web_command(query: str, log_fn, lang: str) -> bool:
    # Play YouTube Videos
    if "play" in query and "youtube" in query:
        topic = query.replace("play", "").replace("on youtube", "").strip()
        log_fn(f"[Web]: Playing '{topic}' on YouTube...")
        speak(f"Playing {topic} on YouTube.", lang)

        player = getattr(pywhatkit, "playonyt", None)
        if callable(player):
            player(topic)
        else:
            search_term = topic.replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
            speak(f"Opening YouTube search for {topic}.", lang)

        return True

    # Send WhatsApp Message via Voice
    elif "whatsapp" in query or "send message" in query:
        speak("Please enter or say the phone number with country code.", lang)
        # Supports web-driven WhatsApp messaging
        sendwhatmsg_instantly("+910000000000", "Hello from AI Assistant!", tab_close=True)
        speak("WhatsApp message process initiated.", lang)
        return True

    # Open Custom Websites / URLs
    elif "open" in query:
        for site in ["youtube", "google", "github", "stackoverflow", "reddit"]:
            if site in query:
                webbrowser.open(f"https://www.{site}.com")
                speak(f"Opening {site}.", lang)
                return True

    # Google Search
    elif "search" in query:
        search_query = query.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching Google for {search_query}.", lang)
        return True

    return False