from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field

class ChallengeCategory(str, Enum):
    OUTDOOR = "Outdoor"
    NATURE = "Nature"
    KINDNESS = "Kindness"
    HAPPINESS = "Happiness"
    HUMAN_CONNECTION = "Human Connection"
    COMMUNITY = "Community"
    HEALTH = "Health"
    CREATIVITY = "Creativity"
    EXPLORATION = "Exploration"

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Challenge(BaseModel):
    id: str
    title: str
    description: str
    category: ChallengeCategory
    difficulty: DifficultyLevel
    xp_reward: int = Field(default=100)
    time_estimate_minutes: int = Field(default=15)
    spoken_intro: str
    safety_notes: str = "Stay alert to your surroundings. No trespassing or risky maneuvers."
    created_at: str
    status: str = "pending" # pending, accepted, completed, skipped

class UserContext(BaseModel):
    user_id: str = "guest_user"
    username: str = "Trailblazer"
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 150
    streak_days: int = 1
    completed_challenges_count: int = 0
    badges: List[str] = []
    unlocked_features: List[str] = []
    offline_mode: bool = False
    preferred_categories: List[ChallengeCategory] = []
    recent_categories: List[str] = []

class GenerateChallengeRequest(BaseModel):
    user_id: str = "guest_user"
    desired_category: Optional[ChallengeCategory] = None
    difficulty: Optional[DifficultyLevel] = None
    time_available_minutes: Optional[int] = 20
    offline_requested: bool = False

class ReflectionRequest(BaseModel):
    challenge_id: str
    reflection_text: str
    voice_audio_base64: Optional[str] = None
    minutes_spent: int = 15

class RewardResult(BaseModel):
    challenge_id: str
    base_xp: int
    bonus_xp: int
    total_xp_awarded: int
    previous_level: int
    new_level: int
    level_up: bool
    new_badges: List[str] = []
    unlocked_features: List[str] = []
    gemma_encouragement: str
    sincerity_score: float = 1.0

class SocialPost(BaseModel):
    id: str
    author_name: str
    author_level: int
    broad_location: str
    challenge_title: str
    category: str
    reflection: str
    time_ago: str
    kudos_count: int = 0
    verified: bool = True

class JourneyCard(BaseModel):
    username: str
    level: int
    total_challenges: int
    categories_breakdown: Dict[str, int]
    badges_earned: List[Dict[str, str]]
    notable_quotes: List[str]
    shareable_summary: str
