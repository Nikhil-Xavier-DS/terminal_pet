def render(state, decision):
    print("\n🐾 --- PET ---")
    print(f"Hunger: {state['hunger']:.1f}")
    print(f"Energy: {state['energy']:.1f}")
    print(f"Bond:   {state['bond']:.1f}")
    print("\nMochi: " + decision.get("message", ""))