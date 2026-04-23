import time

from config import STATE_LIMITS

from engine.state import load_state, save_state, tick, clamp
from engine.mood import compute_mood
from engine.offline_sim import simulate_offline

from engine.commands import handle_command

from engine.drives import compute_drives
from engine.goals import choose_goal, resolve_goal
from engine.planner import plan_action
from engine.thoughts import generate_thought

from agent.prompt import build_prompt
from agent.brain import decide, reflect, llm_reason_goal

from memory.memory import (
    init_memory,
    save_memory,
    update_memory,
    evolve_personality,
    add_offline_events,
    compress_memory,
    adapt_personality,
    update_boredom,
    reflect_identity, 
    generate_life_story,
    update_emotion_history, 
    update_personality_arc,
    summarize_memory_llm
)

from ui.input_handler import InputHandler
from ui.render import render


# ---------------------------
# LOAD STATE + MEMORY
# ---------------------------
state, offline_time = load_state()
memory = init_memory()


# ---------------------------
# OFFLINE SIMULATION
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

    # ---------------------------
    # 1. world tick
    # ---------------------------
    state = tick(state)

    # ---------------------------
    # 2. user command
    # ---------------------------
    user_action = input_handler.get_last_action()
    state, user_feedback = handle_command(user_action, state)

    # boredom update
    memory = update_boredom(memory, user_action)

    # ---------------------------
    # 3. drives
    # ---------------------------
    drives = compute_drives(state, memory)

    # ---------------------------
    # 4. goal reasoning via llm
    # ---------------------------
    llm_goal = choose_goal(state, drives)
    rule_goal = llm_reason_goal(state, memory, drives)
    goal = resolve_goal(llm_goal, rule_goal, state)
    state["goal"] = goal

    # ---------------------------
    # 5. plan action
    # ---------------------------
    action = plan_action(state, goal)

    # ---------------------------
    # 6. internal thought
    # ---------------------------
    thought = generate_thought(state, memory, goal)

    # ---------------------------
    # 7. mood
    # ---------------------------
    mood = compute_mood(state, memory)
    state["mood"] = mood

    # ---------------------------
    # 8. LLM (expression only)
    # ---------------------------
    prompt = build_prompt(state, memory, mood, goal, thought, action)
    decision = decide(prompt, action, goal, thought)

    # ---------------------------
    # 9. apply action
    # ---------------------------
    from engine.actions import apply_action
    state = apply_action(state, action)

    reflection = reflect(state, memory, decision)

    if reflection:
        memory["events"].append({
            "text": reflection.get("reflection", ""),
            "importance": 0.7,
            "time": time.time()
        })

    # ---------------------------
    # 10. memory update + learning
    # ---------------------------
    memory = update_memory(memory, decision, user_action)
    memory = adapt_personality(memory)
    memory = evolve_personality(state, memory)
    memory = update_emotion_history(memory)
    memory = update_personality_arc(memory)
    
    # identity reflection (occasionally)
    if int(time.time()) % 20 == 0:
        memory = reflect_identity(memory)

    # ---------------------------
    # 11. memory compression
    # ---------------------------
    memory = compress_memory(memory)

    # ---------------------------
    # 12. clamp state
    # ---------------------------
    state = clamp(state, STATE_LIMITS)

    # ---------------------------
    # 13. persist (IMPORTANT: before render)
    # ---------------------------
    save_state(state)
    save_memory(memory)

    # ---------------------------
    # 14. to see story
    # ---------------------------
    if int(time.time()) % 30 == 0:
        story = generate_life_story(memory)
        print("\n📖 Mochi's Story:", story[:120], "...")

    if int(time.time()) % 60 == 0:
        memory = summarize_memory_llm(memory)
    # ---------------------------
    # 15. render UI
    # ---------------------------
    render(state, decision, user_feedback)

    time.sleep(TICK_RATE)