from ui.animation import get_frame


def render(state, decision, user_action=None):
    print("\n" + "=" * 40)

    # 🐾 VISUAL (Creature)
    frame = get_frame(state)
    if frame:
        print(frame)

    # ---------------------------
    # 📊 STATE
    # ---------------------------
    print("\n📊 STATE")
    print(f"Hunger : {state.get('hunger', 0):.1f}")
    print(f"Energy : {state.get('energy', 0):.1f}")
    print(f"Bond   : {state.get('bond', 0):.1f}")
    print(f"Mood   : {state.get('mood', 'calm')}")

    # ---------------------------
    # 🧠 INTERNAL DECISION
    # ---------------------------
    print("\n🧠 INTERNAL STATE")
    print(f"Emotion : {decision.get('emotion', '')}")
    print(f"Goal    : {decision.get('goal', '')}")
    print(f"Action  : {decision.get('action', '')}")

    # ---------------------------
    # ⚖️ INTERNAL DEBATE (SAFE)
    # ---------------------------
    debug = decision.get("decision_debug", {})
    details = debug.get("details", [])

    if details:
        print("\n⚖️ Internal Debate:")
        for line in details:
            print("  -", line)

    # ---------------------------
    # 🧑 USER ACTION
    # ---------------------------
    if user_action:
        print(f"\n🧑 You: {user_action}")

    # ---------------------------
    # 💬 EXPRESSION
    # ---------------------------
    message = decision.get("message", "...")
    print("\n💬 Mochi:")
    print(message)

    print("\n" + "=" * 40)