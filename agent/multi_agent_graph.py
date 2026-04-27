from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from agent.tool_registry import TOOLS
from config import MODEL
from collections import defaultdict
import json

llm = Ollama(model=MODEL)


# =========================================================
# INIT STATE
# =========================================================
def init_state(state, memory):
    return {
        "state": state,
        "memory": memory,

        # tools injected into graph state
        "tools": TOOLS,

        # agent outputs
        "emotion": None,
        "emotion_goal": None,
        "emotion_conf": 0,

        "rule_goal": None,
        "rule_conf": 0,

        "memory_goal": None,
        "memory_conf": 0,

        "goal": None,

        # tool system
        "tool_calls": [],
        "tool_results": None,

        # debug
        "decision_debug": None,
    }


# =========================================================
# TOOL ROUTER NODE
# =========================================================
def tool_router(data):
    calls = data.get("tool_calls", [])
    tools = data.get("tools", {})

    results = []

    for call in calls:
        tool_name = call.get("tool")
        args = call.get("args", {})

        if tool_name in tools:
            try:
                result = tools[tool_name](data)
                results.append({tool_name: result})
            except Exception as e:
                results.append({tool_name: {"error": str(e)}})

    data["tool_results"] = results
    data["tool_calls"] = []

    return data


# =========================================================
# EMOTION AGENT
# =========================================================
def emotion_agent(data):
    state = data["state"]

    prompt = f"""
You are an emotion agent.

TOOLS:
- memory_read
- time_tool

Return JSON ONLY:

{{
 "emotion": "happy|sad|lonely|calm|anxious|excited",
 "goal": "eat|sleep|play|seek_attention|rest",
 "confidence": 0.0-1.0,
 "tool_calls": [
   {{"tool": "memory_read", "args": {{}}}}
 ]
}}

State:
Hunger={state['hunger']}
Energy={state['energy']}
Bond={state['bond']}
"""

    try:
        parsed = json.loads(llm.invoke(prompt))

        data["emotion"] = parsed.get("emotion")
        data["emotion_goal"] = parsed.get("goal")
        data["emotion_conf"] = parsed.get("confidence", 0.5)
        data["tool_calls"] = parsed.get("tool_calls", [])

    except:
        data["tool_calls"] = []

    return data


# =========================================================
# RULE AGENT (NO TOOLS)
# =========================================================
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


# =========================================================
# MEMORY AGENT (TOOL-AWARE)
# =========================================================
def memory_agent(data):
    prompt = """
Use memory_read tool if needed.

Return JSON ONLY:
{
 "goal": "eat|sleep|play|seek_attention|rest",
 "confidence": 0.0-1.0,
 "tool_calls": [
   {"tool": "memory_read", "args": {}}
 ]
}
"""

    try:
        parsed = json.loads(llm.invoke(prompt))

        data["memory_goal"] = parsed.get("goal")
        data["memory_conf"] = parsed.get("confidence", 0.5)
        data["tool_calls"] = parsed.get("tool_calls", [])

    except:
        data["memory_goal"] = "rest"
        data["memory_conf"] = 0.5
        data["tool_calls"] = []

    return data


# =========================================================
# GOAL RESOLUTION (WEIGHTED VOTING)
# =========================================================
AGENT_WEIGHTS = {
    "emotion": 1.2,
    "rule": 1.6,
    "memory": 1.0
}


def resolve_goal(data):
    scores = defaultdict(float)

    agents = [
        ("emotion", data.get("emotion_goal"), data.get("emotion_conf")),
        ("rule", data.get("rule_goal"), data.get("rule_conf")),
        ("memory", data.get("memory_goal"), data.get("memory_conf")),
    ]

    debug = []

    for name, goal, conf in agents:
        if not goal:
            continue

        weight = AGENT_WEIGHTS.get(name, 1.0)
        score = weight * conf

        scores[goal] += score

        debug.append(f"{name}: {goal} ({conf:.2f}) → {score:.2f}")

    if not scores:
        data["goal"] = "rest"
        return data

    data["goal"] = max(scores, key=scores.get)
    data["decision_debug"] = {"details": debug}

    return data


# =========================================================
# PLANNER
# =========================================================
def planner(data):
    goal = data["goal"]

    plans = {
        "eat": "find food",
        "sleep": "rest safely",
        "play": "engage user",
        "seek_attention": "express emotion",
        "rest": "idle"
    }

    data["plan"] = plans.get(goal, "idle")
    return data


# =========================================================
# ACTION AGENT (TOOL-CAPABLE)
# =========================================================
def action_agent(data):
    goal = data["goal"]

    prompt = f"""
You are an action agent.

Goal: {goal}

Return JSON ONLY:
{{
 "action": "eat|sleep|play|seek_attention|do_nothing",
 "message": "...",
 "tool_calls": []
}}
"""

    try:
        parsed = json.loads(llm.invoke(prompt))

        data["action"] = parsed.get("action")
        data["message"] = parsed.get("message")
        data["tool_calls"] = parsed.get("tool_calls", [])

    except:
        data["tool_calls"] = []

    return data


# =========================================================
# REFLECTION AGENT (CAN WRITE MEMORY)
# =========================================================
def reflection_agent(data):
    msg = data.get("message", "")

    prompt = f"""
Reflect on:

{msg}

Return JSON ONLY:
{{
 "reflection": "...",
 "tool_calls": []
}}
"""

    try:
        parsed = json.loads(llm.invoke(prompt))

        data["reflection"] = parsed.get("reflection")
        data["tool_calls"] = parsed.get("tool_calls", [])

    except:
        data["tool_calls"] = []

    return data


# =========================================================
# ROUTING LOGIC
# =========================================================
def route_tools_or_next(next_node):
    def route(data):
        if data.get("tool_calls"):
            return "tool_router"
        return next_node
    return route


# =========================================================
# BUILD GRAPH
# =========================================================
def build_graph():
    g = StateGraph(dict)

    g.add_node("emotion", emotion_agent)
    g.add_node("rule", rule_agent)
    g.add_node("memory", memory_agent)
    g.add_node("resolve", resolve_goal)
    g.add_node("planner", planner)
    g.add_node("action", action_agent)
    g.add_node("reflect", reflection_agent)
    g.add_node("tool_router", tool_router)

    g.set_entry_point("emotion")

    # emotion → maybe tools → rule
    g.add_conditional_edges("emotion", route_tools_or_next("rule"))
    g.add_edge("tool_router", "emotion")

    # rule → memory
    g.add_edge("rule", "memory")

    # memory → maybe tools → resolve
    g.add_conditional_edges("memory", route_tools_or_next("resolve"))
    g.add_edge("tool_router", "memory")

    # resolve → planner
    g.add_edge("resolve", "planner")

    # planner → action
    g.add_edge("planner", "action")

    # action → maybe tools → reflect
    g.add_conditional_edges("action", route_tools_or_next("reflect"))
    g.add_edge("tool_router", "action")

    # reflect → maybe tools → END
    g.add_conditional_edges("reflect", route_tools_or_next("end"))
    g.add_edge("tool_router", "reflect")

    g.add_edge("reflect", END)

    return g.compile()


graph = build_graph()


# =========================================================
# PUBLIC API
# =========================================================
def run_multi_agent_graph(state, memory):
    data = init_state(state, memory)
    return graph.invoke(data)