import json
import os
import time

MEMORY_FILE = "data/memory.json"


# ---------------------------
# DEFAULT STRUCTURE
# ---------------------------
def default_memory():
    return {
        "events": [],
        "summary": "",
        "emotions": {
            "attachment": 5.0,
            "neglect": 0.0,
            "trust": 5.0
        },
        "user_patterns": {
            "last_feed_time": None,
            "feed_intervals": [],
            "responsiveness": 1.0
        },
        "identity": {
            "self_image": "I am a small evolving creature.",
            "history": []
        },
        "boredom": 0.0,
        "personality_shift": None,
        "personality_arc": {
            "type": "neutral",
            "stability": 0.0,
            "history": []
            },
        "emotion_history": []
    }


# ---------------------------
# INIT + AUTO-UPGRADE
# ---------------------------
def init_memory():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        return upgrade_memory(memory)

    return default_memory()


def reflect_identity(memory):
    e = memory["emotions"]

    reflection = None

    if e["neglect"] > 7:
        reflection = "I think I've become more anxious when alone."

    elif e["attachment"] > 8:
        reflection = "I feel deeply connected to you now."

    elif e["trust"] < 3:
        reflection = "I'm not sure I trust you as much anymore."

    if reflection:
        memory["identity"]["self_image"] = reflection
        memory["identity"]["history"].append({
            "text": reflection,
            "time": time.time()
        })

    return memory


def upgrade_memory(memory):
    """Ensure old memory files get new fields safely"""

    defaults = default_memory()

    # ---------------------------
    # TOP-LEVEL KEYS
    # ---------------------------
    for key, value in defaults.items():
        if key not in memory:
            memory[key] = value

    # ---------------------------
    # EMOTIONS
    # ---------------------------
    if "emotions" not in memory:
        memory["emotions"] = defaults["emotions"]

    for k, v in defaults["emotions"].items():
        if k not in memory["emotions"]:
            memory["emotions"][k] = v

    if "boredom" not in memory:
        memory["boredom"] = 0.0

    if "identity" not in memory:
        memory["identity"] = {
            "self_image": "I am a small evolving creature.",
            "history": []
            }

    # ---------------------------
    # USER PATTERNS
    # ---------------------------
    if "user_patterns" not in memory:
        memory["user_patterns"] = defaults["user_patterns"]

    for k, v in defaults["user_patterns"].items():
        if k not in memory["user_patterns"]:
            memory["user_patterns"][k] = v

    if "personality_arc" not in memory:
        memory["personality_arc"] = {
            "type": "neutral",
            "stability": 0.0,
            "history": []
        }

    if "emotion_history" not in memory:
        memory["emotion_history"] = []

    # ---------------------------
    # 🔥 EVENT FORMAT MIGRATION
    # ---------------------------
    upgraded_events = []

    for e in memory.get("events", []):
        if isinstance(e, str):
            # old format → convert
            upgraded_events.append({
                "text": e,
                "importance": 0.3,
                "time": time.time()
            })
        elif isinstance(e, dict):
            # ensure required keys exist
            upgraded_events.append({
                "text": e.get("text", ""),
                "importance": e.get("importance", 0.3),
                "time": e.get("time", time.time())
            })

    memory["events"] = upgraded_events

    return memory


def update_boredom(memory, user_action):
    if user_action:
        memory["boredom"] = max(0, memory.get("boredom", 0) - 2)
    else:
        memory["boredom"] += 0.2

    memory["boredom"] = max(0, min(10, memory["boredom"]))
    return memory


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# ---------------------------
# MEMORY UPDATE
# ---------------------------
def update_memory(memory, decision, user_action=None):
    event = {
        "text": decision.get("message", ""),
        "importance": compute_importance(memory),
        "time": time.time()
    }

    memory["events"].append(event)

    if len(memory["events"]) > 100:
        memory["events"] = memory["events"][-100:]

    if decision.get("goal") == "seek_attention":
        memory["emotions"]["attachment"] += 0.3

    if user_action is None:
        memory["emotions"]["neglect"] += 0.1

    if user_action == "feed":
        memory["emotions"]["trust"] += 0.2
        memory["emotions"]["attachment"] += 0.1
        update_feed_pattern(memory)

    return memory


