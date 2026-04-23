import json, os, time

STATE_FILE = "data/state.json"

# rates per second
HUNGER_RATE = 0.0005     # increase per second
ENERGY_DECAY = 0.0004    # decrease per second

def init_state():
    return {
        "hunger": 5,
        "energy": 7,
        "bond": 3,
        "mood": "neutral",
        "last_seen": 0,
        "offline_log": []
    }

def apply_offline_progress(state):
    now = time.time()
    last_seen = state.get("last_seen", now)

    elapsed = now - last_seen

    if elapsed <= 0:
        return state, 0

    # apply decay
    state["hunger"] += elapsed * HUNGER_RATE
    state["energy"] -= elapsed * ENERGY_DECAY

    return state, elapsed


def load_state():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = init_state()

    # 🔥 apply offline simulation
    state, elapsed = apply_offline_progress(state)

    return state, elapsed


def save_state(state):
    state["last_seen"] = time.time()

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def tick(state):
    state["hunger"] += 0.3
    state["energy"] -= 0.2
    return state


def clamp(state, limits):
    for k, (lo, hi) in limits.items():
        if k != "last_seen":
            state[k] = max(lo, min(hi, state[k]))
    return state