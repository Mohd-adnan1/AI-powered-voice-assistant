import customtkinter as ctk
import threading
import keyboard
from voice.tts import speak
from voice.stt import listen
from brain.llm_chat import ask_gemini
from services.os_utilities import handle_system_command
from services.web_media import handle_web_command
from services.office_tools import handle_office_command
import psutil
from config import LANGUAGES, DEFAULT_LANGUAGE

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Desktop Assistant HUD")
        self.geometry("850x650")
        self.resizable(False, False)

        self.current_lang = DEFAULT_LANGUAGE
        self.is_listening = False

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(pady=15, padx=20, fill="x")

        self.title_label = ctk.CTkLabel(
            self.header_frame, text="⚡ AI VOICE ASSISTANT HUB", font=("Consolas", 20, "bold")
        )
        self.title_label.pack(side="left", padx=15, pady=10)

        self.lang_option = ctk.CTkOptionMenu(
            self.header_frame, 
            values=["en (English)", "hi (Hindi)", "es (Spanish)", "ur (Urdu)"],
            command=self.change_language
        )
        self.lang_option.pack(side="right", padx=15, pady=10)

        # Chat & Log Terminal
        self.log_terminal = ctk.CTkTextbox(self, font=("Consolas", 13), wrap="word")
        self.log_terminal.pack(pady=10, padx=20, fill="both", expand=True)
        self.log("System initialized. Welcome!")

        # Control Panel
        self.control_frame = ctk.CTkFrame(self, corner_radius=10)
        self.control_frame.pack(pady=15, padx=20, fill="x")

        self.mic_button = ctk.CTkButton(
            self.control_frame, 
            text="🎙️ START LISTENING", 
            fg_color="#1f6aa5", 
            hover_color="#144870",
            font=("Consolas", 14, "bold"),
            command=self.toggle_listening_thread
        )
        self.mic_button.pack(side="left", padx=15, pady=12, expand=True)

        self.text_input = ctk.CTkEntry(self.control_frame, placeholder_text="Type command or question here...", width=400)
        self.text_input.pack(side="left", padx=10, pady=12)
        self.text_input.bind("<Return>", lambda event: self.send_text_command())

        self.send_button = ctk.CTkButton(self.control_frame, text="Send", width=80, command=self.send_text_command)
        self.send_button.pack(side="left", padx=10, pady=12)

        #
        # Add to __init__ of AssistantGUI
        self.stats_label = ctk.CTkLabel(self.header_frame, text="CPU: --% | RAM: --%", font=("Consolas", 11))
        self.stats_label.pack(side="right", padx=10)
        self.update_telemetry()


        # hotkey keyboard 

        # Global Hotkey Trigger (Ctrl + Alt + Space to start listening anywhere)
        try:
            keyboard.add_hotkey("ctrl+alt+space", self.toggle_listening_thread)
            self.log("[+] Global Hotkey Active: Press 'Ctrl + Alt + Space' anywhere to speak.")
        except Exception:
            pass

    def log(self, text: str):
        """Prints formatted logs to the GUI terminal."""
        self.log_terminal.insert("end", f"{text}\n")
        self.log_terminal.see("end")

    def change_language(self, choice: str):
        lang_code = choice.split()[0]
        self.current_lang = lang_code
        self.log(f"[+] Active language set to: {LANGUAGES[lang_code]['name']}")

    def toggle_listening_thread(self):
        threading.Thread(target=self.process_voice_command, daemon=True).start()

    def send_text_command(self):
        query = self.text_input.get().strip()
        if query:
            self.text_input.delete(0, "end")
            threading.Thread(target=self.execute_pipeline, args=(query,), daemon=True).start()

    def process_voice_command(self):
        self.mic_button.configure(text="🔴 LISTENING...", fg_color="#a51f1f")
        query = listen(self.current_lang)
        self.mic_button.configure(text="🎙️ START LISTENING", fg_color="#1f6aa5")

        if query:
            self.log(f"\n🗣️ User ({LANGUAGES[self.current_lang]['name']}): {query}")
            self.execute_pipeline(query)

    def execute_pipeline(self, query: str):
        query_lower = query.lower()

        # Command Routing Priority: System -> Web -> Office -> LLM Brain
        if handle_system_command(query_lower, self.log, self.current_lang):
            return
        elif handle_web_command(query_lower, self.log, self.current_lang):
            return
        elif handle_office_command(query_lower, self.log, self.current_lang):
            return
        else:
            self.log("🤖 Thinking...")
            response = ask_gemini(query)
            self.log(f"🤖 Assistant: {response}")
            speak(response, self.current_lang)
    def update_telemetry(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.stats_label.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
        self.after(3000, self.update_telemetry)
