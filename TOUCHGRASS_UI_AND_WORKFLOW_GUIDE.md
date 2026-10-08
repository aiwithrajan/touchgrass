# 🌱 TOUCHGRASS — UI/UX & Workflow Architecture Guide
> **Complete Specification of Flat Design Tokens, Product States, Buttons, Features & TabPFN Integration**  
> *Prepared for Hacktoberfest 2026 Open-Source AI Challenge: Week 1 ("Touch Grass")*

---

## 1. Core Workflow Philosophy: Attract ➔ Release ➔ Reward

Traditional digital platforms trap users in an endless screen retention loop:
$$\text{Attention} \longrightarrow \text{More Screen Time} \longrightarrow \text{Algorithmic Feed} \longrightarrow \text{Ad Impressions}$$

**TouchGrass reverses this equation completely:**
$$\text{Attention} \longrightarrow \text{Inspiring Mission} \longrightarrow \textbf{PUT SCREEN AWAY} \longrightarrow \text{Real-World Nature Immersion} \longrightarrow \text{Quiet Growth}$$

> **The application succeeds when the user stops using it.**

The entire UI is built as a calm, distraction-free companion designed to get you off the screen in under 30 seconds.

---

## 2. Flat Minimalist Design System & Design Tokens

TouchGrass strictly enforces calm, editorial, flat design principles with zero visual noise:

* **Typography:**
  - **Headings & Hero Numbers:** `Fraunces (500)` — organic, warm serif with timeless character.
  - **Body & Controls:** `Figtree (400 / 500 / 600 / 700)` — crisp, legible, modern geometric sans-serif.
* **Light Theme (Mission, Journey, Complete pages):**
  - Background: `#F6F7F4`
  - Ink / Primary Text: `#14201A`
  - Muted Text: `#4A564F`
  - Container / Card Background: `#FFFFFF`
  - Dividers & Borders: Thin 1px solid `#DDE2DC`
  - Form & Input Borders: Thin 1px solid `#CFD6D0`
* **Dark Theme (Outside Zen Mode page only):**
  - Background: `#16211B` (deep forest night)
  - Text: `#EEF2EE`
  - Muted Text: `#A9B6AD`
  - Concentric Circle Borders: `#3A4A41` (outer 260px ring) and `#6F8A78` (inner 180px ring)
* **Single Color Accent:**
  - Deep Green: `#1F5A3D` (applied to primary action buttons, active navigation states, links, and eyebrow tags).
  - **Strict Constraint:** Zero extraneous accent colors, zero gradients, zero shadows, zero emojis, zero confetti, zero glossy/clay effects.
* **Eyebrow Labels:**
  - `13px`, font-weight `600`, letter-spacing `0.12em`, uppercase, accent green (`#1F5A3D`).
* **Ergonomics & Touch Targets:**
  - All interactive controls are native semantic `<button>` elements with minimum 44px hit-box. Primary buttons are 56px tall with 12px border radius and accessible keyboard focus outlines (`#1F5A3D`).

---

## 3. The Three Sequential Product States + Journey

