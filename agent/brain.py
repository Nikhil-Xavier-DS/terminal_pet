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


def reflect(state, memory, decision):
    prompt = f"""
You are reflecting on your recent action.

STATE:
{state}

DECISION:
{decision}

MEMORY SUMMARY:
{memory.get("summary", "")}

Answer in JSON:
{{
  "reflection": "...",
  "learning": "...",
  "adjustment": "increase_trust | decrease_trust | none"
}}
"""

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        text = res.json()["response"]
        return extract_json(text) or {}

    except:
        return {}


def llm_reason_goal(state, memory, drives):
    prompt = f"""
    You are deciding the next GOAL for a living digital creature.

    STATE:
    - Hunger: {state["hunger"]}
    - Energy: {state["energy"]}
    - Bond: {state["bond"]}

    EMOTIONS:
    {memory["emotions"]}

    DRIVES:
    {drives}

    MEMORY SUMMARY:
    {memory.get("summary", "")}

    RECENT EVENTS:
    {[e["text"] for e in memory["events"][-5:]]}

    ---

    Choose the most important goal.

    Allowed goals:
    - eat
    - sleep
    - play
    - seek_attention
    - explore
    - rest

    Return ONLY valid JSON:

    {{
    "type": "eat | sleep | play | seek_attention | explore | rest",
    "reason": "short explanation",
    "confidence": 0.0
    }}
    """
    
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        text = res.json()["response"]
        data = extract_json(text)

        # ---------------------------
        # VALIDATION LAYER (VERY IMPORTANT)
        # ---------------------------
        allowed = {
            "eat", "sleep", "play",
            "seek_attention", "explore", "rest"
        }

        if isinstance(data, dict):
            gtype = data.get("type", "rest")

            if isinstance(gtype, list):
                gtype = gtype[0] if gtype else "rest"

            gtype = str(gtype).strip().lower()

            if gtype not in allowed:
                gtype = "rest"

            return {
                "type": gtype,
                "reason": data.get("reason", ""),
                "confidence": float(data.get("confidence", 0.5))
            }

        return {"type": "rest", "reason": "fallback", "confidence": 0.1}

    except Exception as e:
        print("Goal LLM error:", e)
        return {"type": "rest", "reason": "error fallback", "confidence": 0.1}