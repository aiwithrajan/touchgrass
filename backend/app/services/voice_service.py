import base64
import httpx
from typing import Dict, Any, Optional
from backend.app.config import settings

class VoiceService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID

    async def generate_speech(self, text: str) -> Dict[str, Any]:
        """
        Generates spoken audio for the challenge.
        If ElevenLabs API key is active, calls ElevenLabs.
        Otherwise provides structured metadata for browser Web Speech API offline synthesis.
        """
        if self.api_key and not settings.OFFLINE_MODE:
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.api_key
                }
                data = {
                    "text": text,
                    "model_id": "eleven_turbo_v2",
                    "voice_settings": {
                        "stability": 0.55,
                        "similarity_boost": 0.75
                    }
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, json=data, headers=headers)
                    if response.status_code == 200:
                        audio_base64 = base64.b64encode(response.content).decode("utf-8")
                        return {
                            "provider": "elevenlabs",
                            "audio_base64": f"data:audio/mpeg;base64,{audio_base64}",
                            "text": text
                        }
                    else:
                        print(f"[VoiceService] ElevenLabs error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"[VoiceService] ElevenLabs exception: {e}")

        # Fallback to Browser Speech Synthesis (zero dependency & 100% offline trail compatible)
        return {
            "provider": "web_speech_fallback",
            "audio_base64": None,
            "text": text
        }

voice_service = VoiceService()
