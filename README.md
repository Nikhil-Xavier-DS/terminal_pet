---

# 🐾 Terminal Pet (Local LLM Companion)

A **living, autonomous terminal pet** powered by a local LLM (via Ollama), persistent memory, and an evolving emotional system.

Your pet isn’t just a chatbot—it’s a small simulation that thinks, reacts, remembers, and slowly develops a relationship with you over time.

It runs **fully offline**, lives in your terminal, and doesn’t forget you.

---

## ✨ Features

### 🤖 Local AI Brain

Powered by a local model through Ollama.
No cloud APIs. No tracking. Fully offline intelligence.

---

### ❤️ Emotional System

Your pet has internal emotional state that evolves over time:

* attachment ❤️
* trust 🤝
* neglect 😔

These directly influence behavior, tone, and decisions.

---

### 💾 Persistent Memory

Your pet remembers everything:

* past interactions
* emotional history
* relationship changes

Even after restarts:

> “Oh… you’re back.”

---

### 🔁 Autonomous Simulation

The pet lives on its own timeline:

* hunger increases
* energy decreases
* attention needs grow
* emotional drift over time

It exists even when you’re not interacting.

---

### 🛡 Safe Decision Layer

All LLM outputs are validated before execution:

* prevents impossible actions
* enforces system rules
* keeps simulation consistent

---

## 🗂 Project Structure

```text
terminal-pet/
│
├── main.py
├── config.py
│
├── engine/
│   ├── state.py
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
│
└── data/
    ├── memory.json
    ├── state.json
```

---

## ⚙️ Installation

### 1. Install Python dependencies

```bash
pip install requests
```

---

### 2. Install Ollama

Download and install Ollama:
👉 [https://ollama.ai](https://ollama.ai)

Then pull a model:

```bash
ollama run llama3
```

---

## 🚀 Running the Pet

```bash
python main.py
```

---

## 🧠 How It Works

### 1. Simulation Loop

Each tick updates internal state:

* hunger ⬆️
* energy ⬇️
* emotional drift
* bond changes over time

---

### 2. LLM Decision Making

The model receives:

* current state
* emotional memory
* personality profile

It responds with structured intent:

```json
{
  "action": "play",
  "message": "I want attention...",
  "emotion": "needy"
}
```

---

### 3. Validation Layer

Before execution:

* invalid actions are rejected
* safety rules enforced
* system consistency preserved

---

### 4. Memory System

All interactions are stored:

* emotional events
* behavioral history
* relationship progression

Saved automatically in `/data`.

---

## 🧬 Personality System

Defined in `config.py`:

```python
PERSONALITY = {
  "name": "Mochi",
  "archetype": "clingy chaotic companion",
  "traits": [
    "emotionally reactive",
    "attention-seeking",
    "affectionate when engaged"
  ]
}
```

Your pet’s personality directly shapes how it speaks and reacts.

---

## 💾 Persistence Model

Two layers of memory:

* `data/state.json` → physical + simulation state
* `data/memory.json` → emotional + interaction history

Everything persists across restarts.

---

## 🔁 Example Output

```text
🐾 Pet is alive...

Hunger: 6.2
Energy: 3.1
Bond: 4.8

Mochi: Hey… don’t ignore me too long…
```

---

## 🧪 Design Philosophy

This is not a chatbot.

It is a hybrid system:

> **Simulation engine + emotional model + constrained LLM agent**

* 🧠 LLM = personality + reasoning
* ⚙️ Code = physics + rules + memory
* 💾 Storage = continuity of identity

---

## ⚠️ Notes

* Best with fast local models (e.g. llama3, mistral)
* Ensure Ollama is running before starting
* First run will auto-create `/data`

---

## 🚀 Future Ideas

* multiple interacting pets 🐕🐈
* evolving personality over time
* offline aging system
* ASCII animation mode
* sound / notification reactions
* CLI command system (`feed`, `play`, `talk`)
* installable CLI tool (`pet` command)

---

## 🧡 Credits

Built as an experiment in:

* local LLM agents (Ollama)
* persistent simulated memory
* emotional state systems
* constrained AI behavior design

---

If you want next upgrades, I can help you turn this into something seriously impressive:

* 🔥 CLI tool (`pet run`, `pet feed`, etc.)
* 📦 pip-installable package
* 🧠 better memory architecture (event graph / embeddings)
* 🎮 real “game-like” loop with animations

Just say the direction.
