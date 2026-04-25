from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from config import MODEL

llm = Ollama(model=MODEL)


# ---------------------------
# STATE
# ---------------------------
def init_state(state, memory):
    return {
        "state": state,
        "memory": memory,
        "emotion": None,
        "goal": None,
        "plan": None,
        "action": None,
        "message": None,
        "reflection": None,
    }


# ---------------------------
# EMOTION AGENT
# ---------------------------
def emotion_node(data):
    state = data["state"]
    memory = data["memory"]

    prompt = f"""
Emotion agent.

Hunger: {state['hunger']}
Energy: {state['energy']}
Bond: {state['bond']}

Memory emotions:
{memory['emotions']}

Return ONE word:
happy, sad, anxious, calm, lonely
"""

    data["emotion"] = llm.invoke(prompt).strip().lower()
    return data


# ---------------------------
# GOAL AGENT
# ---------------------------
def goal_node(data):
    state = data["state"]
    emotion = data["emotion"]

    prompt = f"""
Goal agent.

Emotion: {emotion}
Hunger: {state['hunger']}
Energy: {state['energy']}

Choose:
eat | sleep | play | seek_attention | explore | rest
"""

    data["goal"] = llm.invoke(prompt).strip().lower()
    return data


# ---------------------------
# PLANNER AGENT
# ---------------------------
def planner_node(data):
    goal = data["goal"]

    plans = {
        "eat": "find food → eat",
        "sleep": "safe place → sleep",
        "play": "seek user → play",
        "seek_attention": "express emotion",
        "explore": "wander",
        "rest": "idle"
    }

    data["plan"] = plans.get(goal, "do nothing")
    return data


# ---------------------------
# ACTION AGENT
# ---------------------------
def action_node(data):
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

    res = llm.invoke(prompt)

    import json, re
    match = re.search(r"\{.*\}", res, re.DOTALL)

    if match:
        try:
            parsed = json.loads(match.group(0))
            data["action"] = parsed.get("action", "do_nothing")
            data["message"] = parsed.get("message", "")
        except:
            data["action"] = "do_nothing"
            data["message"] = "..."
    else:
        data["action"] = "do_nothing"
        data["message"] = "..."

    return data


# ---------------------------
# REFLECTION AGENT
# ---------------------------
def reflection_node(data):
    msg = data["message"]

    prompt = f"""
Reflect on this:

"{msg}"

Return one sentence feeling.
"""

    data["reflection"] = llm.invoke(prompt).strip()
    return data


# ---------------------------
# BUILD GRAPH
# ---------------------------
def build_graph():
    g = StateGraph(dict)

    g.add_node("emotion", emotion_node)
    g.add_node("goal", goal_node)
    g.add_node("plan", planner_node)
    g.add_node("action", action_node)
    g.add_node("reflect", reflection_node)

    g.set_entry_point("emotion")

    g.add_edge("emotion", "goal")
    g.add_edge("goal", "plan")
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