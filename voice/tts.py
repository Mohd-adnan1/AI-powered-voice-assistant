import asyncio
import os
import pygame
import pyttsx3
import edge_tts
from config import LANGUAGES, DEFAULT_LANGUAGE

pygame.mixer.init()

async def _edge_speak_async(text: str, voice: str):
    """Generates speech audio using Edge TTS and plays it."""
    file_path = "temp_speech.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)
    
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()
    if os.path.exists(file_path):
        os.remove(file_path)

def _pyttsx3_fallback(text: str):
    """Offline speech engine fallback."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text: str, lang_key: str = DEFAULT_LANGUAGE):
    """Main speak function routing speech synthesis based on language selection."""
    voice_info = LANGUAGES.get(lang_key, LANGUAGES[DEFAULT_LANGUAGE])
    tts_voice = voice_info["tts_voice"]
    
    try:
        asyncio.run(_edge_speak_async(text, tts_voice))
    except Exception as e:
        print(f"[Warning] Edge TTS error ({e}). Falling back to pyttsx3.")
        _pyttsx3_fallback(text)