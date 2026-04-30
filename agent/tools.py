from datetime import datetime
from langchain_core.tools import tool


@tool
def get_time() -> str:
    """Get current system time."""
    return datetime.now().isoformat()


@tool
def read_memory(memory: str = "") -> str:
    """Read last memory snapshot."""
    return f"memory accessed: {memory[-200:]}"


@tool
def update_state(info: str) -> str:
    """Apply a state update."""
    return f"state updated with: {info}"