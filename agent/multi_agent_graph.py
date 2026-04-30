from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.llms import Ollama
from langgraph.prebuilt import create_react_agent
from agent.tool_registry import TOOLS
from config import MODEL
from collections import defaultdict
import json


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",  # anything works
    model="local-model"
)


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


agent = create_react_agent(
    llm,
    tools=TOOLS
)


# =========================================================
# TOOL ROUTER NODE
# =========================================================
tool_node = ToolNode(TOOLS)


# =========================================================
# EMOTION AGENT
# =========================================================
def emotion_node(state):
    messages = state["messages"]

    response = llm.invoke(messages)

    return {
        "messages": messages + [response]
    }


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

    # 🧠 single intelligent agent node
    g.add_node("agent", agent)

    # 🛠 tool execution node (AUTOMATIC)
    g.add_node("tools", tool_node)

    g.set_entry_point("agent")

    # 🔁 LangGraph handles tool routing automatically
    g.add_conditional_edges(
        "agent",
        lambda x: "tools" if x.get("tool_calls") else END
    )

    g.add_edge("tools", "agent")

    return g.compile()


graph = build_graph()

def run(state, memory):
    return graph.invoke({
        "messages": [
            ("system", "You are a living pet agent.")
        ],
        "state": state,
        "memory": memory
    })


# =========================================================
# PUBLIC API
# =========================================================
def run_multi_agent_graph(state, memory):
    return graph.invoke({
        "messages": [
            ("system", "You are a virtual pet."),
            ("user", f"""
State Summary:
- hunger: {state.get('hunger')}
- energy: {state.get('energy')}
- bond: {state.get('bond')}
- mood: {state.get('mood')}

Memory summary:
- events: {len(memory.get('events', []))}
- personality: {memory.get('personality', {})}

Decide next action.
""")
        ]
    })