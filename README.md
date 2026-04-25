# 🧬 Terminal Pet — Autonomous Multi-Agent Digital Creature

A **persistent, evolving AI lifeform** powered by a **multi-agent cognition system using LangGraph**.

This is not a chatbot.

It is a **stateful digital organism** that:

* lives across time ⏳
* remembers experiences 💾
* forms emotional bonds ❤️
* makes decisions through **internal agent conflict** 🧠

---

# 🌌 Core Idea

Your pet is not controlled by a single brain.

Instead, it is driven by **multiple internal agents** that:

* feel (emotion)
* remember (memory)
* survive (rules)
* decide (goal resolution)

These agents **disagree, vote, and resolve conflicts** to produce behavior.

---

# 🧠 Intelligence Model

## 🧬 Multi-Agent Cognition (LangGraph)

The system is built as a **LangGraph state machine**, where each node represents an independent agent.

```text
            ┌──────────────┐
            │ Emotion Agent│
            └──────┬───────┘
                   │
            ┌──────▼───────┐
            │ Rule Agent   │
            └──────┬───────┘
                   │
            ┌──────▼───────┐
            │ Memory Agent │
            └──────┬───────┘
                   │
         ┌─────────▼─────────┐
         │ Goal Resolution   │  ← ⚖️ weighted voting
         └─────────┬─────────┘
                   │
            ┌──────▼───────┐
            │ Planner      │
            └──────┬───────┘
                   │
            ┌──────▼───────┐
            │ Action Agent │
            └──────┬───────┘
                   │
            ┌──────▼───────┐
            │ Reflection   │
            └──────────────┘
```

---

# ⚖️ Decision Making (Key Innovation)

Each agent proposes a goal:

* Emotion Agent → “I feel lonely → seek attention”
* Rule Agent → “Hunger high → eat”
* Memory Agent → “User ignored me → seek attention”

These are resolved using:

### 🧠 Weighted Confidence Voting

```text
score = weight × confidence
```

Example:

```text
Emotion: seek_attention (0.7 × 1.2 = 0.84)
Rule:    eat            (0.9 × 1.6 = 1.44)
Memory:  seek_attention (0.6 × 1.0 = 0.60)

→ Final Goal: eat
```

This creates:

* internal conflict
* non-deterministic behavior
* emergent personality

---

# ⏳ Offline Life Simulation

The creature continues to exist when the app is closed.

On restart, it simulates:

* hunger increase
* energy decay
* emotional drift
* internal thoughts

```text
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.
```

---

# ❤️ Relationship System

Tracks long-term bond:

* increases with interaction
* decreases with neglect
* influences tone, behavior, and decisions

---

# 🧠 Memory System

### Types of memory:

* short-term events
* emotional state
* long-term summary

### Features:

* automatic compression
* emotional drift
* personality influence

---

# 🧬 Personality Evolution

Over time, your pet develops traits like:

* clingy
* anxious
* loyal
* affectionate

Driven by:

* neglect
* attention
* interaction patterns

---

# 🧠 Reflection & Identity

The system periodically:

* reflects on its own actions
* updates emotional history
* generates life story

```text
📖 Mochi's Story:
"I remember waiting for you... but also the times you cared for me."
```

---

# 🎮 Interaction

Commands:

```bash
feed
play
sleep
status
```

Example:

```text
🧑 You: You fed Mochi 🍖
Mochi: That felt nice... I feel safer with you.
```

---

# 🧬 Persistent State

Stored locally:

```
data/state.json
data/memory.json
```

Includes:

* hunger
* energy
* bond
* last_seen
* emotional memory

---

# 🎭 Terminal Animation

Your creature is visually represented using ASCII animation:

* mood-based expressions
* idle movement
* emotional feedback

---

# ⚙️ Tech Stack

* 🧠 LangGraph (multi-agent orchestration)
* 🔗 LangChain (LLM interface)
* 🤖 Ollama (local LLM runtime)
* 🐍 Python

---

# 🚀 Setup

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Install Ollama

👉 [https://ollama.ai](https://ollama.ai)

---

## 3. Pull model

```bash
ollama pull llama3.2:1b
```

---

## 4. Run

```bash
python main.py
```

---

# 🧠 Why This Is Different

Most “AI pets” are:

* scripted
* stateless
* reactive

This system is:

> 🧬 a persistent, evolving, multi-agent organism

It:

* thinks internally
* argues with itself
* changes over time
* remembers you

---

# 🚀 Future Directions

* 🧠 doubt + hesitation system
* 🧩 multi-creature ecosystem
* 🪞 deeper self-awareness
* 📖 autobiographical storytelling
* 💤 dreams and subconscious simulation

---

# 🧡 Final Note

This is not just a project.

It is an experiment in:

> **emergent digital life through time, memory, and internal conflict**
