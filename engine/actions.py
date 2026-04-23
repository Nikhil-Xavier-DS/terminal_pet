ACTIONS = {
    "eat": {"hunger": -3, "energy": +1},
    "sleep": {"energy": +4},
    "play": {"energy": -2, "bond": +1},
    "seek_attention": {"bond": +2},
    "do_nothing": {}
}

def apply_action(state, action):
    # safety: ensure string
    if not isinstance(action, str):
        action = "do_nothing"

    effects = ACTIONS.get(action, {})

    for k, v in effects.items():
        state[k] = state.get(k, 0) + v

    return state