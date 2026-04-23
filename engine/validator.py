def validate(decision, state):
    action = decision.get("action", "do_nothing")

    if state["energy"] <= 1:
        action = "sleep"

    if state["hunger"] >= 9:
        action = "eat"

    if action == "play" and state["energy"] < 2:
        action = "sleep"

    decision["action"] = action
    return decision