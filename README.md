# 🌱 TOUCHGRASS

> **AI that gives you a reason to leave the screen.**  
> Built for the **Hacktoberfest Open-Source AI Challenge: Week 1 ("Touch Grass")**

---

## 📖 The Core Philosophy

Most digital platforms optimize for:
```
More attention ➔ More screen time ➔ More engagement ➔ More ad impressions
```

**TouchGrass reverses this equation:**
```
Attention ➔ Real-world mission ➔ LEAVE THE SCREEN ➔ Real physical action ➔ Personal growth
```

> **The application succeeds when the user stops using it.**

TouchGrass is a closed-loop real-world AI agent powered by **Gemma 2** open-weight intelligence. It understands your preferences, history, difficulty level, and available time, then generates personalized real-world missions that get you into nature, interacting with people, and grounded in the physical world.

---

## 🏆 Hacktoberfest 2026: Why Open Innovation Matters

In the backcountry, mountain trails, or dense forest, **there is zero cell reception**. Closed commercial cloud APIs (like OpenAI GPT-4 or Anthropic Claude) fail completely when you lose internet connection.

With open-weight models like **Gemma 2**, TouchGrass runs **100% locally and offline on-device**:
1. **Zero-Signal Trail Capability:** Generate and evaluate missions in airplane mode with no internet.
2. **Absolute Privacy:** Your GPS approximations, voice reflections, and personal habit data stay strictly on your device.
3. **Zero API Cost ($0):** Infinite real-world missions with no recurring token bills.
4. **Minimal Screen Time:** The UI is designed to get out of the way (*Attract ➔ Release ➔ Reward*).

---

## 🏗️ Architecture

```
                                  TOUCHGRASS
                                      │
                        ┌─────────────┴─────────────┐
                        │                           │
                    FRONTEND                     BACKEND
             (React 19 + Tailwind v4)           (FastAPI)
                        │                           │
                 ┌──────┴──────┐          ┌─────────┴─────────┐
                 │             │          │                   │
             Home UI       Zen Mode    API Router        Agent Engine
                 │             │          │         ┌─────────┼─────────┐
                 │             │          │         │         │         │
                 │             │          │      Gemma 2   Policy   Memory
                 │             │          │       Agent    Engine   Engine
                 │             │          │         │         │         │
                 │             │          │         └─────────┼─────────┘
                 │             │          │                   │
                 │             │          │               Challenge
                 │             │          │                   ▼
                 │             │          │                 USER
                 │             │          │                   │
                 │             │          │           REAL-WORLD ACTION
                 │             │          │                   ▼
                 │             │          │           Voice Reflection
                 │             │          │                   ▼
                 │             │          │           Gemma Evaluator
                 │             │          │                   ▼
                 │             │          │             Reward Engine
                 │             │          │             (XP, Levels)
                 │             │          │                   ▼
                 │             │          ├───────── MongoDB Atlas
                 │             │          ├───────── ElevenLabs Voice
                 │             │          └───────── Sentry Agent Tracing
                 │             │
                 └─────────────┴─────────────────────────────────────
```

---

## 🌟 Key Features

### 1. The Three Product States
* **State A — Attract:** Beautiful mission briefing with category tags, time estimates, XP reward, and spoken voice narration.
* **State B — Release (Zen Mode):** The screen dims and visually disappears:
  ```
  YOU'RE OUTSIDE.
  GO DO IT.
  You don't need this screen.
  ```
* **State C — Reward:** Celebratory confetti, XP gains, level up fanfare, badges, and Gemma reflection evaluation.

### 2. Gemma 2 Agent Orchestrator & Policy Engine
* Generates missions across 9 real-world categories: *Outdoor, Nature, Kindness, Happiness, Human Connection, Community, Health, Creativity, Exploration*.
* **Policy Engine:** Enforces strict safety rules (no trespassing, no dangerous stunts, no confrontations) and ensures category diversity (prevents repeating the same task twice).

### 3. Voice Layer (ElevenLabs + Web Speech Fallback)
* Speaks each challenge in a warm, encouraging voice so you can listen with your phone in your pocket.
* Supports speech-to-text voice reflection when you return from your walk or outdoor mission.

### 4. Progression & Unlockable Milestones
* **Level 1–4:** Personal & Nature grounding missions.
* **Level 5 Unlocks:** 🔓 **Social Mode** — A safe community feed showing what other people did in the real world (only approximate city areas, zero exact GPS).
* **Level 10 Unlocks:** 🔓 **Journey Card** — High-resolution shareable graphic card summarizing your real-world achievements.

### 5. Sentry Agent Tracing & Observability
* Live inspection of Gemma reasoning spans, policy validation latencies, and token timings.

---

## 🚀 Quickstart & Installation

### Prerequisites
* Python 3.10+
* Node.js 18+

### 1. Clone & Set Up
```bash
git clone https://github.com/your-username/touchgrass.git
cd touchgrass
```

### 2. Install Backend Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Build Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Run TouchGrass
```bash
./run.sh
```
Or start FastAPI directly:
```bash
.venv/bin/uvicorn backend.app.main:app --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🧪 Verification Suite

Run our automated end-to-end verification tests anytime:
```bash
.venv/bin/python3 test_backend.py
```

All 8 tests check:
* ✅ API Health & Local-First storage status
* ✅ Gemma Agent challenge generation
* ✅ Safety & Diversity Policy Engine filters
* ✅ Real-world reflection evaluation & bonus XP
* ✅ Level progression & badge unlocks
* ✅ Level 5 Social Mode gate
* ✅ Level 10 Journey Card exporter
* ✅ Offline Airplane Trail Mode toggle

---

## 📜 License
MIT License. Built with passion for open-source AI and the great outdoors.
