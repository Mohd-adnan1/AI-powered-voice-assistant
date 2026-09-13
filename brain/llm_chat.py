import sqlite3
from google import genai
from config import GEMINI_API_KEY

# Setup SQLite context storage
conn = sqlite3.connect("assistant_memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS memory (user_query TEXT, bot_response TEXT)")
conn.commit()

# Initialize Client
client = None

def ask_gemini(prompt: str) -> str:
    """Queries Gemini API while incorporating past memory context."""
    global client
    
    if not GEMINI_API_KEY:
        return "Error: No API key found. Please paste your Gemini API key inside API.txt and restart."

    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        # Retrieve last 3 conversations for context
        cursor.execute("SELECT user_query, bot_response FROM memory ORDER BY rowid DESC LIMIT 3")
        history = cursor.fetchall()
        
        context = "System Instruction: You are a desktop AI assistant. Keep answers concise, clear, and direct for voice reading.\n"
        for q, r in reversed(history):
            context += f"User: {q}\nAssistant: {r}\n"
        
        full_prompt = f"{context}User: {prompt}\nAssistant:"
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt,
        )

        reply = getattr(response, "text", None)
        if reply is None:
            candidates = getattr(response, "candidates", None) or []
            for candidate in candidates:
                content = getattr(candidate, "content", None)
                if content is None:
                    continue
                parts = getattr(content, "parts", None) or []
                for part in parts:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        reply = part_text
                        break
                if reply is not None:
                    break
        if reply is None:
            return "I couldn't generate a response for that request."

        reply = reply.strip()

        # Save interaction to database
        cursor.execute("INSERT INTO memory VALUES (?, ?)", (prompt, reply))
        conn.commit()
        return reply

    except Exception as e:
        return f"I ran into an issue processing that: {e}"
    

def parse_and_execute_agent_plan(command: str, executor_fn) -> str:
    """Uses Gemini to break complex multi-step user prompts into sequential tool actions."""
    global client

    if not GEMINI_API_KEY:
        return "Error: No API key found. Please paste your Gemini API key inside API.txt and restart."

    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)

    assert client is not None

    prompt = f"""
    Break down the following user request into a simple Python list of discrete actions:
    User Request: '{command}'
    Available actions: ['search google', 'create ppt', 'create document', 'take screenshot', 'open youtube']
    Return ONLY a valid JSON list of strings, e.g., ["search google AI news", "create document on AI news"].
    """
    try:
        response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
        import json
        response_text = getattr(response, "text", None)
        if not response_text:
            raise ValueError("Gemini returned an empty response.")
        steps = json.loads(response_text.strip())
        for step in steps:
            executor_fn(step)
        return f"Successfully executed {len(steps)} sequential autonomous steps."
    except Exception as e:
        return f"Agent planning failed: {e}"    