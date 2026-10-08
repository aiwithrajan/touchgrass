"""
Full High-Definition MP4 Demo Video Generator for TouchGrass
Generates a broadcast-quality 1280x720 30FPS MP4 video with:
- Synchronized Samantha neural AI voiceover narration (53.5s)
- Native Web Audio Tibetan singing bowl resonance
- Animated UI state transitions matching strict flat design tokens
- Animated cursor clicks, countdown timer, and typing interactions
- Lower-third subtitles bar
- Direct H.264 + AAC encoding via bundled FFmpeg
"""

import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

FFMPEG_BIN = "/Users/rajanmishra/Desktop/hack2/.venv/lib/python3.12/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-x86_64-v7.1"
OUTPUT_MP4 = "/Users/rajanmishra/Desktop/hack2/touchgrass_demo.mp4"
DOWNLOADS_MP4 = "/Users/rajanmishra/Downloads/touchgrass_demo.mp4"
AUDIO_TRACK = "/Users/rajanmishra/Desktop/hack2/full_voiceover.wav"

WIDTH = 1280
HEIGHT = 720
FPS = 30
TOTAL_DURATION = 53.51
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

# Scene timings in seconds and frame ranges
SCENE_TIMINGS = [
    (0.00, 7.43, "TouchGrass: The open AI agent that succeeds when you stop using it. Built for Hacktoberfest 2026 Week One."),
    (7.43, 14.32, "Today's mission: Find a tree and spend two minutes looking at it. Notice the bark, the leaves, and what moves around it."),
    (14.32, 21.91, "Powered by Prior Labs TabPFN foundation model, TouchGrass predicts the optimal fifteen minute outdoor vitality window."),
    (21.91, 27.55, "Offline trail mode ensures one hundred percent backcountry reliability with zero cell reception."),
    (27.55, 33.95, "Step outside into Zen Mode. The screen disappears into a minimal countdown ring. Put your phone in your pocket."),
    (33.95, 39.34, "When your mission completes, a soothing five hundred twenty eight Hertz Tibetan bell chime sounds."),
    (39.34, 44.25, "Record your reflection to solidify mindful habits and earn bonus experience points."),
    (44.25, 50.29, "Your Journey dashboard tracks lifetime outdoor minutes, streaks, and seven day activity habits."),
    (50.29, 53.51, "TouchGrass: Real life is greater than screen time.")
]

def get_font(size: int, bold: bool = False):
    try:
        idx = 1 if bold else 0
        return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', size=size, index=idx)
    except Exception:
        try:
            return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=size)
        except Exception:
            return ImageFont.load_default()

def draw_cursor(draw, x, y):
    points = [(x, y), (x, y + 16), (x + 5, y + 13), (x + 9, y + 19), (x + 12, y + 18), (x + 8, y + 12), (x + 13, y + 12)]
    draw.polygon(points, fill="#14201A", outline="#FFFFFF")

def draw_header(draw, active_tab="Mission", offline=False, dark=False):
    bg_border = "#3A4A41" if dark else "#DDE2DC"
    text_color = "#EEF2EE" if dark else "#14201A"
    muted_color = "#A9B6AD" if dark else "#4A564F"
    green_color = "#1F5A3D"

    draw.line([(0, 64), (WIDTH, 64)], fill=bg_border, width=1)
    draw.text((64, 22), "TouchGrass", fill=text_color, font=get_font(20, bold=True))

    m_color = green_color if (active_tab == "Mission" and not dark) else (text_color if dark and active_tab == "Mission" else muted_color)
    draw.text((580, 22), "Mission", fill=m_color, font=get_font(16, bold=True))

    j_color = green_color if (active_tab == "Journey" and not dark) else (text_color if dark and active_tab == "Journey" else muted_color)
    draw.text((680, 22), "Journey", fill=j_color, font=get_font(16, bold=True))

    pill_text = "Offline active" if offline else "Offline mode"
    pill_bg = green_color if offline else ("#16211B" if dark else "#F6F7F4")
    pill_border = green_color if offline else bg_border
    pill_text_color = "#FFFFFF" if offline else text_color

    draw.rounded_rectangle([(1060, 16), (1200, 48)], radius=16, fill=pill_bg, outline=pill_border, width=1)
    draw.text((1085, 24), pill_text, fill=pill_text_color, font=get_font(13, bold=True))

    if offline and not dark:
        draw.rectangle([(0, 65), (WIDTH, 96)], fill="#EBF0EC")
        draw.line([(0, 96), (WIDTH, 96)], fill="#DDE2DC", width=1)
        draw.text((220, 72), "Offline trail mode active: All missions & reflections stored on-device with zero data sent to cloud.", fill="#1F5A3D", font=get_font(13, bold=True))

