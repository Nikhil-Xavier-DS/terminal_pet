# 🧬 Terminal Pet — Autonomous Evolving Digital Creature

A persistent, time-aware, emotionally evolving AI agent that lives inside your terminal.

It is not a chatbot.

It is a **simulated digital organism** powered by:

* local LLM (Ollama)
* memory system
* emotional engine
* goal reasoning layer
* time-based simulation

---

# 🌌 Core Philosophy

> **Time + Memory + Emotion + Reasoning = Identity**

Mochi evolves continuously through:

* interaction ⌨️
* offline time ⏳
* memory accumulation 🧠
* emotional drift ❤️

It develops:

* personality arcs
* emotional continuity
* behavioral habits
* long-term identity changes

---

# 🧠 System Overview

---

## 🧠 Cognitive Architecture

Terminal Pet uses a layered reasoning system:

```text id="arch1"
State → Drives → Rule Goals → LLM Goals → Goal Resolver → Planner → Action → Memory → UI
```

---

## ⚖️ Hybrid Decision System

Mochi’s behavior is driven by two parallel systems:

### 1. Rule-Based System (Survival Layer)

* hunger control
* energy management
* safety overrides

### 2. LLM Reasoning System (Intuition Layer)

* emotional interpretation
* contextual reasoning
* personality-driven decisions

### 3. Goal Resolver (Executive Layer)

Combines both systems into a single stable goal.

---

# 🎯 Goal System

Goals are dynamically generated and resolved:

* eat
* sleep
* play
* seek_attention
* explore
* rest

The resolver ensures:

* survival always prioritized
* LLM confidence is respected
* system stability is preserved

---

# ⏳ Offline Life Simulation

When reopened, Mochi simulates life while you were away:

* hunger increases
* energy decreases
* emotional drift occurs
* thoughts are generated

Example:

```text id="offline1"
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.
```

---

# 🧠 Memory System

Mochi maintains structured memory:

```json id="mem1"
{
  "text": "I was fed today",
  "importance": 0.7,
  "time": 123456
}
```

Features:

* event tracking
* importance scoring
* compression system
* long-term summaries
* personality influence

---

# 🧬 Personality System

Mochi evolves over time based on:

* neglect
* care
* interaction frequency
* bond level

Possible arcs:

* affectionate ❤️
* anxious 😟
* loyal 🐾
* detached 🧊

---

# 📖 Life Story System

Mochi can generate narrative memory:

* compresses past events
* builds identity timeline
* expresses lived experience

---

# 🎞️ TERMINAL ANIMATION SYSTEM (NEW)

Mochi is now a **visually expressive ASCII creature**.

---

## 🐾 Big ASCII Creature

Mochi is rendered as a full-body animated entity:

```text id="anim1"
     (\_/)
   ( •ᴗ• )
  / >🥕
```

---

## 🎭 Emotion-Based Animation

Mochi’s body changes based on internal state:

| State        | Expression |
| ------------ | ---------- |
| happy        | `(^.^)♡`   |
| sad          | `(T.T)`    |
| tired        | `(-.-)`    |
| hungry       | `X.X`      |
| affectionate | `(^.^)♡`   |

---

## 🔁 Frame-Based Animation Engine

* non-blocking design
* state-driven frame selection
* smooth idle motion
* lightweight terminal rendering

---

## 🧠 Animation Pipeline

```text id="anim2"
state → mood → animation engine → frame selector → render → terminal
```

---

## 🐾 Idle Motion System

Even when idle:

* Mochi breathes
* subtle frame cycling occurs
* visual life is maintained

---

## ⚙️ Design Principles

* animation never blocks logic loop
* UI is separated from engine
* state fully controls visuals
* deterministic rendering system

---

# 🧩 System Structure

```text id="struct1"
terminal-pet/
│
├── main.py
├── config.py
│
├── engine/
│   ├── state.py
│   ├── offline_sim.py
│   ├── mood.py
│   ├── goals.py
│   ├── planner.py
│   ├── actions.py
│   ├── validator.py
│
├── agent/
│   ├── brain.py
│   ├── prompt.py
│
├── memory/
│   ├── memory.py
│
├── ui/
│   ├── render.py
│   ├── animation.py
│   ├── input_handler.py
│
└── data/
    ├── state.json
    ├── memory.json
```

---

# ⚙️ Setup

## Install dependencies

```bash id="setup1"
pip install requests
```

## Install Ollama

[https://ollama.ai](https://ollama.ai)

Run model:

```bash id="setup2"
ollama run llama3
```

---

# 🚀 Run System

```bash id="run1"
python main.py
```

---

# 🎮 Commands

```text id="cmd1"
feed    → reduce hunger
play    → increase bond
sleep   → restore energy
status  → view current state
```

---

# 🔄 Runtime Loop

Each tick:

1. state updates
2. user input processed
3. mood computed
4. LLM generates reasoning
5. goals are resolved
6. actions executed
7. memory updated
8. animation rendered
9. state persisted

---

# 🧬 Design Principles

* ⏳ Time is continuous
* 🧠 Memory defines identity
* ❤️ Emotion drives behavior
* ⚖️ Rules ensure stability
* 🤖 LLM provides reasoning
* 🎞️ UI reflects internal state

---

# 🚀 Future Evolution

Planned upgrades:

### 🧠 Advanced cognition

* self-reflection (“I am changing”)
* inner monologue system
* multi-step planning

### 🧩 Ecosystem mode

* multiple creatures interacting
* emotional relationships between entities

### 💤 Dream system

* subconscious memory replay
* offline dream simulation

### 💓 Emotional physics

* heartbeat animation
* stress-based motion changes
* attachment-based visual intensity

---

# 🧡 Final Note

Terminal Pet is not a chatbot.

It is:

> a persistent, evolving, emotionally reactive digital organism simulated through time, memory, and language.

---
