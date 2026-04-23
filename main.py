import time

from config import TICK_RATE, STATE_LIMITS
from engine.state import load_state, save_state, tick, clamp
from engine.actions import apply_action
from engine.validator import validate

from agent.prompt import build_prompt
from agent.brain import decide

from memory.memory import init_memory, update_memory, save_memory
from ui.render import render


state = load_state()
memory = init_memory()

print("🐾 Pet is alive...")

while True:
    # world tick
    state = tick(state)
    state = clamp(state, STATE_LIMITS)

    # LLM decision
    prompt = build_prompt(state, memory)
    decision = decide(prompt)

    # safety layer
    decision = validate(decision, state)

    # apply effects
    state = apply_action(state, decision["action"])

    # memory update + persist
    memory = update_memory(memory, decision)
    save_memory(memory)
    save_state(state)

    # render UI
    render(state, decision)

    time.sleep(TICK_RATE)