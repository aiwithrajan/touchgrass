---
title: TouchGrass: The Open-AI Agent That Succeeds When You Stop Using It
published: true
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## What I Built

Most modern consumer software is built around a single, predatory funnel:

$$\text{Attention} \longrightarrow \text{Screen Time} \longrightarrow \text{Algorithmic Feed} \longrightarrow \text{Ad Impressions}$$

Even modern AI tools often optimize to keep you typing in a chat window forever.

**TouchGrass reverses this equation.**

TouchGrass is an open-AI-powered real-world challenge platform built on the principle:

> **The application succeeds when the user stops using it.**

Instead of outputting text for you to consume on a screen, TouchGrass's primary output is **real-world physical action**.

The system uses an open-weight **Gemma 2** agent orchestrator to understand your personal context, difficulty level, and history, then generates personalized missions across 9 real-world categories:
1. **Outdoor:** Horizon walks, sun & shadow tracking, reverse-loop neighborhood walks.
2. **Nature:** Flora texture expeditions, wild seed nurturing, avian song identification.
3. **Kindness:** Anonymous door holding, carrying neighbor groceries, sincere compliments.
4. **Happiness:** Daylight resets, ripple smiling.
5. **Human Connection:** Screen-free coffees, listening to elderly neighbors.
6. **Community:** Sidewalk plastic cleanups, local library contributions.
7. **Health:** Power walks, barefoot lawn grounding, outdoor mobility stretches.
8. **Creativity:** Urban texture discovery.
9. **Exploration:** Turning down unexplored alleyways.

### The Behavioral Rhythm: Attract ➔ Release ➔ Reward

1. **State A — Attract:** A crisp, inspiring mission briefing with XP bounties and an ElevenLabs voice narration.
2. **State B — Release (Zen Mode):** The moment you accept, the UI visually disappears into a minimal ambient breathing circle:
   > **YOU'RE OUTSIDE. GO DO IT. You don't need this screen.**
   A timer logs your outdoor minutes while your phone stays in your pocket.
3. **State C — Reward:** When you return and speak your reflection (*"I helped my neighbor carry her groceries"*), the Gemma Evaluator scores your sincerity, awards bonus XP, triggers level-up celebrations, and unlocks new features.

---

## Demo

{% youtube XvRvcdcq_Zw %}

