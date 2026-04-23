# 🐾 Terminal Pet (Living Local LLM Agent)

A **persistent, time-aware virtual pet** that lives in your terminal.

It:
- remembers you across restarts 💾  
- reacts when you’ve been away ⏳  
- evolves emotionally ❤️  
- responds to your commands ⌨️  
- acts autonomously using a local LLM 🤖  

Powered by a local model via Ollama.

---

# 🌟 Key Features

## 🧠 1. Local AI Brain
Uses a local LLM (via Ollama) for personality-driven responses.

## ❤️ 2. Emotional System
Tracks:
- attachment
- neglect
- trust

These evolve over time and usage.

---

## ⏳ 3. Offline Simulation (NEW)
Your pet continues to “live” while the program is closed:

- hunger increases over time
- energy decreases over time
- emotional changes based on absence

When you return:

> “You were gone for a while… I missed you.”

---

## 🕓 4. Last Seen Tracking (NEW)

Stores the last time you interacted:

```json
"last_seen": 1713870000
Used to calculate absence duration.

⌨️ 5. Interactive Commands
You can directly interact:
> feed
> play
> sleep
> status
Each command gives instant feedback:
* 🧑 You: You fed Mochi 🍖
* 🧑 You: Mochi went to sleep 💤

💾 6. Persistent Memory
Your pet remembers everything:
* state (hunger, energy, bond)
* emotional history
* past interactions
Stored in:
data/state.json
data/memory.json

🗂 Project Structure
terminal-pet/
│
├── main.py
├── config.py
│
├── engine/
│   ├── state.py        # simulation + offline logic
│   ├── actions.py      # pet actions
│   ├── validator.py    # safety rules
│   ├── commands.py     # user commands
│
├── agent/
│   ├── brain.py        # LLM decision engine
│   ├── prompt.py       # context builder
│   ├── ollama_utils.py # model + runtime checks
│
├── memory/
│   ├── memory.py       # emotional memory system
│
├── ui/
│   ├── input_handler.py
│   ├── render.py
│
└── data/
    ├── state.json
    ├── memory.json

⚙️ Requirements
Install Python dependency
pip install requests
Install Ollama
Download and install:
👉 https://ollama.ai
Run a model:
ollama run llama3

🚀 How to Run
python main.py

🧠 How It Works
1. Time Simulation
Each tick:
* hunger increases
* energy decreases
2. Offline Simulation
When restarted:
* time difference is calculated
* state is updated automatically
3. Command System
User input is processed immediately:
* affects state instantly
* triggers visible feedback
4. LLM Decision
The model receives:
* current state
* emotional memory
* personality profile
Returns:
{
  "action": "play",
  "message": "I feel playful...",
  "emotion": "happy"
}

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

🧪 Example Behavior
After 10 minutes away:
⏳ You were away for 10m...

Mochi: Oh! You're back! I missed you!
After feeding:
> feed

🧑 You: You fed Mochi 🍖
Mochi: mmm… that feels better

⚠️ Notes
* Works best with llama3 or mistral models
* Ollama must be running in background
* First run may download model automatically

🧠 Design Philosophy
This is not just a chatbot.
It is:
A persistent simulation agent with emotional memory + time awareness
* LLM = personality
* Code = world rules
* Memory = identity
* Time = life

🚀 Future Ideas
* 🧬 personality evolution over time
* 🎭 mood system (sad/happy/needy/distant)
* 💤 sleep cycles tied to real clock
* 🐾 multiple pets interacting
* 🔊 sound + animation layer

🧡 Credits
Built using:
* Python simulation engine
* Ollama local LLM runtime
* custom agent + memory architecture
