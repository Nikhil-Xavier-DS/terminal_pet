def compute_drives(state, memory):
    e = memory["emotions"]

    boredom = memory.get("boredom", 0)

    drives = {
        "survival": (
            state["hunger"] * 0.7 +
            (10 - state["energy"]) * 0.3
        ),
        "attachment": e.get("attachment", 0),
        "fear": e.get("neglect", 0),
        "trust": e.get("trust", 0),
        "boredom": boredom,
        "curiosity": min(10, boredom * 0.8)
    }

    # clamp
    for k in drives:
        drives[k] = max(0, min(10, drives[k]))

    return drives