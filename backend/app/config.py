import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "TouchGrass"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Storage / DB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    LOCAL_STORAGE_PATH: str = os.getenv("LOCAL_STORAGE_PATH", "backend/data/user_memory.json")
    
    # AI Providers
    GEMMA_MODEL: str = os.getenv("GEMMA_MODEL", "gemma-2-9b-it")
    GEMMA_API_KEY: str = os.getenv("GEMMA_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # ElevenLabs Voice API
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel / friendly voice
    
    # Sentry Observability
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    
    # Simulation / Offline flag
    OFFLINE_MODE: bool = os.getenv("OFFLINE_MODE", "false").lower() in ("true", "1")

settings = Settings()
