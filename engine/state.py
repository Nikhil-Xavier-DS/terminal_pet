import json, os, random

STATE_FILE = "data/state.json"

def init_state():
    return {
        "hunger": 5,
        "energy": 7,
        "bond": 3
    }

def tick(state):
    state["hunger"] += 0.3
    state["energy"] -= 0.2
    return state

def clamp(state, limits):
    for k, (lo, hi) in limits.items():
        state[k] = max(lo, min(hi, state[k]))
    return state

def load_state():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return init_state()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)