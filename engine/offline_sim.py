import time

def simulate_offline(state, memory, mood_func):
    now = time.time()
    last = state.get("last_seen", now)

    elapsed = now - last

    if elapsed < 5:
        return state, memory, []

    events = []

    ticks = int(elapsed // 10)  # simulate every 10 seconds chunk

    for _ in range(min(ticks, 50)):  # cap to avoid explosion
        # basic simulation
        state["hunger"] += 0.2
        state["energy"] -= 0.15

        # emotional drift
        memory["emotions"]["neglect"] += 0.05

        # occasional "thoughts"
        if state["hunger"] > 7:
            events.append("I felt hungry while waiting...")

        if memory["emotions"]["neglect"] > 5:
            events.append("I wondered if you would come back.")

    # clamp
    state["hunger"] = min(state["hunger"], 10)
    state["energy"] = max(state["energy"], 0)

    state["last_seen"] = now

    return state, memory, events