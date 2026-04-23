import time

def choose_goal(state, drives):
    current = state.get("goal")

    # ---------------------------
    # CONTINUE EXISTING GOAL
    # ---------------------------
    if current:
        if not is_goal_complete(state, current):
            return current

    # ---------------------------
    # NEW GOAL SELECTION
    # ---------------------------
    if drives["survival"] > 7:
        goal_type = "restore_survival"

    elif drives["fear"] > 6:
        goal_type = "restore_bond"

    elif drives["boredom"] > 6:
        goal_type = "explore"

    else:
        goal_type = "idle"

    return create_goal(goal_type)


# ---------------------------
# GOAL DEFINITIONS
# ---------------------------
def create_goal(goal_type):
    if goal_type == "restore_survival":
        return {
            "type": goal_type,
            "steps": ["eat", "rest"],
            "current_step": 0,
            "created_at": time.time()
        }

    if goal_type == "restore_bond":
        return {
            "type": goal_type,
            "steps": ["seek_attention", "play"],
            "current_step": 0,
            "created_at": time.time()
        }

    if goal_type == "explore":
        return {
            "type": goal_type,
            "steps": ["play", "rest"],
            "current_step": 0,
            "created_at": time.time()
        }

    return {
        "type": "idle",
        "steps": ["do_nothing"],
        "current_step": 0,
        "created_at": time.time()
    }


# ---------------------------
# STEP HANDLING
# ---------------------------
def get_current_step(goal):
    if "steps" not in goal:
        # convert old goal into new format
        action = goal.get("type", "do_nothing")

        goal["steps"] = [action]
        goal["current_step"] = 0

    return goal["steps"][goal["current_step"]]


def advance_goal(goal):
    if "steps" not in goal:
        return goal

    if goal["current_step"] < len(goal["steps"]) - 1:
        goal["current_step"] += 1

    return goal


def is_goal_complete(state, goal):
    if "type" not in goal:
        return True

    if goal["type"] == "restore_survival":
        return state["hunger"] < 4 and state["energy"] > 5

    if goal["type"] == "restore_bond":
        return state["bond"] > 6

    if goal["type"] == "explore":
        return False

    return False