from langchain_community.llms import Ollama
from config import MODEL

llm = Ollama(model=MODEL)


# ---------------------------
# 1. EMOTION AGENT
# ---------------------------
def emotion_agent(state, memory):
    prompt = f"""
You are Emotion Agent.

State:
Hunger: {state['hunger']}
Energy: {state['energy']}
Bond: {state['bond']}

Memory emotions:
{memory['emotions']}

Return ONE word emotion:
happy, sad, anxious, calm, lonely, excited
"""
    return llm.invoke(prompt).strip().lower()


# ---------------------------
# 2. GOAL AGENT
# ---------------------------
def goal_agent(state, memory, emotion):
    prompt = f"""
You are Goal Agent.

Emotion: {emotion}
Hunger: {state['hunger']}
Energy: {state['energy']}

Choose goal:
eat | sleep | play | seek_attention | explore | rest | do_nothing
"""
    return llm.invoke(prompt).strip().lower()


# ---------------------------
# 3. PLANNER AGENT
# ---------------------------
def planner_agent(goal):
    plans = {
        "eat": "find food → eat",
        "sleep": "find safe space → sleep",
        "play": "seek user → play",
        "seek_attention": "signal user → emotional expression",
        "explore": "wander environment",
        "rest": "idle recovery"
    }
    return plans.get(goal, "do nothing")


# ---------------------------
# 4. REFLECTION AGENT
# ---------------------------
def reflection_agent(message):
    prompt = f"""
You are Reflection Agent.

Event: {message}

Give one emotional reflection sentence.
"""
    return llm.invoke(prompt).strip()


# ---------------------------
# 5. ACTION AGENT
# ---------------------------
def action_agent(state, goal, emotion):
    prompt = f"""
You are Action Agent.

Goal: {goal}
Emotion: {emotion}

Return JSON:
{{
  "action": "eat|sleep|play|seek_attention|do_nothing",
  "message": "short expressive sentence"
}}
"""
    res = llm.invoke(prompt)

    import json, re

    match = re.search(r"\{.*\}", res, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    return {"action": "do_nothing", "message": "..."}