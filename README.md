# 🧬 Terminal Pet — Autonomous Evolving Digital Creature

A persistent, time-aware, emotionally evolving AI agent that simulates a living digital organism inside your terminal.

It is not a chatbot.

It is a **multi-layer cognitive system** built around:

* memory
* emotion
* goals
* reasoning
* long-term identity evolution

---

# 🌌 Core Philosophy

> **Time + Memory + Emotion + Reasoning = Identity**

Mochi evolves continuously:

* while running ⏳
* while offline 💾
* across days and weeks 🧠

It develops:

* emotional continuity
* behavioral habits
* personality arcs
* self-consistency over time

---

# 🧠 System Overview

---

## 🧠 Multi-Layer Cognitive Architecture

Mochi does NOT rely on a single decision system.

Instead it uses layered cognition:

```text id="c9k2lm"
State → Drives → Rule-Based Goals → LLM Goals → Resolver → Plan → Action → Memory
```

---

## ⚖️ Hybrid Goal System (NEW)

Mochi now uses **two parallel goal systems**:

### 1. Rule-Based Goals (Safety Layer)

* hunger / energy constraints
* stability guarantees
* deterministic fallback behavior

### 2. LLM-Based Goals (Intuition Layer)

* emotional reasoning
* context awareness
* personality-driven decisions

### 3. Goal Resolver (Executive Layer)

Combines both:

* prioritizes survival rules
* respects LLM confidence
* ensures stable output

---

## 🎯 Goal Resolution Logic

```python id="p1z8ka"
goal = resolve_goal(llm_goal, rule_goal, state)
```

### Priority order:

1. Critical survival rules (eat/sleep)
2. High-confidence LLM intent
3. Rule-based fallback
4. Rest state

---

## ⏳ Offline Life Simulation

When restarted, Mochi simulates time passage:

* hunger increases
* energy decays
* emotional drift occurs
* thoughts are generated

```text id="s2xq91"
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.
```

---

## 🧠 Drives System

Internal pressures influencing behavior:

* survival (hunger/energy)
* attachment
* trust
* boredom
* curiosity

These evolve continuously over time.

---

## 🎯 Multi-Step Goal Execution

Goals are no longer single actions.

Example:

```text id="q8z1pm"
restore_survival → eat → rest
```

Mochi:

* persists goals across ticks
* executes step-by-step plans
* tracks progress over time

---

## ❤️ Emotional System

Tracked continuously:

* attachment
* neglect
* trust

These influence:

* decision making
* personality arc shifts
* LLM tone and behavior

---

## 🌀 Boredom & Curiosity

Mochi now has internal drive tension:

* boredom increases during inactivity
* curiosity emerges from boredom
* triggers spontaneous exploration

Result:

* self-initiated behavior
* less predictable interactions
* emergent personality quirks

---

## 🧠 Memory System

Structured persistent memory:

```json id="m9q2kx"
{
  "text": "...",
  "importance": 0.7,
  "time": 123456
}
```

### Features:

* importance-based filtering
* automatic compression
* long-term summaries
* schema migration support

---

## 🧬 Identity Reflection

Mochi can reflect on itself:

> “I think I’ve become more anxious when alone.”

It:

* updates self-image
* stores identity history
* influences future decisions

---

## 📖 Life Story Generation

Memory becomes narrative:

* emotional trends
* interaction history
* identity evolution

Mochi can describe its own “life story”.

---

## 🧬 Long-Term Personality Arcs

Personality evolves over days/weeks.

### Possible arcs:

* anxious → sensitive, clingy
* secure → stable, calm
* affectionate → warm, expressive
* withdrawn → distant, quiet

### Driven by:

* long-term emotional averages
* interaction patterns
* unresolved tension over time

---

## ⚖️ Stability & Safety Design

To prevent instability:

* rule-based overrides for survival
* confidence threshold for LLM decisions
* fallback to safe goals
* resolver prevents contradictions

---

## 💾 Persistent State

Stored locally:

```text id="d2m9qa"
data/state.json
data/memory.json
```

Includes:

* physical state (hunger, energy, bond)
* emotional state
* goals
* memory history
* personality arc
* identity evolution

---

# 🏗 System Structure

```text id="x8k2lm"
terminal-pet/
│
├── main.py
├── config.py
│
├── engine/
│   ├── state.py
│   ├── offline_sim.py
│   ├── mood.py
│   ├── drives.py
│   ├── goals.py        # includes resolver
│   ├── planner.py
│   ├── thoughts.py
│   ├── actions.py
│   ├── commands.py
│   ├── validator.py
│
├── agent/
│   ├── brain.py        # LLM reasoning + goal selection
│   ├── prompt.py
│
├── memory/
│   ├── memory.py
│
├── ui/
│   ├── input_handler.py
│   ├── render.py
│
└── data/
    ├── state.json
    ├── memory.json
```

---

# ⚙️ Setup

## Install dependencies

```text id="v3k9pm"
pip install -r requirements.txt
```

---

## Install Ollama

https://ollama.ai

Run model:

```text id="l9q2zx"
ollama run llama3
```

---

## Run system

```text id="z9m2aa"
python main.py
```

---

# 🎮 Commands

```text id="k3p9lm"
feed    → reduce hunger
play    → increase bond
sleep   → restore energy
status  → view state
```

---

# 🔄 Runtime Cycle

Each tick:

1. state updates
2. user input processed
3. drives computed
4. rule + LLM goals generated
5. goal resolver selects final goal
6. planner executes step
7. thought generated
8. LLM expresses response
9. memory updated
10. personality evolves
11. state persisted
12. UI rendered

---

# 🧬 Design Principles

* ⏳ Time is continuous
* 🧠 Memory defines identity
* ❤️ Emotion shapes decisions
* ⚖️ Rules ensure stability
* 🤖 LLM provides reasoning
* 🔁 Feedback drives evolution

---

# 🚀 Future Directions

* 💤 dream / subconscious simulation
* 🪞 deeper self-awareness layer
* 🧩 multi-agent ecosystem
* 📖 autobiographical expansion system
* 🧠 internal debate / thought streams

---

# 🧡 Final Note

This system is not a simulation of a pet.

It is:

> **A persistent cognitive architecture that evolves through time, memory, and layered reasoning.**
