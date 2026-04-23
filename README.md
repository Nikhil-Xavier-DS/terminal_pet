# 🐾 Terminal Pet (Local LLM Agent)

A **living terminal-based virtual pet** powered by a local LLM (via Ollama), persistent memory, emotional state, and autonomous behavior.

Your pet:
- remembers you across restarts 💾  
- develops emotional attachment ❤️  
- acts autonomously 🔁  
- responds with personality 🎭  
- runs fully offline 🏠  

---

# 🧠 Features

## 🤖 Local AI Brain
Uses a local model via Ollama to make decisions.

## ❤️ Emotional System
Tracks:
- attachment
- neglect
- trust

These directly influence behavior.

## 💾 Persistent Memory
- Pet remembers past interactions
- State and memory survive program restarts

## 🔁 Autonomy
Pet acts continuously even without input:
- gets hungry
- loses energy
- seeks attention

## 🛡 Safe Decision Layer
All LLM outputs are validated before execution.

---

# 🗂 Project Structure

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
⚙️ Requirements
1. Install Python deps
pip install requests
2. Install Ollama
Install and run a local model:
👉 https://ollama.ai
Example:
ollama run llama3

🚀 How to Run
python main.py

🧠 How It Works
1. State Loop

Every tick:
* hunger increases
* energy decreases
* bond changes over time
2. LLM Decision

The model receives:
* current state
* emotional memory
* personality profile
It returns:
{
  "action": "play",
  "message": "I want attention...",
  "emotion": "needy"
}
3. Validation Layer

Ensures:
* pet cannot do impossible actions
* survival rules are enforced
4. Memory System

Stores:
* emotional history
* interaction events
Saved automatically to disk.

❤️ Personality System
Defined in config.py:
PERSONALITY = {
  "name": "Mochi",
  "archetype": "clingy chaotic companion",
  "traits": [
    "emotionally reactive",
    "attention-seeking",
    "affectionate when engaged"
  ]
}

💾 Persistence
Your pet remembers everything via:
* data/state.json → physical state
* data/memory.json → emotional history
Even after restart:
“Oh… you’re back.”

🔁 Example Behavior
🐾 Pet is alive...

Hunger: 6.2
Energy: 3.1
Bond: 4.8

Mochi: Hey… don’t ignore me too long…

🧪 Design Philosophy
This is NOT just a chatbot.
It is:
A constrained simulation + emotional memory + LLM personality engine
* LLM = personality + reasoning
* Code = rules + physics + memory

⚠️ Notes
* Works best with small/fast models (llama3, mistral)
* Always run Ollama before starting
* First run will create /data automatically

🚀 Future Ideas
* multiple pets interacting
* personality evolution over time
* idle behavior while app is closed (simulated aging)
* ASCII animation system
* sound + notification reactions

🧡 Credits
Built as a local autonomous agent experiment using:
* Ollama local LLM runtime
* Python simulation engine
* rule-based agent architecture
---

If you want next, I can also:
- add a **CLI command system (feed/play/talk while running)**  
- or turn this into a **pip-installable package with entry command `pet`**
