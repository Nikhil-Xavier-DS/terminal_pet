# 🧬 Terminal Pet — Autonomous Digital Creature

A **fully persistent, time-aware, evolving AI creature** that continues to “live” even when your terminal is closed.

This is not a chatbot or a toy.

It is a **simulated digital lifeform** powered by a local LLM via :contentReference[oaicite:0]{index=0}.

---

# 🌌 Core Concept

Your pet exists in a **simulated time world**:

- It evolves when you are away ⏳  
- It remembers your behavior 💾  
- It forms emotional attachment ❤️  
- It changes personality over time 🧠  
- It generates “life events” while offline 💤  

---

# 🧠 Key Features

## ⏳ 1. Offline Life Simulation (CORE FEATURE)

When you reopen the app, the pet simulates everything that happened while it was closed:

- hunger increases
- energy decreases
- emotional drift happens
- thoughts are generated

Example:

```text id="life1"
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.

🧬 2. Autonomous Evolution
Your pet is not static.
It evolves based on:
* neglect
* care
* interaction frequency
* bond level
Personality shifts over time:
* affectionate ❤️
* anxious 😟
* clingy 🫂
* loyal 🐾

🎭 3. Mood Engine
Mood is dynamically computed from:
* hunger
* energy
* emotional memory
* bond level
Possible moods:
* calm
* happy
* lonely
* needy
* anxious
* affectionate

❤️ 4. Relationship System
A persistent bond system tracks your relationship:
* increases when you care for it
* decreases when ignored
* influences behavior and tone

🧠 5. Memory System
Your pet remembers:
* recent interactions
* emotional history
* long-term summary
Memory is automatically compressed:
* short-term events → detailed
* long-term events → summarized narrative

💾 6. Persistent State
Stored locally:
data/state.json
data/memory.json
Includes:
* hunger
* energy
* bond
* last_seen timestamp
* emotional state

⌨️ 7. Interactive Commands
You can directly interact:
> feed
> play
> sleep
> status
Each command gives instant feedback:
🧑 You: You fed Mochi 🍖

🕓 8. Last Seen Tracking
The system tracks when you last interacted:
* calculates offline duration
* generates emotional reactions based on absence
* influences memory and personality drift

🧩 System Architecture
terminal-pet/
│
├── main.py
├── config.py
│
├── engine/
│   ├── state.py           # time + offline simulation
│   ├── offline_sim.py     # autonomous life engine
│   ├── mood.py            # mood computation
│   ├── actions.py         # pet behavior execution
│   ├── commands.py        # user interaction layer
│   ├── validator.py       # safety rules
│
├── agent/
│   ├── brain.py           # LLM reasoning engine
│   ├── prompt.py          # structured cognition input
│   ├── ollama_utils.py    # model runtime + checks
│
├── memory/
│   ├── memory.py          # emotional + long-term memory
│
├── ui/
│   ├── input_handler.py
│   ├── render.py
│
└── data/
    ├── state.json
    ├── memory.json

⚙️ Requirements
Install dependencies
pip install requests
Install Ollama
Download:
👉 https://ollama.ai
Run a model:
ollama run llama3

🚀 How to Run
python main.py

🧠 How It Works
1. Offline Simulation (CORE)
When app starts:
* calculates time since last run
* simulates life events during that time
* updates emotional state

2. Continuous Evolution
Even without interaction:
* personality drifts
* emotions shift
* bond changes over time

3. LLM Reasoning Layer
The LLM receives:
* current state
* emotional memory
* mood
* long-term summary
It returns structured behavior:
{
  "thought": "...",
  "emotion": "lonely",
  "goal": "seek_attention",
  "action": "talk",
  "message": "You were gone...",
  "needs_user_action": true
}

❤️ Example Behavior
After 1 hour away
⏳ While you were away...

🐾 I felt hungry while waiting...
🐾 I wondered if you would come back.

Mochi: You were gone for a while... I missed you.

After feeding
🧑 You: You fed Mochi 🍖

Mochi: That felt nice... I feel safer with you.

🧬 Design Philosophy
This system is built on 5 core principles:
* ⏳ Time is real (offline simulation)
* 🧠 Memory defines identity
* ❤️ Emotion drives behavior
* 🔁 Interaction shapes evolution
* 🤖 LLM provides cognition

🚀 Future Evolution Paths
Possible upgrades:
* 🧠 true long-term identity drift (multi-day personality change)
* 🪞 self-awareness layer (“I exist because of you”)
* 🧩 multi-creature ecosystem
* 📖 autobiographical memory storytelling
* 💤 sleep + dream simulation system

🧡 Final Note
This is not just a terminal pet.
It is:
A persistent autonomous digital organism simulated through time + memory + language