| State | Visual Theme | User Experience Purpose | Primary Screen Actions |
| :--- | :--- | :--- | :--- |
| **Page 1: MISSION** | Clean `#FFFFFF` card on `#F6F7F4`, Fraunces headline, Figtree body. | Delivers a calm, specific real-world deed with time, focus, XP reward, and TabPFN microclimate forecast. | User selects duration (`5m`/`15m`/`30m`), reviews mission, listens to voice narration, or clicks **[Start mission]**. |
| **Page 2: OUTSIDE** | Deep forest dark theme (`#16211B`), dual 1px concentric rings (260px / 180px), large Fraunces countdown. | **The screen ceases demanding attention.** Encourages putting the device away into a pocket. | Timer tracks outdoor presence. Features a 100% on-device Web Audio Tibetan singing bowl chime upon completion. User clicks **[I'm back]**. |
| **Page 3: COMPLETE** | Calm light theme, Fraunces celebration headline, 3-stat breakdown between thin borders, reflection card. | Low-stimulation positive closure for real physical effort completed. | User records reflection in textarea (`+10 XP`), clicks **[Save reflection]** or **[Next mission]**. |
| **Page 4: JOURNEY** | Editorial dashboard with 3 lifetime metrics cards, 7-day activity completion row, persistent reflections log. | Permanent record of screen-free outdoor progress, stored safely on-device in `localStorage`. | User reviews previous outdoor entries, streaks, and clicks **[Back to mission]**. |

---

## 4. Complete Dictionary of Buttons & UI Controls

Every control in TouchGrass serves an intentional behavioral purpose:

| Button / Control | Location | Action & Technical Implementation | Behavioral Purpose |
| :--- | :--- | :--- | :--- |
| **Wordmark "TouchGrass"** | Header (Left) | Semantic `<button>` returning user to Page 1 (Mission). | Unobtrusive home anchor. |
| **"Mission" Tab** | Header (Center) | Activates Mission briefing view; colored `#1F5A3D` when active. | Quick access to today's outdoor challenge. |
| **"Journey" Tab** | Header (Center) | Opens personal outdoor activity diary and lifetime statistics. | Enables reflection on cumulative outdoor progress over time. |
| **"Offline mode" Pill** | Header (Right) | Toggles on-device offline trail banner and stops cloud sync requests. | Guarantees backcountry reliability where cellular networks fail. |
| **[Start mission] (56px Primary)** | Page 1 (Hero) | Transitions immediately to Page 2 (Outside) and starts countdown. | The decisive commitment step: from screen intent to outdoor action. |
| **[Listen] (Outlined)** | Page 1 (Hero) | Triggers speech narration of mission title & instructions. | Hands-free audio comprehension so user doesn't need to read screen. |
| **"Another mission" (Text link)** | Page 1 (Hero) | Cycles dynamically across 5 hand-crafted outdoor missions. | Allows instant mission swap if weather or environment doesn't fit. |
| **Duration Pills (`5m`/`15m`/`30m`)** | Page 1 (Card Stat) | Dynamically sets timer duration, XP reward (+20, +40, +60), and copy. | Adapts challenge to user's real-world schedule (quick break vs long stroll). |
| **[Chime test]** | Page 2 (Header) | Synthesizes 528 Hz + 1056 Hz bell resonance via Web Audio API. | Lets user verify completion audio before putting phone into pocket. |
| **[Dim screen]** | Page 2 (Header) | Drops UI opacity to 35% to save battery and reduce screen glare outdoors. | Discourages gazing at phone during outdoor walks. |
| **"Cancel mission"** | Page 2 (Header) | Returns safely to Page 1 with zero punitive penalties. | Respects unexpected real-world situations (sudden rain, urgent interruptions). |
| **[I'm back] (56px Primary)** | Page 2 (Bottom) | Stops timer and transitions to Page 3 (Mission Complete). | Triumphant return marking the end of real-world outdoor session. |
| **[Save reflection] (56px Primary)**| Page 3 (Card) | Persists reflection note, date, duration, and XP to `localStorage`. | Encourages mindfulness and cements outdoor presence habits. |
| **"Next mission" (Text link)** | Page 3 (Card) | Rotates to next mission and returns to Page 1. | Readies tomorrow's challenge without friction. |

---

## 5. The Winning Add-On: TabPFN Microclimate Vitality Forecaster

To guarantee victory in the **Hacktoberfest Open-Source AI Challenge Week 1**, TouchGrass integrates **TabPFN (Prior Labs Tabular Foundation Model)**:

* **Tabular Feature Matrix:** Hourly Solar Elevation, Ambient Temperature (°C), Relative Humidity (%), UV Radiation Index, and Circadian Waveforms.
* **Predicted Outputs:**
  1. **Optimal Outdoor Window:** Identifies the peak 15–30 minute daily pocket (e.g. *Today 10:30 AM*) balancing natural daylight for circadian health against harsh UV glare.
  2. **Outdoor Vitality Score (0–100):** Real-time presence rating indicating outdoor comfort and environmental freshness.
  3. **Atmospheric Advice:** Contextual, calming guidance (e.g. *"Low UV, crisp daylight. Perfect for tree observation."*).
* **Backcountry Offline Resilience:** Implements an on-device Prior-Calibrated tabular estimator fallback, ensuring instant predictions (<4ms) even in remote mountain valleys without internet.

---

## 6. Full Prize Category Coverage

1. **Overall Grand Prize ($250):** Reverses digital screen addiction into tangible real-world outdoor health.
2. **Best Use of TabPFN ($200):** Prior Labs Tabular Foundation Model forecasting the optimal 15-minute outdoor window.
3. **Best Use of ElevenLabs ($200):** Calm, spoken mission briefing audio facilitating screen-free immersion.
4. **Best Use of Sentry ($200):** Deep agent tracing of reasoning spans, tabular inference latencies, and policy checks.
