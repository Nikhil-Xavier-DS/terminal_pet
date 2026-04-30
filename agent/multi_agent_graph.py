from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_openai import ChatOpenAI
from agent.tool_registry import TOOLS
from collections import defaultdict
import json
import re

# =========================================================
# LLM (LM STUDIO / OPENAI COMPATIBLE)
# =========================================================
llm = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0.7
)

# =========================================================
# SAFE JSON PARSER (CRITICAL FIX)
# =========================================================
def safe_json_parse(text: str):
    if not text:
        return {}

    text = str(text).strip()
    text = re.sub(r"```json|```", "", text)

    try:
        return json.loads(text)
    except:
        pass

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return {}


# =========================================================
# REACT EXECUTOR (TOOLS ENABLED)
# =========================================================
react_agent = create_react_agent(llm, tools=TOOLS)
tool_node = ToolNode(TOOLS)


# =========================================================
# INIT STATE
# =========================================================
def init_state(state, memory):
    return {
        "state": state,
        "memory": memory,

        "emotion_goal": None,
        "emotion_conf": 0,

        "rule_goal": None,
        "rule_conf": 0,

        "memory_goal": None,
        "memory_conf": 0,

        "planner_goal": None,
        "planner_conf": 0,

        "goal": None,
        "action_result": None,
        "decision_debug": {}
    }


# =========================================================
# 1. EMOTION AGENT (LLM + SAFE PARSE)
# =========================================================
def emotion_agent(data):
    s = data["state"]

    prompt = f"""
Return ONLY JSON:

{{"goal":"eat|sleep|play|rest","confidence":0-1}}

State:
hunger={s['hunger']}
energy={s['energy']}
bond={s['bond']}
mood={s.get('mood')}
"""

    raw = llm.invoke(prompt)
    res = safe_json_parse(raw.content if hasattr(raw, "content") else str(raw))

    data["emotion_goal"] = res.get("goal", "rest")
    data["emotion_conf"] = float(res.get("confidence", 0.5))
    return data


# =========================================================
# 2. RULE AGENT (DETERMINISTIC)
# =========================================================
def rule_agent(data):
    s = data["state"]

    if s["hunger"] > 8:
        g, c = "eat", 0.95
    elif s["energy"] < 2:
        g, c = "sleep", 0.9
    else:
        g, c = "play", 0.6

    data["rule_goal"] = g
    data["rule_conf"] = c
    return data


# =========================================================
# 3. MEMORY AGENT (SAFE + LIGHTWEIGHT)
# =========================================================
def memory_agent(data):
    recent = data["memory"].get("events", [])[-5:]

    prompt = f"""
Memory:
{recent}

Return ONLY JSON:
{{"goal":"eat|sleep|play|rest","confidence":0-1}}
"""

    raw = llm.invoke(prompt)
    res = safe_json_parse(raw.content if hasattr(raw, "content") else str(raw))

    data["memory_goal"] = res.get("goal", "rest")
    data["memory_conf"] = float(res.get("confidence", 0.5))
    return data


# =========================================================
# 4. PLANNER AGENT
# =========================================================
def planner_agent(data):
    prompt = f"""
Combine:

Emotion: {data['emotion_goal']}
Rule: {data['rule_goal']}
Memory: {data['memory_goal']}

Return ONLY JSON:
{{"goal":"eat|sleep|play|rest","confidence":0-1}}
"""

    raw = llm.invoke(prompt)
    res = safe_json_parse(raw.content if hasattr(raw, "content") else str(raw))

    data["planner_goal"] = res.get("goal", "rest")
    data["planner_conf"] = float(res.get("confidence", 0.5))
    return data


# =========================================================
# 5. WEIGHTED RESOLVER
# =========================================================
WEIGHTS = {
    "emotion": 1.2,
    "rule": 1.6,
    "memory": 1.0,
    "planner": 1.3
}

def resolve_goal(data):
    scores = defaultdict(float)
    debug = []

    agents = [
        ("emotion", data["emotion_goal"], data["emotion_conf"]),
        ("rule", data["rule_goal"], data["rule_conf"]),
        ("memory", data["memory_goal"], data["memory_conf"]),
        ("planner", data["planner_goal"], data["planner_conf"]),
    ]

    for name, goal, conf in agents:
        if not goal:
            continue

        score = WEIGHTS[name] * float(conf)
        scores[goal] += score
        debug.append(f"{name}: {goal} → {score:.2f}")

    data["goal"] = max(scores, key=scores.get) if scores else "rest"
    data["decision_debug"] = {"details": debug}
    return data


# =========================================================
# 6. EXECUTION AGENT (REACT + TOOLS)
# =========================================================
def execute_agent(data):
    goal = data["goal"]

    result = react_agent.invoke({
        "messages": [
            ("system", "You are the execution engine of a virtual pet. Use tools if needed."),
            ("user", f"Execute goal: {goal}")
        ],
        "state": data["state"],
        "memory": data["memory"]
    })

    data["action_result"] = result["messages"][-1].content
    return data


# =========================================================
# TOOL ROUTER
# =========================================================
def tool_router(state):
    return "tools" if state.get("tool_calls") else END


# =========================================================
# BUILD GRAPH
# =========================================================
def build_graph():
    g = StateGraph(dict)

    g.add_node("emotion", emotion_agent)
    g.add_node("rule", rule_agent)
    g.add_node("memory", memory_agent)
    g.add_node("planner", planner_agent)
    g.add_node("resolver", resolve_goal)

    g.add_node("execute", execute_agent)
    g.add_node("tools", tool_node)

    g.set_entry_point("emotion")

    g.add_edge("emotion", "rule")
    g.add_edge("rule", "memory")
    g.add_edge("memory", "planner")
    g.add_edge("planner", "resolver")
    g.add_edge("resolver", "execute")

    g.add_conditional_edges("execute", tool_router)
    g.add_edge("tools", "execute")

    return g.compile()


graph = build_graph()


# =========================================================
# PUBLIC API
# =========================================================
def run_multi_agent_graph(state, memory):
    return graph.invoke(init_state(state, memory))