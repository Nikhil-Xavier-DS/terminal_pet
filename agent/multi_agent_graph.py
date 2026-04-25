from collections import defaultdict
import json, re
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from pydantic import ValidationError

from config import MODEL
from agent.schemas import EmotionOutput, MemoryOutput, ActionOutput, ReflectionOutput

llm = Ollama(model=MODEL)

AGENT_WEIGHTS = {
    "emotion": 1.2,
    "rule": 1.6,     # survival should dominate
    "memory": 1.0
}

# ---------------------------
# INIT STATE
# ---------------------------
def init_state(state, memory):
    return {
        "state": state,
        "memory": memory,

        # agent outputs
        "emotion": None,
        "emotion_goal": None,
        "rule_goal": None,
        "memory_goal": None,

        # resolved
        "goal": None,
        "plan": None,
        "action": None,
        "message": None,
        "reflection": None,
    }


# ---------------------------
# 1. EMOTION AGENT
# ---------------------------
def emotion_agent(data):
    state = data["state"]

    prompt = f"""
Emotion agent.

Hunger: {state['hunger']}
Energy: {state['energy']}
Bond: {state['bond']}

Return JSON:
{{
 "emotion": "...",
 "goal": "eat|sleep|play|seek_attention|explore|rest",
 "confidence": 0.0-1.0
}}
"""

    try:
        raw = llm.invoke(prompt)

        # 🔥 force validation
        result = EmotionOutput.model_validate_json(raw)

        data["emotion"] = result.emotion
        data["emotion_goal"] = result.goal
        data["emotion_conf"] = result.confidence

    except ValidationError:
        data["emotion"] = "calm"
        data["emotion_goal"] = "rest"
        data["emotion_conf"] = 0.5

    return data


# ---------------------------
# 2. RULE AGENT (NO LLM)
# ---------------------------
def rule_agent(data):
    state = data["state"]

    if state["hunger"] > 8:
        data["rule_goal"] = "eat"
        data["rule_conf"] = 0.9
    elif state["energy"] < 2:
        data["rule_goal"] = "sleep"
        data["rule_conf"] = 0.85
    else:
        data["rule_goal"] = "play"
        data["rule_conf"] = 0.6

    return data


# ---------------------------
# 3. MEMORY AGENT
# ---------------------------
def memory_agent(data):
    memory = data["memory"]
    recent = memory.get("events", [])[-5:]

    prompt = f"""
Memory agent.

Recent events:
{recent}

Return JSON:
{{
 "goal": "eat|sleep|play|seek_attention|explore|rest",
 "confidence": 0.0-1.0
}}
"""

    try:
        raw = llm.invoke(prompt)
        result = MemoryOutput.model_validate_json(raw)

        data["memory_goal"] = result.goal
        data["memory_conf"] = result.confidence

    except ValidationError:
        data["memory_goal"] = "rest"
        data["memory_conf"] = 0.5

    return data


# ---------------------------
# 4. GOAL RESOLUTION (VOTING)
# ---------------------------
def normalize_goal(goal):
    # handle list
    if isinstance(goal, list):
        return goal[0] if goal else None

    # handle None
    if goal is None:
        return None

    # convert to string
    if not isinstance(goal, str):
        goal = str(goal)

    return goal.strip().lower()

def resolve_goal(data):
    scores = defaultdict(float)

    # collect votes
    agents = [
        ("emotion", data.get("emotion_goal"), data.get("emotion_conf", 0)),
        ("rule", data.get("rule_goal"), data.get("rule_conf", 0)),
        ("memory", data.get("memory_goal"), data.get("memory_conf", 0)),
    ]

    debug = []

    for name, goal, conf in agents:
        goal = normalize_goal(goal)

        if not goal:
            continue

        weight = AGENT_WEIGHTS.get(name, 1.0)
        score = weight * conf

        scores[goal] += score

        debug.append(f"{name}: {goal} (conf={conf:.2f}, weight={weight}) → {score:.2f}")

    if not scores:
        data["goal"] = "do_nothing"
        return data

    # pick highest score
    best_goal = max(scores, key=scores.get)

    data["goal"] = best_goal

    # 🔥 OPTIONAL: introspection (VERY COOL)
    data["decision_debug"] = {
        "scores": dict(scores),
        "details": debug
    }

    return data


# ---------------------------
# 5. PLANNER
# ---------------------------
def planner(data):
    goal = data["goal"]

    plans = {
        "eat": "find food → eat",
        "sleep": "rest safely",
        "play": "engage user",
        "seek_attention": "express emotion",
        "explore": "wander",
        "rest": "idle"
    }

    data["plan"] = plans.get(goal, "idle")
    return data


# ---------------------------
# 6. ACTION AGENT
# ---------------------------
def action_agent(data):
    goal = data["goal"]
    emotion = data["emotion"]

    prompt = f"""
Action agent.

Goal: {goal}
Emotion: {emotion}

Return JSON:
{{
 "action": "eat|sleep|play|seek_attention|do_nothing",
 "message": "..."
}}
"""
    try:
        raw = llm.invoke(prompt)
        result = ActionOutput.model_validate_json(raw)

        data["action"] = result.action
        data["message"] = result.message

    except ValidationError:
        data["action"] = "do_nothing"
        data["message"] = "..."

    return data


# ---------------------------
# 7. REFLECTION AGENT
# ---------------------------
def reflection_agent(data):
    msg = data["message"]

    prompt = f"""
Reflect:

"{msg}"

Return one sentence.
"""
    try:
        raw = llm.invoke(prompt)
        result = ReflectionOutput.model_validate_strings(raw)

        data["reflection"] = result.strip()
    
    except ValidationError:
        data["reflection"] = "..."

    return data


# ---------------------------
# BUILD GRAPH
# ---------------------------
def build_graph():
    g = StateGraph(dict)

    g.add_node("emotion", emotion_agent)
    g.add_node("rule", rule_agent)
    g.add_node("memory", memory_agent)

    g.add_node("resolve", resolve_goal)
    g.add_node("plan", planner)
    g.add_node("action", action_agent)
    g.add_node("reflect", reflection_agent)

    g.set_entry_point("emotion")

    # parallel-ish branches (sequential execution but independent logic)
    g.add_edge("emotion", "rule")
    g.add_edge("rule", "memory")
    g.add_edge("memory", "resolve")

    g.add_edge("resolve", "plan")
    g.add_edge("plan", "action")
    g.add_edge("action", "reflect")

    g.add_edge("reflect", END)

    return g.compile()


graph = build_graph()


# ---------------------------
# PUBLIC API
# ---------------------------
def run_multi_agent_graph(state, memory):
    data = init_state(state, memory)
    result = graph.invoke(data)

    return {
        "emotion": result.get("emotion"),
        "goal": result.get("goal"),
        "action": result.get("action"),
        "message": result.get("message"),
        "reflection": result.get("reflection"),
    }