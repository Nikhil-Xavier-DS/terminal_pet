import time

from config import TICK_RATE, STATE_LIMITS, MODEL
from agent.ollama_utils import ensure_model

from engine.state import load_state, save_state, tick, clamp
from engine.actions import apply_action
from engine.validator import validate
from engine.commands import handle_command

from agent.prompt import build_prompt
from agent.brain import decide

from memory.memory import init_memory, update_memory, save_memory, apply_absence_effect
from ui.render import render
from ui.input_handler import InputHandler

def format_time(seconds):
    mins = int(seconds // 60)
    hours = int(mins // 60)

    if hours > 0:
        return f"{hours}h"
    elif mins > 0:
        return f"{mins}m"
    else:
        return f"{int(seconds)}s"

# ensure model exists
ensure_model(MODEL)

state, offline_time = load_state()
memory = init_memory()
memory = apply_absence_effect(memory, offline_time)

input_handler = InputHandler(state)
input_handler.start()

print("🐾 Pet is alive...")

if offline_time > 10:
    print(f"\n⏳ You were away for {format_time(offline_time)}...")

    if offline_time > 3600:
        print("Mochi: You were gone for so long… I got lonely… 😢")
    elif offline_time > 300:
        print("Mochi: Oh! You're back! I missed you!")

while True:
    # 1. tick world
    state = tick(state)
    state = clamp(state, STATE_LIMITS)

    # 2. check user input
    user_action = input_handler.get_last_action()

    # 3. agent decision
    prompt = build_prompt(state, memory)
    decision = decide(prompt)

    decision = validate(decision, state)

    # 4. apply agent action
    state = apply_action(state, decision["action"])

    # 5. memory update
    memory = update_memory(memory, decision, user_action)
    save_memory(memory)
    save_state(state)

    # 6. render
    render(state, decision)

    time.sleep(TICK_RATE)