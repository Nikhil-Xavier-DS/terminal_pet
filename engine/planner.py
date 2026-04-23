from engine.goals import get_current_step, advance_goal

def plan_action(state, goal):
    action = get_current_step(goal)

    # after action, move to next step
    goal = advance_goal(goal)

    return action