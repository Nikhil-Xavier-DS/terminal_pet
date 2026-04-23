import requests
import json
import re
from config import MODEL, OLLAMA_URL


def extract_json(text):
    """
    Extract first JSON object from LLM response.
    """
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        pass
    return None


def fallback():
    return {
        "intent": "fallback",
        "action": "do_nothing",
        "emotion": "confused",
        "message": "...",
        "confidence": 0.0
    }


def decide(prompt):
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        text = res.json().get("response", "")

        parsed = extract_json(text)

        if isinstance(parsed, dict):
            return parsed

        print("⚠️ Invalid JSON from LLM. Using fallback.")
        return fallback()

    except Exception as e:
        print(f"⚠️ LLM error: {e}")
        return fallback()