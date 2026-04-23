import requests
import json
from config import MODEL, OLLAMA_URL

def decide(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    text = res.json()["response"]

    try:
        return json.loads(text)
    except:
        return {
            "intent": "fallback",
            "action": "do_nothing",
            "emotion": "confused",
            "message": "..."
        }