import requests
import json
import re
from config import MODEL, OLLAMA_URL


def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        return None
    return None


def fallback():
    return {
        "emotion": "neutral",
        "message": "...",
        "mood": "calm",
        "needs_user_action": False
    }


def call_llm(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    text = res.json()["response"]
    return extract_json(text)


def decide(prompt, action, goal, thought):
    try:
        data = call_llm(prompt)

        if not isinstance(data, dict):
            data = fallback()

    except Exception as e:
        print("LLM error:", e)
        data = fallback()

    # 🔥 inject real cognition
    data["action"] = action
    data["goal"] = goal["type"]
    data["thought"] = thought

    return data