import random

def generate_thought(state, memory, goal):
    g = goal.get("type")

    if state["hunger"] > 8:
        return "I'm really hungry..."

    if memory["emotions"]["neglect"] > 6:
        return "Why haven't they come back?"

    if g == "play":
        return "I want to spend time together."

    if g == "seek_attention":
        return "I need them to notice me."

    if g == "explore":
        thoughts = [
            "I wonder what's out there...",
            "Maybe I should do something fun.",
            "I'm getting bored...",
            "I want something new."
        ]
        return random.choice(thoughts)

    if state["energy"] < 3:
        return "I'm so tired..."

    return "Just existing..."