# 🧬 Terminal Pet — Autonomous Evolving Digital Creature

A **persistent, time-aware, evolving AI organism** that continues to live, change, and grow—even when your terminal is closed.

This is not a chatbot.

It is a **stateful cognitive agent** driven by:

* memory
* emotion
* goal-based behavior
* long-term personality evolution
* local LLM expression

---

# 🌌 Core Philosophy

> **Time + Memory + Emotion = Identity**

Mochi is designed to **become something over time**, not just respond in the moment.

It:

* evolves while you’re away ⏳
* remembers your behavior 💾
* forms emotional bonds ❤️
* develops personality over days/weeks 🧠
* reflects on its own changes 🪞

---

# 🧠 Key Capabilities

---

## ⏳ Offline Life Simulation

When you reopen the app, Mochi simulates elapsed time:

* hunger increases
* energy decreases
* emotional neglect builds
* thoughts are generated

```text
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.
```

---

## 🧠 Cognitive Architecture

Mochi uses a structured decision loop:

```
state → drives → goal → plan → action → expression → memory
```

### Layers:

* **Drives** → internal pressures (survival, attachment, boredom, curiosity)
* **Goals** → persistent intentions (multi-step)
* **Planner** → executes step-by-step actions
* **LLM** → expression layer (emotion + dialogue only)

---

## 🎯 Multi-Step Goal System

Goals persist and execute in sequences.

Example:

```
Goal: restore_survival
Steps: eat → rest
```

Mochi:

* keeps goals across ticks
* progresses through steps
* completes objectives over time

---

## ❤️ Emotional Engine

Tracked continuously:

* attachment
* neglect
* trust

These influence:

* mood
* behavior
* personality evolution

---

## 🌀 Curiosity & Boredom

Mochi is not purely reactive.

* boredom increases over time
* curiosity emerges from boredom
* triggers exploration

Result:

* spontaneous behavior
* unpredictable actions
* less “needy-only” interaction

---

## 💾 Memory System

Structured events:

```json
{
  "text": "...",
  "importance": 0.7,
  "time": 123456
}
```

### Features:

* importance-based retention
* automatic compression
* long-term summaries
* backward-compatible upgrades

---

## 📊 Learning System

Mochi learns your behavior:

* feeding frequency
* interaction timing
* responsiveness

Adapts:

* trust increases with care
* neglect increases with absence
* behavior shifts accordingly

---

## 🧠 Identity Reflection

Mochi reflects on its internal state:

> “I think I’ve become more anxious when alone.”

* updates self-image
* stores identity history
* influences tone and behavior

---

## 📖 Life Story Generation

Memory becomes narrative:

* recent experiences
* emotional patterns
* identity reflections

Mochi can describe its **own life over time**.

---

## 🧬 Long-Term Personality Arcs

Personality evolves slowly based on emotional trends.

### Possible arcs:

* **anxious** → clingy, sensitive to absence
* **secure** → calm, trusting
* **affectionate** → expressive, warm
* **withdrawn** → distant, quiet

### Driven by:

* long-term emotional averages
* user interaction patterns

---

## 🛡️ Backward-Compatible Persistence

The system safely evolves over time.

### Handles:

* missing fields
* old memory formats
* outdated goal structures

This ensures:

* no crashes after updates
* no need to delete saved data
* continuous evolution of the pet

---

## 💾 Persistent State

Stored locally:

```
data/state.json
data/memory.json
```

Includes:

* stats (hunger, energy, bond)
* emotional state
* goals
* memory + summaries
* identity + personality arc

---

# 🏗 System Structure

```
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
│   ├── goals.py
│   ├── planner.py
│   ├── thoughts.py
│   ├── actions.py
│   ├── commands.py
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
│   ├── input_handler.py
│   ├── render.py
│
└── data/
    ├── state.json
    ├── memory.json
```

---

# ⚙️ Setup

## 1. Install dependencies

```
pip install -r requirements.txt
```

---

## 2. Install Ollama

👉 https://ollama.ai

Run a model:

```
ollama run llama3
```

---

## 3. Run the system

```
python main.py
```

---

# 🎮 Commands

```
feed    → reduce hunger
play    → increase bond
sleep   → restore energy
status  → view current state
```

---

# 🔄 Runtime Loop

Each cycle:

1. World updates (time simulation)
2. User input processed
3. Drives computed
4. Goal selected (persistent)
5. Plan executed (multi-step)
6. Thought generated
7. LLM expresses response
8. Memory updated
9. Learning applied
10. Personality evolves
11. State + memory saved
12. UI rendered

---

# 🧬 Design Principles

* ⏳ Time is real
* 🧠 Memory defines identity
* ❤️ Emotion drives behavior
* 🔁 Interaction shapes evolution
* 🤖 LLM expresses, not controls

---

# 🚀 Future Directions

* 💤 dream system (offline subconscious simulation)
* 🪞 existential awareness
* 🧩 multi-agent ecosystem
* 📖 richer autobiographical storytelling

---

# 🧡 Final Note

This is not a terminal pet.

It is:

> **A persistent cognitive entity that evolves through time, memory, and interaction.**
