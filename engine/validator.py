def validate(decision, state):
    decision = normalize_decision(decision)

    action = decision.get("action", "do_nothing")

    if state["energy"] <= 1:
        action = "sleep"

    if state["hunger"] >= 9:
        action = "eat"

    if action == "play" and state["energy"] < 2:
        action = "sleep"

    decision["action"] = action
    return decision



def normalize_decision(decision):
    if not isinstance(decision, dict):
        return {"action": "do_nothing"}

    action = decision.get("action", "do_nothing")

    # 🔥 Fix: handle list, None, weird types
    if isinstance(action, list):
        action = action[0] if action else "do_nothing"

    if not isinstance(action, str):
        action = str(action)

    decision["action"] = action.lower().strip()

    return decision