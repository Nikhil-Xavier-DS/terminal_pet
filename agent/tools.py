from datetime import datetime
from langchain_core.tools import tool


# ---------------------------
# TIME TOOL
# ---------------------------
@tool
def time_tool(_: str = "") -> dict:
    """Returns current system time."""
    return {"time": datetime.now().isoformat()}


# ---------------------------
# MEMORY READ TOOL
# ---------------------------
@tool
def memory_read_tool(data: dict) -> dict:
    """Reads last few memory events."""
    memory = data.get("memory", {})
    return {
        "recent": memory.get("events", [])[-5:]
    }


# ---------------------------
# MEMORY WRITE TOOL
# ---------------------------
@tool
def memory_write_tool(data: dict) -> dict:
    """Writes a new event into memory."""
    memory = data.get("memory", {})
    event = data.get("event")

    if event:
        memory.setdefault("events", []).append(event)

    return {"status": "saved"}


# ---------------------------
# STATE TOOL
# ---------------------------
@tool
def state_tool(data: dict) -> dict:
    """Modifies a state value by delta."""
    state = data.get("state", {})
    key = data.get("key")
    delta = data.get("delta", 0)

    if key:
        state[key] = state.get(key, 0) + delta

    return state