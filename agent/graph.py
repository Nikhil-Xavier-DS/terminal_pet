from config import MODEL
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from agent.schemas import AgentDecision
import json, re


def parse_llm_output(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))
        return AgentDecision(**data)
    except Exception:
        return None

# ---------------------------
# LLM
# ---------------------------
llm = Ollama(model=MODEL)

# ---------------------------
# STATE SCHEMA
# ---------------------------
def init_graph_state(state, memory, mood):
    return {
        "state": state,
        "memory": memory,
        "mood": mood,
        "goal": None,
        "plan": None,
        "action": None,
        "reflection": None,
        "message": None,
    }


# ---------------------------
# NODE 1: GOAL REASONING
# ---------------------------
def goal_node(data):
    state = data["state"]
    mood = data["mood"]

    prompt = f"""
You are an AI creature.

State:
Hunger: {state['hunger']}
Energy: {state['energy']}
Mood: {mood}

Choose ONE goal:
eat | sleep | play | seek_attention | explore | rest

Respond ONLY with the goal.
"""

    goal = llm.invoke(prompt).strip().lower()

    data["goal"] = goal
    return data


# ---------------------------
# NODE 2: PLANNING
# ---------------------------
def plan_node(data):
    goal = data["goal"]

    plan_map = {
        "eat": "find food → eat",
        "sleep": "find safe place → sleep",
        "play": "seek user → play",
        "seek_attention": "signal user → express emotion",
        "explore": "look around → move",
        "rest": "stay still → recover",
    }

    data["plan"] = plan_map.get(goal, "do nothing")
    return data


# ---------------------------
# NODE 3: ACTION + EXPRESSION
# ---------------------------
def action_node(data):
    state = data["state"]
    memory = data["memory"]
    goal = data["goal"]

    prompt = f"""
Return JSON ONLY:

Goal: {goal}
State:
- Hunger: {state['hunger']}
- Energy: {state['energy']}
"""

    res = llm.invoke(prompt)

    parsed = parse_llm_output(res)

    if parsed:
        data["action"] = parsed.action
        data["message"] = parsed.message
        data["reflection"] = parsed.reflection
        data["goal"] = parsed.goal
    else:
        data["action"] = "do_nothing"
        data["message"] = "..."
        data["reflection"] = None

    return data


# ---------------------------
# NODE 4: REFLECTION (NEW POWER)
# ---------------------------
def reflect_node(data):
    memory = data["memory"]
    message = data["message"]

    prompt = f"""
Reflect briefly on this experience:

"{message}"

Return one sentence about how you feel.
"""

    reflection = llm.invoke(prompt)
    data["reflection"] = reflection.strip()

    return data


# ---------------------------
# BUILD GRAPH
# ---------------------------
def build_graph():
    graph = StateGraph(dict)

    graph.add_node("goal", goal_node)
    graph.add_node("plan", plan_node)
    graph.add_node("action", action_node)
    graph.add_node("reflect", reflect_node)

    graph.set_entry_point("goal")

    graph.add_edge("goal", "plan")
    graph.add_edge("plan", "action")
    graph.add_edge("action", "reflect")
    graph.add_edge("reflect", END)

    return graph.compile()


# ---------------------------
# PUBLIC API (REPLACES decide)
# ---------------------------
graph = build_graph()

def run_agent(state, memory, mood):
    data = init_graph_state(state, memory, mood)
    result = graph.invoke(data)

    return {
        "action": result.get("action"),
        "message": result.get("message"),
        "goal": result.get("goal"),
        "reflection": result.get("reflection"),
    }