# ---------------------------
# IMPORTANCE
# ---------------------------
def compute_importance(memory):
    e = memory["emotions"]

    score = 0.0

    if e["neglect"] > 6:
        score += 0.5

    if e["attachment"] > 7:
        score += 0.3

    return min(1.0, score)


# ---------------------------
# USER PATTERN LEARNING
# ---------------------------
def update_feed_pattern(memory):
    now = time.time()
    patterns = memory["user_patterns"]

    last = patterns["last_feed_time"]

    if last:
        interval = now - last
        patterns["feed_intervals"].append(interval)
        patterns["feed_intervals"] = patterns["feed_intervals"][-20:]

    patterns["last_feed_time"] = now


def adapt_personality(memory):
    patterns = memory["user_patterns"]

    if patterns["feed_intervals"]:
        avg = sum(patterns["feed_intervals"]) / len(patterns["feed_intervals"])

        if avg > 300:
            memory["emotions"]["neglect"] += 0.2
        else:
            memory["emotions"]["trust"] += 0.1

    return memory


# ---------------------------
# COMPRESSION
# ---------------------------
def compress_memory(memory):
    events = memory["events"]

    important = [e for e in events if e["importance"] > 0.6]
    recent = events[-10:]

    merged = important + recent
    unique = {e["time"]: e for e in merged}

    memory["events"] = list(unique.values())

    if len(memory["events"]) > 20:
        memory["summary"] = "Mochi remembers emotional patterns of care, absence, and interaction."

    return memory


# ---------------------------
# OFFLINE EVENTS
# ---------------------------
def add_offline_events(memory, events):
    if not events:
        return memory

    for e in events:
        memory["events"].append({
            "text": e,
            "importance": 0.5,
            "time": time.time()
        })

    return memory


# ---------------------------
# PERSONALITY EVOLUTION
# ---------------------------
def evolve_personality(state, memory):
    neg = memory["emotions"]["neglect"]
    att = memory["emotions"]["attachment"]

    if neg > 8:
        memory["personality_shift"] = "anxious and clingy"

    elif att > 8:
        memory["personality_shift"] = "deeply affectionate"

    elif state["bond"] > 8:
        memory["personality_shift"] = "loyal companion"

    return memory


def generate_life_story(memory):
    events = memory["events"][-20:]
    identity = memory.get("identity", {})

    story = []

    for e in events:
        story.append(e["text"])

    if identity.get("history"):
        story.append("I have changed over time.")

        for h in identity["history"][-3:]:
            story.append(h["text"])

    return " ".join(story)


def update_emotion_history(memory):
    e = memory["emotions"]

    snapshot = {
        "attachment": e["attachment"],
        "neglect": e["neglect"],
        "trust": e["trust"],
        "time": time.time()
    }

    memory["emotion_history"].append(snapshot)

    # keep last ~200 points
    memory["emotion_history"] = memory["emotion_history"][-200:]

    return memory


def update_personality_arc(memory):
    history = memory["emotion_history"]

    if len(history) < 20:
        return memory

    # take recent window
    recent = history[-50:]

    avg_attachment = sum(x["attachment"] for x in recent) / len(recent)
    avg_neglect = sum(x["neglect"] for x in recent) / len(recent)
    avg_trust = sum(x["trust"] for x in recent) / len(recent)

    current_arc = memory["personality_arc"]["type"]
    new_arc = current_arc

    # arc detection logic
    if avg_neglect > 7:
        new_arc = "anxious"

    elif avg_attachment > 8 and avg_trust > 6:
        new_arc = "secure"

    elif avg_trust < 3:
        new_arc = "withdrawn"

    elif avg_attachment > 7:
        new_arc = "affectionate"

    # stability system (prevents rapid flipping)
    if new_arc == current_arc:
        memory["personality_arc"]["stability"] += 0.1
    else:
        memory["personality_arc"]["stability"] -= 0.2

    # threshold to switch
    if memory["personality_arc"]["stability"] < -1:
        memory["personality_arc"]["type"] = new_arc
        memory["personality_arc"]["stability"] = 0

        memory["personality_arc"]["history"].append({
            "arc": new_arc,
            "time": time.time()
        })

    return memory
