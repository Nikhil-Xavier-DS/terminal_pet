# 🐾 Terminal Pet (LangGraph Multi-Agent System)

A **living virtual pet system** built using **LangGraph + LangChain + local LLMs (LM Studio / Ollama compatible)**.

The pet is powered by a **multi-agent architecture** where different reasoning systems vote on behavior, and a ReAct executor performs actions using tools.

---

# 🧠 Architecture Overview

The system is designed as a **production-style agent graph**:

```

Emotion Agent   ─┐
Rule Agent      ─┼──► Planner ─► Resolver (Weighted Voting)
Memory Agent    ─┤
Planner Agent   ─┘

```
                    ↓
            🎯 Final Goal

                    ↓
        🤖 ReAct Execution Agent
                    ↓
            🛠 ToolNode (tools)
```

````

---

# ⚙️ Key Features

## 🧠 Multi-Agent Reasoning
- Emotion Agent → behavioral intuition
- Rule Agent → deterministic survival logic
- Memory Agent → past experience influence
- Planner Agent → synthesis of all signals

## ⚖️ Weighted Voting System
Each agent contributes to final decision:

- Rule Agent (highest priority)
- Emotion Agent (adaptive behavior)
- Memory Agent (experience-driven)
- Planner Agent (LLM synthesis)

---

## 🤖 ReAct Execution Layer
Final decisions are executed using a **ReAct agent**:
- Can use tools dynamically
- Executes actions step-by-step
- Safe isolated execution layer

---

## 🛠 Tool System
Supports LangChain tools such as:
- memory_read
- memory_write
- state update tools
- custom environment actions

All tools are executed via `ToolNode`.

---

## 🧠 Memory System
- Stores events and personality evolution
- Trimmed automatically for context safety
- Used by Memory Agent for decision-making

---

## 🧩 LangGraph Flow
- Fully compiled graph
- Deterministic execution pipeline
- Safe tool routing loop

---

# 📦 Tech Stack

- LangGraph
- LangChain
- ChatOpenAI (LM Studio / OpenAI-compatible local server)
- Python 3.10+
- Pydantic (for structured outputs – optional extension)

---

# 🚀 Getting Started

## 1. Install dependencies

```bash
pip install langgraph langchain langchain-openai
````

If using LM Studio:

```bash
pip install openai
```

---

## 2. Start local LLM (LM Studio)

Run server:

```
http://127.0.0.1:1234/v1
```

Model example:

* `local-model`
* or any OpenAI-compatible model

---

## 3. Run the app

```bash
python main.py
```

---

# 🧠 How It Works

## Step 1 — State Input

Pet receives:

* hunger
* energy
* mood
* memory

---

## Step 2 — Multi-Agent Reasoning

Each agent proposes a goal:

| Agent   | Output                |
| ------- | --------------------- |
| Emotion | instinctive goal      |
| Rule    | survival-driven goal  |
| Memory  | experience-based goal |
| Planner | synthesized goal      |

---

## Step 3 — Weighted Resolution

Final goal is computed using:

```
score = confidence × agent_weight
```

---

## Step 4 — Execution (ReAct)

The final goal is passed to a ReAct agent which:

* decides actions
* optionally uses tools
* executes behavior

---

# 🧪 Example Behavior

```
Emotion: play (0.6)
Rule: eat (0.9)
Memory: sleep (0.4)
Planner: play (0.7)

→ Final Goal: eat

Action: search_food
Message: "I'm hungry... finding food!"
```

---

# 🛠 Project Structure

```
terminal_pet/
│
├── agent/
│   ├── multi_agent_graph.py   # LangGraph system
│   ├── tool_registry.py       # Tool definitions
│
├── engine/
│   ├── state.py
│   ├── mood.py
│   ├── actions.py
│
├── memory/
│   ├── memory.py
│
├── ui/
│   ├── render.py
│
├── main.py
```

---

# 🔥 Why This Architecture Works

### ✔ Separation of concerns

Each agent has a single responsibility

### ✔ Stability

No tool logic inside reasoning nodes

### ✔ Scalability

Easy to add:

* new agents
* new tools
* new voting rules

### ✔ Production-safe LangGraph design

No circular state corruption or invalid updates

---

# 🚧 Future Upgrades

Planned enhancements:

* 🧬 Long-term vector memory (RAG)
* 🤝 Agent debate system (multi-agent argumentation)
* 🧠 Self-reflection loops
* 🧾 Structured Pydantic outputs everywhere
* 🌐 MCP (Model Context Protocol) integration
* 🎭 Personality evolution engine

---

# 🐾 Philosophy

This is not just a chatbot.

It is a **stateful, evolving agent ecosystem** that behaves like a living digital creature.

---

# 🧑‍💻 Author Notes

Built as an experimental system combining:

* agent orchestration (LangGraph)
* tool-using reasoning (ReAct)
* behavioral simulation (pet system)