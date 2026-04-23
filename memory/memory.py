import json, os

MEMORY_FILE = "data/memory.json"

def init_memory():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(MEMORY_FILE):
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

    if decision["action"] == "seek_attention":
        memory["emotions"]["attachment"] += 0.2

    if user_action == "ignore":
        memory["emotions"]["neglect"] += 0.3
        memory["emotions"]["attachment"] -= 0.1

    return memory