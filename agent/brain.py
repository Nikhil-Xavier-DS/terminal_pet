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
        "thought": "system fallback",
        "emotion": "confused",
        "goal": "do_nothing",
        "action": "do_nothing",
        "message": "...",
        "needs_user_action": False
    }


def decide(prompt):
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        text = res.json()["response"]
        data = extract_json(text)

        if isinstance(data, dict):
            return data

        return fallback()

    except Exception as e:
        print("LLM error:", e)
        return fallback()