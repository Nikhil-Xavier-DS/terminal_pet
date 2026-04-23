def handle_command(command, state):
    if not command:
        return state, None

    if command == "feed":
        state["hunger"] = max(0, state["hunger"] - 5)
        return state, "You fed Mochi 🍖"

    elif command == "play":
        if state["energy"] > 2:
            state["energy"] -= 2
            state["bond"] += 1
            return state, "You played with Mochi 🎾"
        else:
            return state, "Mochi is too tired 😴"

    elif command == "sleep":
        state["energy"] += 4
        return state, "Mochi went to sleep 💤"

    elif command == "status":
        msg = (
            f"Status → Hunger: {state['hunger']:.1f}, "
            f"Energy: {state['energy']:.1f}, "
            f"Bond: {state['bond']:.1f}"
        )
        return state, msg

    else:
        return state, f"Unknown command: {command}"