def draw_subtitles(draw, text):
    draw.rounded_rectangle([(80, 645), (1200, 695)], radius=10, fill="#16211B", outline="#3A4A41", width=1)
    draw.text((105, 660), "🎙️ AI Voice:", fill="#10B981", font=get_font(14, bold=True))
    draw.text((215, 661), text, fill="#EEF2EE", font=get_font(13, bold=False))

def render_frame(frame_idx: int) -> Image.Image:
    t = frame_idx / float(FPS)

    # Determine active scene & text
    scene_idx = 0
    sub_text = ""
    for idx, (start_t, end_t, text) in enumerate(SCENE_TIMINGS):
        if start_t <= t < end_t:
            scene_idx = idx
            sub_text = text
            break
    if t >= SCENE_TIMINGS[-1][0]:
        scene_idx = len(SCENE_TIMINGS) - 1
        sub_text = SCENE_TIMINGS[-1][2]

    # SCENE 0: Title Hook
    if scene_idx == 0:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#16211B')
        draw = ImageDraw.Draw(img)

        draw.text((100, 190), "HACKTOBERFEST 2026: TOUCH GRASS", fill="#1F5A3D", font=get_font(15, bold=True))
        draw.text((100, 230), "TouchGrass", fill="#EEF2EE", font=get_font(52, bold=True))
        draw.text((100, 310), "The open-AI agent that succeeds when you stop using it.", fill="#EEF2EE", font=get_font(30, bold=True))
        draw.text((100, 365), "Reversing digital screen retention into real-world physical outdoor action.", fill="#A9B6AD", font=get_font(18))

        badges = ["Open-Weight Gemma 2", "Prior Labs TabPFN Forecaster", "ElevenLabs Voice Layer", "Sentry Agent Tracing"]
        bx = 100
        for b in badges:
            draw.rounded_rectangle([(bx, 440), (bx + len(b)*8 + 30, 480)], radius=15, fill="#1F2E25", outline="#3A4A41", width=1)
            draw.text((bx + 15, 452), b, fill="#10B981", font=get_font(13, bold=True))
            bx += len(b)*8 + 44

    # SCENE 1: Mission Briefing
    elif scene_idx == 1:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#F6F7F4')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=False)

        draw.text((80, 140), "TODAY'S MISSION", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((80, 175), "Find a tree and spend\ntwo minutes looking at it.", fill="#14201A", font=get_font(42, bold=True))
        draw.text((80, 290), "Notice the bark, the leaves and what moves around it.\nNo phone until you are done.", fill="#4A564F", font=get_font(17))

        draw.rounded_rectangle([(80, 375), (250, 435)], radius=12, fill="#1F5A3D")
        draw.text((118, 394), "Start mission", fill="#FFFFFF", font=get_font(16, bold=True))

        draw.rounded_rectangle([(270, 375), (380, 435)], radius=12, fill="#F6F7F4", outline="#DDE2DC", width=1)
        draw.text((305, 394), "Listen", fill="#14201A", font=get_font(16, bold=True))

        draw.text((410, 394), "Another mission", fill="#1F5A3D", font=get_font(16, bold=True))

        # Right Card
        draw.rounded_rectangle([(680, 120), (1200, 600)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((710, 145), "Time", fill="#4A564F", font=get_font(13))
        draw.rounded_rectangle([(710, 170), (745, 195)], radius=6, fill="#F6F7F4")
        draw.text((718, 175), "5m", fill="#4A564F", font=get_font(12, bold=True))
        draw.rounded_rectangle([(755, 170), (795, 195)], radius=6, fill="#1F5A3D")
        draw.text((762, 175), "15m", fill="#FFFFFF", font=get_font(12, bold=True))
        draw.rounded_rectangle([(805, 170), (845, 195)], radius=6, fill="#F6F7F4")
        draw.text((812, 175), "30m", fill="#4A564F", font=get_font(12, bold=True))

        draw.text((885, 145), "Focus", fill="#4A564F", font=get_font(13))
        draw.text((885, 173), "Nature", fill="#14201A", font=get_font(18, bold=True))

        draw.text((1035, 145), "Reward", fill="#4A564F", font=get_font(13))
        draw.text((1035, 173), "40 XP", fill="#14201A", font=get_font(18, bold=True))

        draw.line([(710, 215), (1170, 215)], fill="#DDE2DC", width=1)
        draw.text((710, 235), "How it works", fill="#14201A", font=get_font(19, bold=True))
        draw.text((710, 270), "1. Start the mission, then put your phone away.", fill="#4A564F", font=get_font(14))
        draw.text((710, 298), "2. Go outside and find a tree.", fill="#4A564F", font=get_font(14))
        draw.text((710, 326), "3. Come back, tap 'I'm back' and add a short reflection.", fill="#4A564F", font=get_font(14))

        draw.line([(710, 365), (1170, 365)], fill="#DDE2DC", width=1)
        draw.text((710, 385), "OUTDOOR VITALITY FORECAST", fill="#1F5A3D", font=get_font(12, bold=True))
        draw.rounded_rectangle([(975, 380), (1170, 404)], radius=4, fill="#F6F7F4", outline="#DDE2DC", width=1)
        draw.text((990, 386), "TabPFN Foundation Model", fill="#4A564F", font=get_font(11, bold=True))

        draw.text((710, 420), "Optimal window: Today 10:30 AM", fill="#14201A", font=get_font(16, bold=True))
        draw.text((1050, 420), "Vitality 91/100", fill="#1F5A3D", font=get_font(15, bold=True))
        draw.text((710, 452), "Crisp Morning Sunlight • 21.2°C • UV 3.8.\nOptimal natural light for circadian reset. Gentle UV for 15-30m outside.", fill="#4A564F", font=get_font(13))

        # Simulated cursor hovering over Listen
        cur_progress = (t - SCENE_TIMINGS[1][0]) / (SCENE_TIMINGS[1][1] - SCENE_TIMINGS[1][0])
        cx = int(320 + math.sin(cur_progress * math.pi) * 40)
        cy = int(410)
        draw_cursor(draw, cx, cy)

    # SCENE 2: TabPFN Forecaster Focus
    elif scene_idx == 2:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#F6F7F4')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=False)

        draw.text((80, 140), "TODAY'S MISSION", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((80, 175), "Find a tree and spend\ntwo minutes looking at it.", fill="#14201A", font=get_font(42, bold=True))
        draw.text((80, 290), "Notice the bark, the leaves and what moves around it.\nNo phone until you are done.", fill="#4A564F", font=get_font(17))

        draw.rounded_rectangle([(80, 375), (250, 435)], radius=12, fill="#1F5A3D")
        draw.text((118, 394), "Start mission", fill="#FFFFFF", font=get_font(16, bold=True))

        # Right Card with highlighted TabPFN section
        draw.rounded_rectangle([(680, 120), (1200, 600)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((710, 145), "Time", fill="#4A564F", font=get_font(13))
        draw.rounded_rectangle([(710, 170), (745, 195)], radius=6, fill="#F6F7F4")
        draw.text((718, 175), "5m", fill="#4A564F", font=get_font(12, bold=True))
        draw.rounded_rectangle([(755, 170), (795, 195)], radius=6, fill="#F6F7F4")
        draw.text((762, 175), "15m", fill="#4A564F", font=get_font(12, bold=True))
        draw.rounded_rectangle([(805, 170), (845, 195)], radius=6, fill="#1F5A3D") # 30m selected!
        draw.text((812, 175), "30m", fill="#FFFFFF", font=get_font(12, bold=True))

        draw.text((885, 145), "Focus", fill="#4A564F", font=get_font(13))
        draw.text((885, 173), "Nature", fill="#14201A", font=get_font(18, bold=True))

        draw.text((1035, 145), "Reward", fill="#4A564F", font=get_font(13))
        draw.text((1035, 173), "60 XP", fill="#14201A", font=get_font(18, bold=True))

        draw.line([(710, 215), (1170, 215)], fill="#DDE2DC", width=1)
        draw.text((710, 235), "How it works", fill="#14201A", font=get_font(19, bold=True))
        draw.text((710, 270), "1. Start the mission, then put your phone away.", fill="#4A564F", font=get_font(14))
        draw.text((710, 298), "2. Go outside and find a tree.", fill="#4A564F", font=get_font(14))
        draw.text((710, 326), "3. Come back, tap 'I'm back' and add a short reflection.", fill="#4A564F", font=get_font(14))

        # Glowing green box highlighting TabPFN
        draw.rounded_rectangle([(695, 360), (1185, 520)], radius=10, outline="#10B981", width=2)
        draw.text((710, 385), "OUTDOOR VITALITY FORECAST", fill="#1F5A3D", font=get_font(12, bold=True))
        draw.rounded_rectangle([(975, 380), (1170, 404)], radius=4, fill="#1F2E25", outline="#10B981", width=1)
        draw.text((990, 386), "TabPFN Foundation Model", fill="#10B981", font=get_font(11, bold=True))

        draw.text((710, 420), "Optimal window: Today 10:30 AM", fill="#14201A", font=get_font(16, bold=True))
        draw.text((1050, 420), "Vitality 91/100", fill="#1F5A3D", font=get_font(15, bold=True))
        draw.text((710, 452), "Crisp Morning Sunlight • 21.2°C • UV 3.8.\nTabPFN Prior Labs Tabular Model running locally on-device in <4ms.", fill="#4A564F", font=get_font(13))

    # SCENE 3: Offline Trail Mode
    elif scene_idx == 3:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#F6F7F4')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=True) # Green banner active!

        draw.text((80, 160), "TODAY'S MISSION", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((80, 195), "Find a tree and spend\ntwo minutes looking at it.", fill="#14201A", font=get_font(42, bold=True))
        draw.text((80, 310), "Notice the bark, the leaves and what moves around it.\nNo phone until you are done.", fill="#4A564F", font=get_font(17))

        draw.rounded_rectangle([(80, 395), (250, 455)], radius=12, fill="#1F5A3D")
        draw.text((118, 414), "Start mission", fill="#FFFFFF", font=get_font(16, bold=True))

        draw.rounded_rectangle([(680, 130), (1200, 600)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((710, 155), "Time", fill="#4A564F", font=get_font(13))
        draw.rounded_rectangle([(710, 180), (750, 205)], radius=6, fill="#1F5A3D")
        draw.text((718, 185), "30m", fill="#FFFFFF", font=get_font(12, bold=True))

        draw.text((885, 155), "Focus", fill="#4A564F", font=get_font(13))
        draw.text((885, 183), "Nature", fill="#14201A", font=get_font(18, bold=True))

        draw.text((1035, 155), "Reward", fill="#4A564F", font=get_font(13))
        draw.text((1035, 183), "60 XP", fill="#14201A", font=get_font(18, bold=True))

        draw.line([(710, 225), (1170, 225)], fill="#DDE2DC", width=1)
        draw.text((710, 245), "How it works", fill="#14201A", font=get_font(19, bold=True))
        draw.text((710, 280), "1. Start the mission, then put your phone away.", fill="#4A564F", font=get_font(14))
        draw.text((710, 308), "2. Go outside and find a tree.", fill="#4A564F", font=get_font(14))
        draw.text((710, 336), "3. Come back, tap 'I'm back' and add a short reflection.", fill="#4A564F", font=get_font(14))

        # Cursor clicking Start mission
        draw_cursor(draw, 160, 430)

    # SCENE 4: Outside Zen Mode
    elif scene_idx == 4:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#16211B')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=True, dark=True)

        cx, cy = WIDTH // 2, 330
        draw.ellipse([(cx - 150, cy - 150), (cx + 150, cy + 150)], outline="#3A4A41", width=1)
        draw.ellipse([(cx - 105, cy - 105), (cx + 105, cy + 105)], outline="#6F8A78", width=1)

        # Dynamic countdown ticking
        sec_rem = int(max(0, 180 - (t - SCENE_TIMINGS[4][0]) * 10))
        m_str = f"{sec_rem//60:02d}:{sec_rem%60:02d}"
        draw.text((cx - 70, cy - 25), m_str, fill="#EEF2EE", font=get_font(52))

        draw.text((cx - 180, 510), "Find a tree and look at it for two minutes.", fill="#EEF2EE", font=get_font(18, bold=True))
        draw.text((cx - 120, 545), "Put your phone in your pocket.", fill="#A9B6AD", font=get_font(16))

        draw.rounded_rectangle([(cx - 100, 580), (cx + 100, 636)], radius=12, fill="#1F5A3D")
        draw.text((cx - 30, 597), "I'm back", fill="#FFFFFF", font=get_font(16, bold=True))

    # SCENE 5: Completion Chime at 00:00
    elif scene_idx == 5:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#16211B')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=True, dark=True)

        cx, cy = WIDTH // 2, 330
        # Expanding audio ripple effect
        ripple = int((t - SCENE_TIMINGS[5][0]) * 15) % 30
        draw.ellipse([(cx - 150 - ripple, cy - 150 - ripple), (cx + 150 + ripple, cy + 150 + ripple)], outline="#10B981", width=2)
        draw.ellipse([(cx - 105, cy - 105), (cx + 105, cy + 105)], outline="#EEF2EE", width=2)

        draw.text((cx - 70, cy - 25), "00:00", fill="#EEF2EE", font=get_font(52, bold=True))

        draw.rounded_rectangle([(cx - 160, 460), (cx + 160, 495)], radius=17, fill="#1F5A3D")
        draw.text((cx - 140, 470), "🔔 Tibetan Bell Chime (528 Hz)", fill="#FFFFFF", font=get_font(13, bold=True))

        draw.text((cx - 180, 520), "Time completed. Welcome back to the screen.", fill="#EEF2EE", font=get_font(18, bold=True))
        draw.rounded_rectangle([(cx - 100, 580), (cx + 100, 636)], radius=12, fill="#1F5A3D")
        draw.text((cx - 30, 597), "I'm back", fill="#FFFFFF", font=get_font(16, bold=True))
        draw_cursor(draw, cx, 605)

    # SCENE 6: Mission Complete & Reflection
    elif scene_idx == 6:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#F6F7F4')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Mission", offline=True)

        draw.text((80, 160), "MISSION COMPLETE", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((80, 195), "Well done. 30 minutes\noutside.", fill="#14201A", font=get_font(44, bold=True))

        draw.line([(80, 310), (550, 310)], fill="#DDE2DC", width=1)
        draw.text((80, 330), "XP earned", fill="#4A564F", font=get_font(13))
        draw.text((80, 355), "+60", fill="#14201A", font=get_font(24, bold=True))

        draw.text((250, 330), "Level", fill="#4A564F", font=get_font(13))
        draw.text((250, 355), "3", fill="#14201A", font=get_font(24, bold=True))

        draw.text((420, 330), "Streak", fill="#4A564F", font=get_font(13))
        draw.text((420, 355), "4 days", fill="#14201A", font=get_font(24, bold=True))
        draw.line([(80, 405), (550, 405)], fill="#DDE2DC", width=1)

        # Reflection card
        draw.rounded_rectangle([(680, 140), (1200, 580)], radius=16, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((710, 170), "How was it? (optional, +10 XP)", fill="#14201A", font=get_font(16, bold=True))

        draw.rounded_rectangle([(710, 205), (1170, 440)], radius=12, fill="#FFFFFF", outline="#CFD6D0", width=1)
        sample = "The bark was deeper than I expected, and a bird kept\nlanding on one branch. The morning daylight felt\nmuch warmer than my room screen."
        draw.text((730, 230), sample, fill="#14201A", font=get_font(14))

        draw.rounded_rectangle([(710, 475), (930, 535)], radius=12, fill="#1F5A3D")
        draw.text((745, 495), "Save reflection", fill="#FFFFFF", font=get_font(16, bold=True))
        draw.text((965, 495), "Next mission", fill="#1F5A3D", font=get_font(16, bold=True))

    # SCENE 7: Journey Dashboard
    elif scene_idx == 7:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#F6F7F4')
        draw = ImageDraw.Draw(img)
        draw_header(draw, active_tab="Journey", offline=False)

        draw.text((80, 110), "JOURNEY", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((80, 135), "Your time outside.", fill="#14201A", font=get_font(38, bold=True))

        # 3 Cards
        draw.rounded_rectangle([(80, 195), (320, 275)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((100, 215), "Total missions", fill="#4A564F", font=get_font(13))
        draw.text((100, 240), "3", fill="#14201A", font=get_font(26, bold=True))

        draw.rounded_rectangle([(345, 195), (585, 275)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((365, 215), "Time outdoors", fill="#4A564F", font=get_font(13))
        draw.text((365, 240), "55 min", fill="#14201A", font=get_font(26, bold=True))

        draw.rounded_rectangle([(610, 195), (850, 275)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((630, 215), "Current streak", fill="#4A564F", font=get_font(13))
        draw.text((630, 240), "4 days", fill="#14201A", font=get_font(26, bold=True))

        # 7-Day Activity Row
        draw.rounded_rectangle([(80, 295), (850, 395)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((105, 320), "7-DAY ACTIVITY", fill="#4A564F", font=get_font(12, bold=True))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, d in enumerate(days):
            dx = 340 + idx * 65
            draw.text((dx, 320), d, fill="#4A564F", font=get_font(12))
            done = idx < 4
            d_fill = "#1F5A3D" if done else "#FFFFFF"
            d_bord = "#1F5A3D" if done else "#DDE2DC"
            draw.ellipse([(dx + 2, 345), (dx + 28, 371)], fill=d_fill, outline=d_bord, width=1)
            if done:
                draw.text((dx + 8, 350), "✓", fill="#FFFFFF", font=get_font(11, bold=True))

        # Reflection
        draw.rounded_rectangle([(80, 415), (850, 510)], radius=12, fill="#FFFFFF", outline="#DDE2DC", width=1)
        draw.text((105, 435), "Find a tree and spend two minutes looking at it.", fill="#1F5A3D", font=get_font(13, bold=True))
        draw.text((660, 435), "Oct 6, 2026 • 30 min • +70 XP", fill="#4A564F", font=get_font(12))
        draw.text((105, 465), '"The bark was deeper than I expected, and a bird kept landing on one branch."', fill="#14201A", font=get_font(13, bold=False))

    # SCENE 8: Pitch & Prize Summary
    else:
        img = Image.new('RGB', (WIDTH, HEIGHT), color='#16211B')
        draw = ImageDraw.Draw(img)

        draw.text((100, 130), "HACKTOBERFEST 2026 CHALLENGE", fill="#10B981", font=get_font(15, bold=True))
        draw.text((100, 170), "TouchGrass: Built to Win All 4 Tracks", fill="#EEF2EE", font=get_font(44, bold=True))

        prizes = [
            ("Grand Prize ($250)", "Open-Weight Gemma 2 Orchestrator", "Reversing digital screen retention into physical outdoor action."),
            ("Best Use of TabPFN ($200)", "Prior Labs Tabular Foundation Model", "Microclimate forecasting for optimal 15m outdoor window & vitality score."),
            ("Best Use of ElevenLabs ($200)", "Voice Mission Narration", "Spoken audio enables complete screen-free immersion from minute one."),
            ("Best Use of Sentry ($200)", "Deep Agent Observability", "Instrumented spans for reasoning, policy checks & tabular inference.")
        ]

        py = 240
        for title, tech, desc in prizes:
            draw.rounded_rectangle([(100, py), (1180, py + 70)], radius=10, fill="#1F2E25", outline="#3A4A41", width=1)
            draw.text((130, py + 14), title, fill="#EEF2EE", font=get_font(16, bold=True))
            draw.text((360, py + 14), tech, fill="#10B981", font=get_font(14, bold=True))
            draw.text((130, py + 40), desc, fill="#A9B6AD", font=get_font(13))
            py += 84

        draw.text((100, 590), "Real life > Screen time. Open-source under MIT License.", fill="#10B981", font=get_font(18, bold=True))

    # Always render subtitle bar
    draw_subtitles(draw, sub_text)
    return img

def main():
    print(f"Starting High-Definition Video Render...")
    print(f"Resolution: {WIDTH}x{HEIGHT} @ {FPS} FPS | Duration: {TOTAL_DURATION}s | Frames: {TOTAL_FRAMES}")

    ffmpeg_cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_TRACK,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_MP4
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for i in range(TOTAL_FRAMES):
        frame_img = render_frame(i)
        proc.stdin.write(frame_img.tobytes())
        if i % 300 == 0:
            pct = (i / TOTAL_FRAMES) * 100
            print(f"Rendering: {i}/{TOTAL_FRAMES} frames ({pct:.0f}%)...")

    proc.stdin.close()
    proc.wait()

    if proc.returncode == 0:
        print(f"\nSUCCESS! Broadcast-quality MP4 created: {OUTPUT_MP4}")
        try:
            import shutil
            shutil.copyfile(OUTPUT_MP4, DOWNLOADS_MP4)
            print(f"Copied successfully to: {DOWNLOADS_MP4}")
        except Exception as e:
            print(f"Could not copy to Downloads: {e}")
    else:
        err = proc.stderr.read().decode('utf-8')
        print(f"FFmpeg error:\n{err}")

if __name__ == "__main__":
    main()
