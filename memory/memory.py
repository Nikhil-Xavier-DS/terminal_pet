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

    if user_action == "fed":
        memory["emotions"]["trust"] += 0.3
        memory["emotions"]["attachment"] += 0.2

    if user_action == "played":
        memory["emotions"]["attachment"] += 0.4

    if user_action == "too_tired":
        memory["emotions"]["neglect"] += 0.1

    if decision["action"] == "seek_attention":
        memory["emotions"]["attachment"] += 0.2

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