from agent.multi_agents import (
    emotion_agent,
    goal_agent,
    planner_agent,
    action_agent,
    reflection_agent
)


def run_multi_agent(state, memory):
    # 1. emotion perception
    emotion = emotion_agent(state, memory)

    # 2. goal selection
    goal = goal_agent(state, memory, emotion)

    # 3. planning
    plan = planner_agent(goal)

    # 4. action execution
    action_data = action_agent(state, goal, emotion)

    # 5. reflection
    reflection = reflection_agent(action_data["message"])

    return {
        "emotion": emotion,
        "goal": goal,
        "plan": plan,
        "action": action_data["action"],
        "message": action_data["message"],
        "reflection": reflection
    }