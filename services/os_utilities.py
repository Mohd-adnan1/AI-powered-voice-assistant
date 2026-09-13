import os
import time
import datetime
import psutil
import pyautogui
import cv2
import screen_brightness_control as sbc
from voice.tts import speak

def handle_system_command(query: str, log_fn, lang: str) -> bool:
    # Time and Date
    if "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        msg = f"The current time is {now}."
        log_fn(f"[System]: {msg}")
        speak(msg, lang)
        return True

    elif "date" in query or "day" in query:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        msg = f"Today is {today}."
        log_fn(f"[System]: {msg}")
        speak(msg, lang)
        return True

    # Launch System Applications
    elif "calculator" in query or "calc" in query:
        log_fn("[System]: Opening Calculator...")
        speak("Opening Calculator.", lang)
        os.system("calc")
        return True

    elif "open notepad" in query:
        log_fn("[System]: Opening Notepad...")
        speak("Opening Notepad.", lang)
        os.system("notepad")
        return True

    elif "task manager" in query:
        log_fn("[System]: Opening Task Manager...")
        speak("Opening Task Manager.", lang)
        os.system("taskmgr")
        return True

    # Basic Voice Math Calculations
    elif "calculate" in query:
        expr = query.replace("calculate", "").strip()
        try:
            cleaned = expr.replace("x", "*").replace("times", "*").replace("plus", "+").replace("minus", "-").replace("divided by", "/")
            res = eval(cleaned, {"__builtins__": None}, {})
            msg = f"The answer is {res}"
            log_fn(f"[Math]: {msg}")
            speak(msg, lang)
            return True
        except Exception:
            pass

    # System Telemetry (CPU & Battery)
    elif any(k in query for k in ["battery", "cpu", "system status", "ram", "memory"]):
        battery = psutil.sensors_battery()
        cpu = psutil.cpu_percent(interval=1)
        battery_pct = f"{battery.percent}%" if battery else "N/A"
        msg = f"CPU usage is at {cpu} percent. Battery is at {battery_pct}."
        log_fn(f"[System]: {msg}")
        speak(msg, lang)
        return True

    # Volume Controls
    elif "volume up" in query or "increase volume" in query:
        pyautogui.press("volumeup", presses=5)
        log_fn("[System]: Increased volume")
        speak("Increased volume.", lang)
        return True
    elif "volume down" in query or "decrease volume" in query:
        pyautogui.press("volumedown", presses=5)
        log_fn("[System]: Decreased volume")
        speak("Decreased volume.", lang)
        return True
    elif "mute" in query:
        pyautogui.press("volumemute")
        log_fn("[System]: Toggled mute")
        speak("Muted or unmuted audio.", lang)
        return True

    # Brightness Control
    elif "brightness" in query:
        try:
            sbc.set_brightness(75)
            log_fn("[System]: Adjusted brightness to 75%")
            speak("Brightness adjusted to 75 percent.", lang)
        except Exception:
            log_fn("[System Error]: Could not adjust brightness")
            speak("Could not adjust screen brightness.", lang)
        return True

    # Screenshot Capture
    elif "screenshot" in query or "capture screen" in query:
        filename = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(filename)
        log_fn(f"[System]: Saved screenshot as {filename}")
        speak("Screenshot captured and saved.", lang)
        return True

    # Camera Photo Snapshot
    elif "photo" in query or "camera" in query or "picture" in query:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            img_name = f"photo_{int(time.time())}.jpg"
            cv2.imwrite(img_name, frame)
            log_fn(f"[System]: Photo saved as {img_name}")
            speak("Photo captured successfully.", lang)
        else:
            log_fn("[System Error]: Could not access camera")
            speak("Failed to access camera.", lang)
        cap.release()
        return True

    # Quick Note Creation
    elif "write note" in query or "take a note" in query or "save note" in query:
        note_content = query.replace("write note", "").replace("take a note", "").replace("save note", "").strip()
        if note_content:
            with open("quick_notes.txt", "a") as f:
                f.write(f"[{time.ctime()}] {note_content}\n")
            log_fn(f"[System Note]: {note_content}")
            speak("Note saved to your notepad file.", lang)
            return True

    return False