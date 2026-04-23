def render(state, decision, user_action=None):
    print("\n🐾 --- PET ---")
    print(f"Hunger: {state['hunger']:.1f}")
    print(f"Energy: {state['energy']:.1f}")
    print(f"Bond:   {state['bond']:.1f}")

    print(f"\n💭 Emotion: {decision.get('emotion')}")
    print(f"🎯 Goal: {decision.get('goal')}")

    if user_action:
        print(f"\n🧑 You: {user_action}")

    # make message always safe
    message = decision.get("message") or "..."

    print("\nMochi: " + str(message))