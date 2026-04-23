def compute_mood(state, memory):
    e = memory["emotions"]

    if e["neglect"] > 5:
        return "lonely"

    if state["hunger"] > 8:
        return "irritated"

    if state["bond"] > 7:
        return "affectionate"

    if state["energy"] < 3:
        return "tired"

    if e["attachment"] > 6:
        return "needy"

    return "calm"