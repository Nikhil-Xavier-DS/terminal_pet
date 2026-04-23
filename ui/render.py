from ui.animation import get_frame


def render(state, decision, user_action=None):
    frame = get_frame(state)

    print("\n" + "=" * 40)

    # 🐰 Mochi (visual layer)
    print(frame)

    # 📊 STATE
    print("\n📊 STATE")
    print(f"Hunger : {state['hunger']:.1f}")
    print(f"Energy : {state['energy']:.1f}")
    print(f"Bond   : {state['bond']:.1f}")
    print(f"Mood   : {state.get('mood', 'calm')}")

    # 🧠 LLM OUTPUT
    print("\n🧠 Mochi Thoughts")
    print(decision.get("message", ""))

    print(f"\n🎯 Goal: {decision.get('goal', '')}")

    # 🧑 USER ACTION
    if user_action:
        print(f"\n🧑 You: {user_action}")

    print("=" * 40)