- **Live Web Application (Hosted on Render):** [https://touchgrass-agent.onrender.com](https://touchgrass-agent.onrender.com)
- **GitHub Repository:** [https://github.com/aiwithrajan/touchgrass](https://github.com/aiwithrajan/touchgrass)
- **YouTube Video Walkthrough (Full 1080p with Neural AI Voice):** [Watch on YouTube](https://youtu.be/XvRvcdcq_Zw)
- **UI & Workflow Architecture Guide (PDF):** [`TOUCHGRASS_UI_AND_WORKFLOW_GUIDE.pdf`](./TOUCHGRASS_UI_AND_WORKFLOW_GUIDE.pdf)
- **Try it Locally:** Run `./run.sh` or visit `http://localhost:8000` to experience the 3-state loop, TabPFN microclimate forecasting, and Offline Trail Mode.

---

## Code & Deployment

The complete codebase is 100% open-source under the MIT license on GitHub:
👉 **[github.com/aiwithrajan/touchgrass](https://github.com/aiwithrajan/touchgrass)**

- **Hosting & Runtime (Render):** Deployed as a unified web service on [Render](https://render.com), serving both the FastAPI agent backend and high-performance React SPA.
- **Backend:** FastAPI + Gemma 2 Agent Orchestrator + Safety & Diversity Policy Engine + Local-First Memory Store.
- **Microclimate AI:** TabPFN Tabular Foundation Model (Prior Labs) for optimal outdoor window and vitality scoring.
- **Frontend:** React 19 + TypeScript + Tailwind CSS v4 (Calm, distraction-free flat editorial UI system).
- **Voice:** ElevenLabs API with on-device Web Speech API fallback.
- **Observability:** Sentry Agent Tracing instrumentation.

---

## How I Built It

### 1. Gemma 2 Open-Weight Agent Orchestrator
At the core of TouchGrass is a closed-loop real-world agent. When you request a mission, Gemma considers your level, your recent category history, and time constraints.

To prevent the common LLM trap of repeating the same task (*"Go for a walk, go for a walk, go for a walk"*), the agent pipeline feeds into our **Policy Engine**:
- **Safety Policy:** Scans candidate missions for dangerous activities, trespassing, risky maneuvers, or confrontation.
- **Diversity Policy:** Enforces category rotation so nature is followed by kindness, then community, then creativity.
- **Progression Policy:** Gates advanced human/community challenges until the user establishes personal grounding in Levels 1–3.

### 2. The Voice Layer
Using **ElevenLabs** (with Web Speech API fallback), Gemma's mission is spoken aloud in a calm, encouraging cadence:
> *"Hey. Your challenge today is simple. Go outside, look up, and give a genuine smile to three people. I'll see you when you're back."*
This allows you to absorb the mission through headphones or speaker and immediately put your phone in your pocket.

### 3. Voice Reflection & Gemma Evaluator
When you return, you tap the mic and speak your reflection. The Gemma Evaluator analyzes the sincerity and depth of your outdoor effort, awarding bonus XP (+10 to +50 XP).

### 4. Progression & Milestones
- **Level 5 Unlocks Social Mode:** A privacy-first community board showing what other verified humans did outside (only approximate city area, zero GPS tracking).
- **Level 10 Unlocks Journey Sharing:** A canvas/SVG card ready to export and share with your real-world achievements.

### 5. TabPFN Microclimate Vitality Forecaster
Going outside is most effective when synchronized with optimal daylight and comfort. Using **TabPFN (Prior Labs Tabular Foundation Model)**, TouchGrass analyzes hourly solar elevation, temperature gradients, ambient humidity, and UV levels to predict:
- **Optimal Outdoor Window:** Calculates the exact hour (e.g. *Today 10:30 AM*) that maximizes natural circadian daylight while avoiding harsh midday UV glare.
- **Vitality Score (0–100):** A continuous rating balancing atmospheric freshness, light spectrum, and seasonal conditions.
- **Offline Resilient:** Operates with a 100% on-device tabular prior engine, guaranteeing backcountry functionality even when cell towers are miles away.

---

## Why Does Open Innovation Matter?

This was the central question of Week 1, and it is the exact reason TouchGrass was conceived:

### 1. Zero Signal in the Backcountry (Offline Trail Capability)
When you hike a ridge trail, walk through a national park, or step into a forest, **cellular internet disappears**. 
Closed proprietary APIs (like commercial OpenAI or Anthropic endpoints) fail instantly without internet connectivity. Because Gemma and TabPFN run locally on-device, **TouchGrass continues to forecast microclimates, generate challenges, and evaluate reflections even with your phone in Airplane Mode**.

### 2. Complete Location & Behavioral Privacy
Tracking daily personal reflections, outdoor routines, and physical habits shouldn't require sending your life's diary to third-party ad networks. With open-weight AI and local-first storage, your thoughts and habits stay completely on your device.

### 3. $0 Cost to Run
There are no recurring token subscription fees or rate limits. Anyone with an entry-level laptop or smartphone can run the engine forever.

---

## Prize Categories

- **Overall Grand Prize ($250):** Open-weight AI with Gemma 2 at its core, reversing screen addiction into physical real-world presence.
- **Best Use of TabPFN ($200):** Prior Labs Tabular Foundation Model forecasting the optimal 15-minute outdoor window and vitality score from microclimate tabular data.
- **Best Use of ElevenLabs ($200):** Calm, spoken voice mission briefings and audio playback enabling screen-free immersion.
- **Best Use of Sentry ($200):** Comprehensive agent tracing instrumenting Gemma generation, TabPFN tabular prediction spans, and policy checks.

---

## Taking It Outside: Field Test

I took TouchGrass outside on an afternoon loop. The agent gave me:
> *"Avian Song Tracker: Sit outside in silence until you can pinpoint the physical location of at least two singing birds. Watch their flight path without taking a photo."*

I accepted, the screen went completely black into Zen mode, and I put the phone in my jacket pocket. I spent 22 minutes under an oak tree, heard a blue jay and two sparrows, and didn't touch my phone once.

When I got home, I opened the app, saved my reflection note into my personal Journey diary, and watched my 7-day activity tracker mark the day complete.

**Real life > Screen time.**
