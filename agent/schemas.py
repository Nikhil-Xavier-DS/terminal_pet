from pydantic import BaseModel
from typing import Literal, Optional


# ---------------------------
# CORE LLM OUTPUT
# ---------------------------
class AgentDecision(BaseModel):
    goal: Literal[
        "eat",
        "sleep",
        "play",
        "seek_attention",
        "explore",
        "rest",
        "do_nothing"
    ]

    action: Literal[
        "eat",
        "sleep",
        "play",
        "seek_attention",
        "do_nothing"
    ]

    message: str
    emotion: str
    reflection: Optional[str] = None


# ---------------------------
# MEMORY EVENT STRUCTURE
# ---------------------------
class MemoryEvent(BaseModel):
    text: str
    importance: float = 0.5
    time: float


# ---------------------------
# GRAPH STATE (LangGraph SAFE)
# ---------------------------
class GraphState(BaseModel):
    state: dict
    memory: dict
    mood: str

    goal: Optional[str] = None
    plan: Optional[str] = None
    action: Optional[str] = None
    message: Optional[str] = None
    reflection: Optional[str] = None