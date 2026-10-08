# 🎬 TouchGrass — Hackathon Video Pitch & Demo Script
> **Official 2-Minute Presentation & Demo Script**  
> *Targeted for Hacktoberfest 2026 Open-Source AI Challenge: Week 1 ("Touch Grass")*  
> *Prizes: Grand Prize ($250) • Best Use of TabPFN ($200) • Best Use of ElevenLabs ($200) • Best Use of Sentry ($200)*

---

## ⏱️ Video Breakdown at a Glance

| Timestamp | Video Section | Screen / Visual State | Spoken Voiceover Narration |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:15** | **The Hook** | Split comparison: Endless TikTok/Twitter doomscrolling vs. TouchGrass clean flat interface. | *"Most modern apps are designed around a single predatory funnel: capture your attention and keep you staring at a screen forever. Even AI tools want you in a chat window all day. We built TouchGrass on the opposite principle: **The application succeeds when you stop using it.**"* |
| **0:15 – 0:35** | **The Mission Briefing** | Page 1 (Mission card, Fraunces serif, Figtree, duration selector 5m/15m/30m). | *"Instead of outputting text to consume, TouchGrass outputs physical real-world action. When you open TouchGrass, you get an inspiring, minimal mission briefing—like 'Find a tree and spend two minutes looking at it.' You can customize duration, listen to spoken narration, or request an alternate deed."* |
| **0:35 – 0:55** | **TabPFN Microclimate Forecaster** | Zoom in on the **OUTDOOR VITALITY FORECAST** badge (`TabPFN Foundation Model`, `Optimal window: Today 10:30 AM`, `Vitality 91/100`). | *"To give users the best outdoor experience, we integrated **TabPFN—the Prior Labs Tabular Foundation Model**. TabPFN evaluates hourly solar elevation, UV index, humidity, and temperature gradients to pinpoint the exact 15-minute window for optimal circadian sunlight without harsh midday UV."* |
| **0:55 – 1:15** | **Offline Trail Mode** | Click the **Offline mode** pill button in the top right. Green banner appears. | *"Because nature often has zero cell signal, TouchGrass is 100% local-first. In backcountry trail mode, challenges, reflections, and TabPFN prior models run entirely on-device with zero data sent to the cloud. Complete privacy, zero signal required."* |
| **1:15 – 1:35** | **Zen Mode (Outside Page)** | Click **[Start mission]**. Screen transitions to deep dark `#16211B` with 260px/180px concentric circles and countdown. | *"The moment you accept the mission, the screen visually steps aside into Zen Mode. Dual concentric circles count down your outdoor presence. Put your phone in your pocket. At 00:00, an organic 528Hz Tibetan singing bowl chime sounds."* |
| **1:35 – 1:50** | **Reward & Journey** | Click **[I'm back]** ➔ Page 3 (Mission Complete) ➔ Fill reflection (+10 XP) ➔ Journey dashboard. | *"When you return, you record a quick reflection. Your Journey tab maintains a permanent on-device diary, lifetime outdoor minutes, and a 7-day habit tracker. Real-world dopamine replaces algorithmic likes."* |
| **1:50 – 2:00** | **Conclusion & Pitch** | Hackathon summary card with 4 partner badges (Gemma 2, TabPFN, ElevenLabs, Sentry). | *"TouchGrass combines open-weight Gemma 2, TabPFN tabular forecasting, ElevenLabs voice, and Sentry observability into a cohesive open-source tool. **Real life is greater than screen time.** Thank you!"* |

---

## 🎙️ Spoken Script for Recording (Word-for-Word)

```text
"Hey everyone! This is our submission for Hacktoberfest 2026 Week One: TouchGrass.

Most modern software traps your attention in an endless loop of screen time, feeds, and ad impressions. Even modern AI assistants often keep you glued to a chat prompt. 

TouchGrass completely reverses this equation. Its primary design goal is simple: the app succeeds when the user stops using it.

When you open TouchGrass, you receive a crisp, intentional outdoor mission. Today's mission: 'Find a tree and spend two minutes looking at it. Notice the bark, the leaves, and what moves around it.' 

To ensure the best outdoor experience, we integrated Prior Labs' TabPFN tabular foundation model. TabPFN analyzes hourly solar elevation, ambient temperature, humidity, and UV levels to forecast your peak outdoor vitality window—recommending the ideal time for circadian reset while avoiding midday UV glare.

Because the best outdoor trails have zero cell service, TouchGrass includes full Offline Trail Mode. All mission generation, TabPFN tabular priors, and reflection notes operate on-device with zero third-party tracking.

When you tap 'Start Mission', the UI gets out of your way. It transitions into a calm, dark Zen Mode with dual concentric rings and a countdown timer. You put your phone in your jacket pocket and step outside. When time expires, a peaceful 528 Hz Tibetan bell chime alerts you.

Back inside, you tap 'I'm back' to log your outdoor reflection, earn XP, and view your 7-day activity habits in your personal Journey diary.

TouchGrass is 100% open source under the MIT license, built with React, Tailwind, FastAPI, Gemma 2, TabPFN, ElevenLabs, and Sentry. 

Remember: Real life is greater than screen time. Thank you!"
```

---

## 🛠️ Automated Tools Included in Codebase

1. **Interactive In-Browser Video Studio:**  
   Open `http://localhost:8000/demo-video` (or open [`video_walkthrough.html`](file:///Users/rajanmishra/Desktop/hack2/video_walkthrough.html) in your browser).  
   Click **"Play Video"** to watch the synchronized 1080p walkthrough with live neural AI voice narration and Tibetan singing bowl chime.  
   Click **"Record & Download Video"** to save an instant `.webm` / `.mp4` video file!

2. **Pre-Generated Demo Video GIF:**  
   [`touchgrass_demo.gif`](file:///Users/rajanmishra/Desktop/hack2/touchgrass_demo.gif) (also saved in `~/Downloads/touchgrass_demo.gif`) — ready to drag and drop directly into Devpost, GitHub README, or Twitter.

3. **Individual Scene Voice Clips:**  
   All 9 scene narration audio files are pre-generated in the [`audio/`](file:///Users/rajanmishra/Desktop/hack2/audio/) folder.
