"""
TouchGrass Animated Demo Video / GIF Generator
Renders an 8-scene high-resolution animated walkthrough (960x600)
demonstrating the entire TouchGrass workflow:
1. Title & Value Prop
2. Page 1: Mission Briefing with TabPFN Microclimate Vitality Forecast
3. Duration Selection & Focus Interaction (5m / 15m / 30m)
4. Offline Trail Mode Activation Banner
5. Page 2: Outside (Zen Mode) with Concentric Rings Countdown
6. Completion Chime (528 Hz Web Audio resonance)
7. Page 3: Mission Complete & Reflection Entry (+10 XP)
8. Page 4: Journey Dashboard with 7-Day Activity Tracker & History
9. Victory Summary & Prize Tracks
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int, bold: bool = False):
    try:
        font_path = '/System/Library/Fonts/Helvetica.ttc'
        # Helvetica index 1 is often Bold, 0 is regular in macOS TTC
        index = 1 if bold else 0
        return ImageFont.truetype(font_path, size=size, index=index)
    except Exception:
        try:
            return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=size)
        except Exception:
            return ImageFont.load_default()

def draw_header(draw, active_tab="Mission", offline=False, dark=False):
    bg_border = "#3A4A41" if dark else "#DDE2DC"
    text_color = "#EEF2EE" if dark else "#14201A"
    muted_color = "#A9B6AD" if dark else "#4A564F"
    green_color = "#1F5A3D"

    # Header bottom border
    draw.line([(0, 60), (960, 60)], fill=bg_border, width=1)

    # Wordmark
    f_logo = get_font(18, bold=True)
    draw.text((48, 20), "TouchGrass", fill=text_color, font=f_logo)

    # Tabs
    f_tab = get_font(15, bold=True)
    f_tab_normal = get_font(15, bold=False)

    m_font = f_tab if active_tab == "Mission" else f_tab_normal
    m_color = green_color if (active_tab == "Mission" and not dark) else (text_color if dark and active_tab == "Mission" else muted_color)
    draw.text((420, 20), "Mission", fill=m_color, font=m_font)

    j_font = f_tab if active_tab == "Journey" else f_tab_normal
    j_color = green_color if (active_tab == "Journey" and not dark) else (text_color if dark and active_tab == "Journey" else muted_color)
    draw.text((500, 20), "Journey", fill=j_color, font=j_font)

    # Offline pill button
    pill_text = "Offline active" if offline else "Offline mode"
    pill_bg = green_color if offline else ("#16211B" if dark else "#F6F7F4")
    pill_border = green_color if offline else bg_border
    pill_text_color = "#FFFFFF" if offline else text_color

    draw.rounded_rectangle([(800, 14), (912, 46)], radius=16, fill=pill_bg, outline=pill_border, width=1)
    f_pill = get_font(13, bold=True)
    draw.text((816, 22), pill_text, fill=pill_text_color, font=f_pill)

    # Offline Banner if active
    if offline and not dark:
        draw.rectangle([(0, 61), (960, 88)], fill="#EBF0EC")
        draw.line([(0, 88), (960, 88)], fill="#DDE2DC", width=1)
        f_banner = get_font(12, bold=True)
        draw.text((120, 67), "Offline trail mode active: All missions & reflections stored on-device with zero data sent to cloud.", fill="#1F5A3D", font=f_banner)

def draw_cursor(draw, x, y):
    """Draws a crisp mac-style pointer arrow"""
    points = [(x, y), (x, y + 18), (x + 5, y + 14), (x + 10, y + 21), (x + 13, y + 20), (x + 8, y + 13), (x + 14, y + 13)]
    draw.polygon(points, fill="#14201A", outline="#FFFFFF")

def create_frames():
    frames = []

    # -------------------------------------------------------------
    # FRAME 1: Title Card / Intro Slate (1.8s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#16211B')
    draw = ImageDraw.Draw(img)

    f_title = get_font(44, bold=True)
    f_sub = get_font(18, bold=False)
    f_eyebrow = get_font(13, bold=True)
    f_badge = get_font(12, bold=True)

    draw.text((80, 180), "TOUCHGRASS", fill="#1F5A3D", font=f_eyebrow)
    draw.text((80, 215), "The Open-AI Agent That Succeeds\nWhen You Stop Using It.", fill="#EEF2EE", font=f_title)
    draw.text((80, 330), "Reversing digital screen retention into real-world physical outdoor action.\nWeek 1 Hacktoberfest 2026: Touch Grass.", fill="#A9B6AD", font=f_sub)

    # Badges
    pills = [
        "Prior Labs TabPFN Forecaster",
        "Gemma 2 Open Orchestrator",
        "ElevenLabs Voice Layer",
        "Sentry Agent Tracing"
    ]
    cur_x = 80
    for p in pills:
        draw.rounded_rectangle([(cur_x, 420), (cur_x + len(p)*7 + 24, 450)], radius=15, fill="#1F2E25", outline="#3A4A41", width=1)
        draw.text((cur_x + 12, 428), p, fill="#EEF2EE", font=f_badge)
        cur_x += len(p)*7 + 34

    frames.append((img, 1800))

    # -------------------------------------------------------------
    # FRAME 2: Page 1 (Mission Briefing) with TabPFN Forecaster (2.0s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#F6F7F4')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Mission", offline=False)

    # Left Column
    draw.text((64, 110), "TODAY'S MISSION", fill="#1F5A3D", font=get_font(12, bold=True))
    draw.text((64, 135), "Find a tree and spend\ntwo minutes looking at it.", fill="#14201A", font=get_font(34, bold=True))
    draw.text((64, 225), "Notice the bark, the leaves and what moves around it.\nNo phone until you are done.", fill="#4A564F", font=get_font(15))

    # Action Buttons
    draw.rounded_rectangle([(64, 290), (200, 342)], radius=12, fill="#1F5A3D")
    draw.text((95, 305), "Start mission", fill="#FFFFFF", font=get_font(14, bold=True))

    draw.rounded_rectangle([(215, 290), (310, 342)], radius=12, fill="#F6F7F4", outline="#DDE2DC", width=1)
    draw.text((245, 305), "Listen", fill="#14201A", font=get_font(14, bold=True))

    draw.text((330, 305), "Another mission", fill="#1F5A3D", font=get_font(14, bold=True))

    # Right Card
    draw.rounded_rectangle([(520, 100), (896, 520)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)

    # Stats Row
    draw.text((545, 120), "Time", fill="#4A564F", font=get_font(12))
    # Duration pills
    draw.rounded_rectangle([(545, 140), (575, 162)], radius=6, fill="#F6F7F4")
    draw.text((552, 144), "5m", fill="#4A564F", font=get_font(11, bold=True))
    draw.rounded_rectangle([(580, 140), (615, 162)], radius=6, fill="#1F5A3D")
    draw.text((586, 144), "15m", fill="#FFFFFF", font=get_font(11, bold=True))
    draw.rounded_rectangle([(620, 140), (655, 162)], radius=6, fill="#F6F7F4")
    draw.text((626, 144), "30m", fill="#4A564F", font=get_font(11, bold=True))

    draw.text((690, 120), "Focus", fill="#4A564F", font=get_font(12))
    draw.text((690, 142), "Nature", fill="#14201A", font=get_font(15, bold=True))

    draw.text((795, 120), "Reward", fill="#4A564F", font=get_font(12))
    draw.text((795, 142), "40 XP", fill="#14201A", font=get_font(15, bold=True))

    draw.line([(545, 175), (870, 175)], fill="#DDE2DC", width=1)

    # How it works
    draw.text((545, 190), "How it works", fill="#14201A", font=get_font(17, bold=True))
    draw.text((545, 218), "1. Start the mission, then put your phone away.", fill="#4A564F", font=get_font(13))
    draw.text((545, 238), "2. Go outside and find a tree.", fill="#4A564F", font=get_font(13))
    draw.text((545, 258), "3. Come back, tap 'I'm back' and add a short reflection.", fill="#4A564F", font=get_font(13))

    # TabPFN Microclimate Vitality Section
    draw.line([(545, 290), (870, 290)], fill="#DDE2DC", width=1)
    draw.text((545, 305), "OUTDOOR VITALITY FORECAST", fill="#1F5A3D", font=get_font(11, bold=True))
    draw.rounded_rectangle([(735, 302), (870, 322)], radius=4, fill="#F6F7F4", outline="#DDE2DC", width=1)
    draw.text((745, 306), "TabPFN Foundation Model", fill="#4A564F", font=get_font(9, bold=True))

    draw.text((545, 335), "Optimal window: Today 10:30 AM", fill="#14201A", font=get_font(14, bold=True))
    draw.text((775, 335), "Vitality 91/100", fill="#1F5A3D", font=get_font(13, bold=True))

    draw.text((545, 360), "Crisp Morning Sunlight • 21.2°C • UV 3.8.\nOptimal natural light for circadian reset. Gentle UV for 15-30m outside.", fill="#4A564F", font=get_font(11))

    frames.append((img, 2000))

    # -------------------------------------------------------------
    # FRAME 3: Clicking Duration "30m" & Toggling "Offline mode" (1.8s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#F6F7F4')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Mission", offline=True)  # Offline banner appears!

    # Left Column
    draw.text((64, 130), "TODAY'S MISSION", fill="#1F5A3D", font=get_font(12, bold=True))
    draw.text((64, 155), "Find a tree and spend\ntwo minutes looking at it.", fill="#14201A", font=get_font(34, bold=True))
    draw.text((64, 245), "Notice the bark, the leaves and what moves around it.\nNo phone until you are done.", fill="#4A564F", font=get_font(15))

    # Action Buttons
    draw.rounded_rectangle([(64, 310), (200, 362)], radius=12, fill="#1F5A3D")
    draw.text((95, 325), "Start mission", fill="#FFFFFF", font=get_font(14, bold=True))

    draw.rounded_rectangle([(215, 310), (310, 362)], radius=12, fill="#F6F7F4", outline="#DDE2DC", width=1)
    draw.text((245, 325), "Listen", fill="#14201A", font=get_font(14, bold=True))

    draw.text((330, 325), "Another mission", fill="#1F5A3D", font=get_font(14, bold=True))

    # Right Card with 30m selected
    draw.rounded_rectangle([(520, 115), (896, 535)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((545, 135), "Time", fill="#4A564F", font=get_font(12))
    draw.rounded_rectangle([(545, 155), (575, 177)], radius=6, fill="#F6F7F4")
    draw.text((552, 159), "5m", fill="#4A564F", font=get_font(11, bold=True))
    draw.rounded_rectangle([(580, 155), (615, 177)], radius=6, fill="#F6F7F4")
    draw.text((586, 159), "15m", fill="#4A564F", font=get_font(11, bold=True))
    draw.rounded_rectangle([(620, 155), (655, 177)], radius=6, fill="#1F5A3D") # 30m active!
    draw.text((626, 159), "30m", fill="#FFFFFF", font=get_font(11, bold=True))

    draw.text((690, 135), "Focus", fill="#4A564F", font=get_font(12))
    draw.text((690, 157), "Nature", fill="#14201A", font=get_font(15, bold=True))

    draw.text((795, 135), "Reward", fill="#4A564F", font=get_font(12))
    draw.text((795, 157), "60 XP", fill="#14201A", font=get_font(15, bold=True)) # 60 XP for 30m

    draw.line([(545, 190), (870, 190)], fill="#DDE2DC", width=1)
    draw.text((545, 205), "How it works", fill="#14201A", font=get_font(17, bold=True))
    draw.text((545, 233), "1. Start the mission, then put your phone away.", fill="#4A564F", font=get_font(13))
    draw.text((545, 253), "2. Go outside and find a tree.", fill="#4A564F", font=get_font(13))
    draw.text((545, 273), "3. Come back, tap 'I'm back' and add a short reflection.", fill="#4A564F", font=get_font(13))

    draw.line([(545, 305), (870, 305)], fill="#DDE2DC", width=1)
    draw.text((545, 320), "OUTDOOR VITALITY FORECAST", fill="#1F5A3D", font=get_font(11, bold=True))
    draw.rounded_rectangle([(735, 317), (870, 337)], radius=4, fill="#F6F7F4", outline="#DDE2DC", width=1)
    draw.text((745, 321), "TabPFN Foundation Model", fill="#4A564F", font=get_font(9, bold=True))
    draw.text((545, 350), "Optimal window: Today 10:30 AM", fill="#14201A", font=get_font(14, bold=True))
    draw.text((775, 350), "Vitality 91/100", fill="#1F5A3D", font=get_font(13, bold=True))
    draw.text((545, 375), "Crisp Morning Sunlight • 21.2°C • UV 3.8.\nLocal TabPFN tabular engine: 100% functional in offline trail mode.", fill="#4A564F", font=get_font(11))

    # Cursor clicking "Start mission"
    draw_cursor(draw, 140, 330)

    frames.append((img, 1800))

    # -------------------------------------------------------------
    # FRAME 4: Page 2 (Outside / Zen Mode) - Concentric Circles (2.2s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#16211B')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Mission", offline=True, dark=True)

    # Concentric Circles (260px and 180px)
    cx, cy = 480, 270
    draw.ellipse([(cx - 130, cy - 130), (cx + 130, cy + 130)], outline="#3A4A41", width=1)
    draw.ellipse([(cx - 90, cy - 90), (cx + 90, cy + 90)], outline="#6F8A78", width=1)

    # Countdown Timer in center
    draw.text((cx - 58, cy - 22), "29:54", fill="#EEF2EE", font=get_font(42))

    # Mission instruction below circles
    draw.text((cx - 150, cy + 160), "Find a tree and look at it for two minutes.", fill="#EEF2EE", font=get_font(16, bold=True))
    draw.text((cx - 110, cy + 190), "Put your phone in your pocket.", fill="#A9B6AD", font=get_font(14))

    # Bottom Actions
    draw.rounded_rectangle([(cx - 90, 500), (cx + 90, 552)], radius=12, fill="#1F5A3D")
    draw.text((cx - 30, 516), "I'm back", fill="#FFFFFF", font=get_font(15, bold=True))

    # Chime test pill in header
    draw.text((700, 22), "Chime test", fill="#A9B6AD", font=get_font(13))
    draw.rounded_rectangle([(770, 14), (880, 46)], radius=16, outline="#3A4A41", width=1)
    draw.text((788, 22), "Dim screen", fill="#EEF2EE", font=get_font(13))

    frames.append((img, 2200))

    # -------------------------------------------------------------
    # FRAME 5: Outside Page Completion - Tibetan Chime at 00:00 (1.8s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#16211B')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Mission", offline=True, dark=True)

    # Concentric circles with active resonance glow
    cx, cy = 480, 270
    draw.ellipse([(cx - 130, cy - 130), (cx + 130, cy + 130)], outline="#6F8A78", width=2)
    draw.ellipse([(cx - 90, cy - 90), (cx + 90, cy + 90)], outline="#EEF2EE", width=2)

    # Timer at 00:00
    draw.text((cx - 58, cy - 22), "00:00", fill="#EEF2EE", font=get_font(42, bold=True))

    # Audio chime notification pill
    draw.rounded_rectangle([(cx - 130, cy + 115), (cx + 130, cy + 145)], radius=15, fill="#1F5A3D")
    draw.text((cx - 110, cy + 122), "🔔 Zen Bell Chime Ringing (528 Hz)", fill="#FFFFFF", font=get_font(12, bold=True))

    draw.text((cx - 160, cy + 160), "Time completed. Welcome back to the screen.", fill="#EEF2EE", font=get_font(16, bold=True))
    draw.text((cx - 120, cy + 190), "Tap 'I'm back' to record your reflection.", fill="#A9B6AD", font=get_font(14))

    # Cursor clicking "I'm back"
    draw.rounded_rectangle([(cx - 90, 500), (cx + 90, 552)], radius=12, fill="#1F5A3D")
    draw.text((cx - 30, 516), "I'm back", fill="#FFFFFF", font=get_font(15, bold=True))
    draw_cursor(draw, cx, 526)

    frames.append((img, 1800))

    # -------------------------------------------------------------
    # FRAME 6: Page 3 (Complete) - Reflection Card (+10 XP) (2.0s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#F6F7F4')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Mission", offline=True)

    # Left Column
    draw.text((64, 130), "MISSION COMPLETE", fill="#1F5A3D", font=get_font(12, bold=True))
    draw.text((64, 155), "Well done. 30 minutes\noutside.", fill="#14201A", font=get_font(34, bold=True))

    # 3 Stats between borders
    draw.line([(64, 260), (450, 260)], fill="#DDE2DC", width=1)
    draw.text((64, 275), "XP earned", fill="#4A564F", font=get_font(12))
    draw.text((64, 295), "+60", fill="#14201A", font=get_font(20, bold=True))

    draw.text((200, 275), "Level", fill="#4A564F", font=get_font(12))
    draw.text((200, 295), "3", fill="#14201A", font=get_font(20, bold=True))

    draw.text((320, 275), "Streak", fill="#4A564F", font=get_font(12))
    draw.text((320, 295), "4 days", fill="#14201A", font=get_font(20, bold=True))
    draw.line([(64, 335), (450, 335)], fill="#DDE2DC", width=1)

    # Right Card: Reflection
    draw.rounded_rectangle([(520, 120), (896, 500)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((545, 145), "How was it? (optional, +10 XP)", fill="#14201A", font=get_font(14, bold=True))

    draw.rounded_rectangle([(545, 175), (870, 340)], radius=12, fill="#FFFFFF", outline="#CFD6D0", width=1)
    sample_ref = "The bark was deeper than I expected, and a bird\nkept landing on one branch. The crisp morning\nlight was invigorating."
    draw.text((560, 190), sample_ref, fill="#14201A", font=get_font(13))

    # Action Buttons
    draw.rounded_rectangle([(545, 365), (740, 417)], radius=12, fill="#1F5A3D")
    draw.text((570, 381), "Save reflection", fill="#FFFFFF", font=get_font(14, bold=True))

    draw.text((765, 381), "Next mission", fill="#1F5A3D", font=get_font(14, bold=True))
    draw_cursor(draw, 640, 390)

    frames.append((img, 2000))

    # -------------------------------------------------------------
    # FRAME 7: Page 4 (Journey Dashboard & Activity Row) (2.0s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#F6F7F4')
    draw = ImageDraw.Draw(img)
    draw_header(draw, active_tab="Journey", offline=False)

    draw.text((64, 85), "JOURNEY", fill="#1F5A3D", font=get_font(12, bold=True))
    draw.text((64, 105), "Your time outside.", fill="#14201A", font=get_font(30, bold=True))
    draw.text((64, 142), "Every minute spent away from the screen adds to your real-world progress.", fill="#4A564F", font=get_font(13))

    # 3 Stat Cards
    draw.rounded_rectangle([(64, 175), (280, 245)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((80, 190), "Total missions", fill="#4A564F", font=get_font(11))
    draw.text((80, 208), "3", fill="#14201A", font=get_font(22, bold=True))

    draw.rounded_rectangle([(300, 175), (516, 245)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((316, 190), "Time outdoors", fill="#4A564F", font=get_font(11))
    draw.text((316, 208), "55 min", fill="#14201A", font=get_font(22, bold=True))

    draw.rounded_rectangle([(536, 175), (752, 245)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((552, 190), "Current streak", fill="#4A564F", font=get_font(11))
    draw.text((552, 208), "4 days", fill="#14201A", font=get_font(22, bold=True))

    # 7-Day Activity Row
    draw.rounded_rectangle([(64, 260), (752, 335)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((80, 275), "7-DAY ACTIVITY", fill="#4A564F", font=get_font(11, bold=True))

    days = [("Mon", True), ("Tue", True), ("Wed", True), ("Thu", True), ("Fri", False), ("Sat", False), ("Sun", False)]
    dx = 280
    for day, done in days:
        draw.text((dx, 273), day, fill="#4A564F", font=get_font(11))
        circle_color = "#1F5A3D" if done else "#FFFFFF"
        circle_border = "#1F5A3D" if done else "#DDE2DC"
        draw.ellipse([(dx + 2, 292), (dx + 24, 314)], fill=circle_color, outline=circle_border, width=1)
        if done:
            draw.text((dx + 8, 296), "✓", fill="#FFFFFF", font=get_font(10, bold=True))
        dx += 65

    # Reflections Diary
    draw.text((64, 355), "Recent outdoor reflections", fill="#14201A", font=get_font(16, bold=True))
    draw.rounded_rectangle([(64, 380), (752, 455)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
    draw.text((80, 395), "Find a tree and spend two minutes looking at it.", fill="#1F5A3D", font=get_font(12, bold=True))
    draw.text((550, 395), "Oct 6, 2026 • 30 min • +70 XP", fill="#4A564F", font=get_font(11))
    draw.text((80, 418), '"The bark was deeper than I expected, and a bird kept landing on one branch."', fill="#14201A", font=get_font(12))

    draw.rounded_rectangle([(64, 480), (220, 528)], radius=12, fill="#1F5A3D")
    draw.text((95, 496), "Back to mission", fill="#FFFFFF", font=get_font(14, bold=True))

    frames.append((img, 2000))

    # -------------------------------------------------------------
    # FRAME 8: Hackathon Victory Summary / Pitch Card (2.2s)
    # -------------------------------------------------------------
    img = Image.new('RGB', (960, 600), color='#16211B')
    draw = ImageDraw.Draw(img)

    draw.text((80, 100), "HACKTOBERFEST 2026: TOUCH GRASS", fill="#1F5A3D", font=get_font(13, bold=True))
    draw.text((80, 130), "TouchGrass Hackathon Winning Architecture", fill="#EEF2EE", font=get_font(32, bold=True))

    # 4 Prize Category Cards
    categories = [
        ("Grand Prize ($250)", "Open-Weight Gemma 2 Orchestrator", "Reverses digital screen retention into real physical action."),
        ("Best Use of TabPFN ($200)", "Prior Labs Tabular Foundation Model", "Microclimate forecasting for optimal 15m outdoor window & vitality."),
        ("Best Use of ElevenLabs ($200)", "Voice Mission Narration", "Spoken mission audio enables screen-free immersion from minute one."),
        ("Best Use of Sentry ($200)", "Deep Agent Observability", "Instrumented spans for reasoning, policy checks & tabular inference.")
    ]

    gy = 200
    for title, tech, desc in categories:
        draw.rounded_rectangle([(80, gy), (880, gy + 55)], radius=10, fill="#1F2E25", outline="#3A4A41", width=1)
        draw.text((100, gy + 10), title, fill="#EEF2EE", font=get_font(14, bold=True))
        draw.text((340, gy + 10), tech, fill="#10B981", font=get_font(13, bold=True))
        draw.text((100, gy + 32), desc, fill="#A9B6AD", font=get_font(12))
        gy += 68

    draw.text((80, 500), "Real life > Screen time. Open-source under MIT License.", fill="#EEF2EE", font=get_font(15, bold=True))
    draw.text((80, 525), "Live at http://localhost:8000 • Codebase: react + tailwind + fastapi + tabpfn + gemma", fill="#A9B6AD", font=get_font(12))

    frames.append((img, 2200))

    # Save animated GIF
    gif_path = "/Users/rajanmishra/Desktop/hack2/touchgrass_demo.gif"
    images = [f[0] for f in frames]
    durations = [f[1] for f in frames]

    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Animated demo video GIF created successfully at: {gif_path}")
    print(f"Total scenes: {len(frames)}, Total duration: {sum(durations)/1000:.1f}s")

if __name__ == "__main__":
    create_frames()
