import json, os

MEMORY_FILE = "data/memory.json"

def init_memory():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(MEMORY_FILE) and os.stat(MEMORY_FILE).st_size != 0:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    return {
        "events": [],
        "emotions": {
            "attachment": 5.0,
            "neglect": 0.0,
            "trust": 5.0
        }
    }

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(memory, decision, user_action=None):
    memory["events"].append(decision.get("message", ""))

    if len(memory["events"]) > 50:
        memory["events"] = memory["events"][-50:]

    # emotional drift based on goals
    if decision.get("goal") == "seek_attention":
        memory["emotions"]["attachment"] += 0.3

    if user_action is None:
        memory["emotions"]["neglect"] += 0.1

    if user_action == "feed":
        memory["emotions"]["trust"] += 0.2
        memory["emotions"]["attachment"] += 0.1

    return memory

def compress_memory(memory):
    events = memory["events"]

    if len(events) > 20:
        summary = "Pet remembers being cared for and interacting over time."

        memory["summary"] = summary
        memory["events"] = events[-10:]  # keep only recent

    return memory

def apply_absence_effect(memory, offline_time):
    if offline_time <= 0:
        return memory

    if offline_time > 300:  # 5 min
        memory["emotions"]["neglect"] += 0.5
        memory["emotions"]["attachment"] -= 0.2

    if offline_time > 3600:  # 1 hour
        memory["emotions"]["neglect"] += 1.0
        memory["emotions"]["trust"] -= 0.3

    return memory

def update_personality(state, memory):
    # drift bond affects attachment baseline
    if state["bond"] > 7:
        memory["emotions"]["attachment"] += 0.1

    if memory["emotions"]["neglect"] > 6:
        memory["emotions"]["trust"] -= 0.1

    # clamp
    for k in memory["emotions"]:
        memory["emotions"][k] = max(0, min(10, memory["emotions"][k]))

    return memory

def add_offline_events(memory, events):
    if not events:
        return memory

    for e in events:
        memory["events"].append(e)

    # compress if too large
    if len(memory["events"]) > 30:
        memory["summary"] = "The creature has experienced long periods of waiting and interaction with its user."
        memory["events"] = memory["events"][-15:]

    return memory

def evolve_personality(state, memory):
    neg = memory["emotions"]["neglect"]
    att = memory["emotions"]["attachment"]

    # loneliness evolution
    if neg > 8:
        memory["personality_shift"] = "anxious and clingy"

    if att > 8:
        memory["personality_shift"] = "deeply affectionate"

    if state["bond"] > 8:
        memory["personality_shift"] = "loyal companion"

    return memory