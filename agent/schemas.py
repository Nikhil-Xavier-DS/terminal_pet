from pydantic import BaseModel
from typing import Literal, Optional


# ---------------------------
# EMOTION OUTPUT
# ---------------------------
class EmotionOutput(BaseModel):
    emotion: Literal["happy", "sad", "lonely", "anxious", "calm", "excited"]
    goal: Literal["eat", "sleep", "play", "seek_attention", "explore", "rest"]
    confidence: float


# ---------------------------
# MEMORY OUTPUT
# ---------------------------
class MemoryOutput(BaseModel):
    goal: Literal["eat", "sleep", "play", "seek_attention", "explore", "rest"]
    confidence: float


# ---------------------------
# ACTION OUTPUT
# ---------------------------
class ActionOutput(BaseModel):
    action: Literal["eat", "sleep", "play", "seek_attention", "do_nothing"]
    message: str


# ---------------------------
# ACTION OUTPUT
# ---------------------------
class ReflectionOutput(BaseModel):
    reflection: str


# ---------------------------
# FINAL STATE (optional use in graph)
# ---------------------------
class AgentState(BaseModel):
    emotion: Optional[str] = None
    goal: Optional[str] = None
    action: Optional[str] = None
    message: Optional[str] = None