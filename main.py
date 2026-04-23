import time

from config import STATE_LIMITS
from engine.state import load_state, save_state, tick, clamp
from engine.mood import compute_mood
from engine.offline_sim import simulate_offline
from engine.commands import handle_command
from agent.prompt import build_prompt
from agent.brain import decide
from memory.memory import (
    update_memory,
    evolve_personality,
    add_offline_events,
    compress_memory
)
from ui.input_handler import InputHandler
from ui.render import render


# ---------------------------
# LOAD STATE + MEMORY
# ---------------------------
state, offline_time = load_state()

memory = {
    "emotions": {
        "attachment": 2,
        "neglect": 0,
        "trust": 5
    },
    "events": [],
    "summary": ""
}


# ---------------------------
# OFFLINE SIMULATION (CORE FEATURE)
# ---------------------------
state, memory, offline_events = simulate_offline(
    state,
    memory,
    compute_mood
)

memory = add_offline_events(memory, offline_events)

if offline_events:
    print("\n⏳ While you were away...")
    for e in offline_events[:3]:
        print("🐾", e)


# ---------------------------
# INPUT SYSTEM
# ---------------------------
input_handler = InputHandler(state)
input_handler.start()


# ---------------------------
# MAIN LOOP
# ---------------------------
TICK_RATE = 2

while True:

    # 1. world tick (basic simulation)
    state = tick(state)

    # 2. user command (if any)
    user_action = input_handler.get_last_action()
    state, user_feedback = handle_command(user_action, state)

    # 3. mood computation
    mood = compute_mood(state, memory)
    state["mood"] = mood

    # 4. LLM decision
    prompt = build_prompt(state, memory, mood)
    decision = decide(prompt)

    # 5. apply LLM action (via actions module)
    # (assuming your actions.py handles mapping)
    # If you already have apply_action, use it here:
    from engine.actions import apply_action
    state = apply_action(state, decision["action"])

    # 6. memory updates
    memory = update_memory(memory, decision, user_action)
    memory = evolve_personality(state, memory)

    # 7. compression (IMPORTANT)
    memory = compress_memory(memory)

    # 8. safety clamp
    state = clamp(state, STATE_LIMITS)

    # 9. persist everything
    save_state(state)

    # 10. render UI
    render(state, decision, user_feedback)

    time.sleep(TICK_RATE)