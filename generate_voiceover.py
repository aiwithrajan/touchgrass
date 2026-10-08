"""
Generates AI Voiceover narration files for TouchGrass Demo Video
Uses macOS Samantha neural voice with afconvert to WAV.
"""

import os
import subprocess

SCENES = [
    {
        "id": "scene1_intro",
        "text": "TouchGrass: The open AI agent that succeeds when you stop using it. Built for Hacktoberfest 2026 Week One."
    },
    {
        "id": "scene2_mission",
        "text": "Today's mission: Find a tree and spend two minutes looking at it. Notice the bark, the leaves, and what moves around it."
    },
    {
        "id": "scene3_tabpfn",
        "text": "Powered by Prior Labs TabPFN foundation model, TouchGrass predicts the optimal fifteen minute outdoor vitality window."
    },
    {
        "id": "scene4_offline",
        "text": "Offline trail mode ensures one hundred percent backcountry reliability with zero cell reception."
    },
    {
        "id": "scene5_outside",
        "text": "Step outside into Zen Mode. The screen disappears into a minimal countdown ring. Put your phone in your pocket."
    },
    {
        "id": "scene6_chime",
        "text": "When your mission completes, a soothing five hundred twenty eight Hertz Tibetan bell chime sounds."
    },
    {
        "id": "scene7_reflection",
        "text": "Record your reflection to solidify mindful habits and earn bonus experience points."
    },
    {
        "id": "scene8_journey",
        "text": "Your Journey dashboard tracks lifetime outdoor minutes, streaks, and seven day activity habits."
    },
    {
        "id": "scene9_pitch",
        "text": "TouchGrass: Real life is greater than screen time."
    }
]

def generate_voiceover():
    audio_dir = "/Users/rajanmishra/Desktop/hack2/audio"
    os.makedirs(audio_dir, exist_ok=True)

    for item in SCENES:
        base_name = item["id"]
        m4a_path = os.path.join(audio_dir, f"{base_name}.m4a")
        wav_path = os.path.join(audio_dir, f"{base_name}.wav")
        text = item["text"]

        print(f"Generating voice for: {base_name}...")
        # Run say with Samantha voice
        cmd_say = ["/usr/bin/say", "-v", "Samantha", "-r", "175", "-o", m4a_path, text]
        subprocess.run(cmd_say, check=True)

        # Convert to WAV
        cmd_convert = ["/usr/bin/afconvert", "-f", "WAVE", "-d", "LEI16", m4a_path, wav_path]
        subprocess.run(cmd_convert, check=True)
        print(f"Saved: {wav_path}")

    print("\nAll AI voiceover files successfully created in audio/")

if __name__ == "__main__":
    generate_voiceover()
