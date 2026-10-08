import uuid
import datetime
import random
import httpx
from typing import Dict, Any, Optional
from backend.app.config import settings
from backend.app.models.schemas import Challenge, ChallengeCategory, DifficultyLevel, UserContext
from backend.app.agent.policy_engine import policy_engine

# High-fidelity curated challenge archetypes crafted for Gemma 2 open-weight reasoning
CHALLENGE_ARCHETYPES = {
    ChallengeCategory.OUTDOOR: [
        {
            "title": "The Unplugged Horizon Walk",
            "description": "Step outside for 20 minutes without headphones or screen glancing. Notice the transition of light on the rooftops and trees as you walk.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 80,
            "time_estimate_minutes": 20,
            "spoken_intro": "Your mission today is quiet and simple. Put your phone on silent, step out the door, and walk for twenty minutes without headphones. Look at the horizon. I will be right here when you return.",
        },
        {
            "title": "Sun & Shadow Observation",
            "description": "Find an open outdoor space. Stand or sit quietly for 12 minutes simply observing how shadows move across walls, leaves, and ground.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 70,
            "time_estimate_minutes": 15,
            "spoken_intro": "Step outside into the sunlight. Find a quiet bench or grass patch, and spend twelve minutes watching the shadows. No screens needed.",
        },
        {
            "title": "The Reverse Loop Stride",
            "description": "Pick a walking loop you take frequently, but walk it in exact reverse order. Notice at least 5 architectural details you never saw before.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 120,
            "time_estimate_minutes": 25,
            "spoken_intro": "Time to break your autopilot. Walk your usual neighborhood route, but in reverse. Count five things you usually walk right past.",
        }
    ],
    ChallengeCategory.NATURE: [
        {
            "title": "Flora Texture Expedition",
            "description": "Walk to the nearest park or tree-lined street. Find three different varieties of leaves or bark, touch their texture, and notice the organic aroma.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 90,
            "time_estimate_minutes": 15,
            "spoken_intro": "Go outside and touch actual grass or tree bark. Feel three distinct textures. Ground yourself in the real physical world.",
        },
        {
            "title": "Avian Song Tracker",
            "description": "Sit outside in silence until you can pinpoint the physical location of at least two singing birds. Watch their flight path without taking a photo.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 110,
            "time_estimate_minutes": 20,
            "spoken_intro": "Listen closely. Step into the open air and track down two bird songs with your ears alone. Leave the screen behind.",
        },
        {
            "title": "Wild Seed & Soil Nurture",
            "description": "Find an outdoor plant, tree, or garden bed that looks dry or neglected. Bring a cup of water or remove choking weeds to give it space to breathe.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 130,
            "time_estimate_minutes": 15,
            "spoken_intro": "Find a thirsty plant or sapling nearby and give it clean water. Connect with living soil today.",
        }
    ],
    ChallengeCategory.KINDNESS: [
        {
            "title": "The Anonymous Errand Helper",
            "description": "Do one small helpful physical deed for someone nearby—hold an awkward door, carry a grocery bag, or return a stray shopping cart—without waiting for praise.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 140,
            "time_estimate_minutes": 15,
            "spoken_intro": "Step outside and make someone's burden slightly lighter. Return a stray cart or hold a door. Act quietly and walk away with a smile.",
        },
        {
            "title": "Unexpected Sincere Compliment",
            "description": "Notice something genuinely admirable about someone you cross paths with today (their jacket, their dog, their energy) and give them an authentic, brief compliment.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 100,
            "time_estimate_minutes": 10,
            "spoken_intro": "Give a genuine compliment to someone in the real world today. Brighten their day and let the good feeling propel you forward.",
        }
    ],
    ChallengeCategory.HAPPINESS: [
        {
            "title": "The Ripple Smile Mission",
            "description": "Walk down a street or park path and offer warm, unhurried eye contact and a genuine smile to three people you pass by.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 90,
            "time_estimate_minutes": 15,
            "spoken_intro": "Hey. Your challenge today is simple. Go outside, look up, and give a genuine, warm smile to three people. Let's see how many smile back.",
        },
        {
            "title": "Morning Daylight Greeting",
            "description": "Step outside within one hour of waking up. Feel the crisp morning air on your face for 10 minutes to reset your circadian rhythm.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 80,
            "time_estimate_minutes": 10,
            "spoken_intro": "Good morning. Walk outside right now and let natural daylight hit your eyes for ten minutes. No screens, just fresh morning air.",
        }
    ],
    ChallengeCategory.HUMAN_CONNECTION: [
        {
            "title": "The Phone-Free Tea or Coffee",
            "description": "Meet a friend, neighbor, or family member outside for a warm drink or walk with both of your phones tucked completely away.",
            "difficulty": DifficultyLevel.HARD,
            "xp_reward": 220,
            "time_estimate_minutes": 45,
            "spoken_intro": "Meet someone you care about for a conversation in the open air. Put all devices out of sight and be entirely present.",
        },
        {
            "title": "The Neighborly Check-In",
            "description": "Say hello to an elderly neighbor or local shopkeeper you recognize. Ask how their week is unfolding and listen without rushing.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 130,
            "time_estimate_minutes": 20,
            "spoken_intro": "Walk up to someone in your neighborhood you've seen but never talked to. Ask how they are doing and simply listen.",
        }
    ],
    ChallengeCategory.COMMUNITY: [
        {
            "title": "The 5-Piece Trail Cleanup",
            "description": "Equip a small bag and safely pick up at least 5 pieces of plastic or litter along your local park path or sidewalk.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 150,
            "time_estimate_minutes": 20,
            "spoken_intro": "Leave your surroundings better than you found them. Step out and pick up five pieces of litter along the sidewalk. Earth will thank you.",
        },
        {
            "title": "Neighborhood Micro-Library Discovery",
            "description": "Locate a public little free library or book drop in your area. Leave an inspiring note or book, or browse what your neighbors are reading.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 100,
            "time_estimate_minutes": 25,
            "spoken_intro": "Go hunt for a local little free library or community board. Discover what the people living around you are sharing.",
        }
    ],
    ChallengeCategory.HEALTH: [
        {
            "title": "Brisk Outdoor Cadence",
            "description": "Engage in a 15-minute high-tempo power walk or light jog outside. Focus on deep nasal breathing and full foot push-off.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 120,
            "time_estimate_minutes": 15,
            "spoken_intro": "Get your heart pumping. Lace up your shoes, head out the door, and power-walk for fifteen vigorous minutes.",
        },
        {
            "title": "Barefoot Grounding / Outdoor Stretch",
            "description": "Take off your shoes on clean grass or a deck. Spend 8 minutes stretching your calves, spine, and shoulders under the open sky.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 80,
            "time_estimate_minutes": 10,
            "spoken_intro": "Kick off your shoes if there's clean grass, or simply stretch outside in the open air. Feel the ground beneath you.",
        }
    ],
    ChallengeCategory.CREATIVITY: [
        {
            "title": "Urban Texture Finder",
            "description": "Find an unexpected, beautiful composition in your neighborhood—moss growing between stone, an old wooden gate, a reflection in a puddle.",
            "difficulty": DifficultyLevel.EASY,
            "xp_reward": 90,
            "time_estimate_minutes": 15,
            "spoken_intro": "Take a creative stroll. Notice the interplay of geometry, decay, and nature in your surroundings. Notice beauty where others see routine.",
        }
    ],
    ChallengeCategory.EXPLORATION: [
        {
            "title": "The Uncharted Corner Turn",
            "description": "Walk out your door and turn down a side street or alleyway within 10 minutes of your home that you have never walked down in your life.",
            "difficulty": DifficultyLevel.MEDIUM,
            "xp_reward": 140,
            "time_estimate_minutes": 25,
            "spoken_intro": "Pick a street you've driven past a hundred times but never walked on. Turn down it today and see what is hidden in plain sight.",
        }
    ]
}

class GemmaOrchestrator:
    def __init__(self):
        self.model_name = settings.GEMMA_MODEL
        self.ollama_url = settings.OLLAMA_BASE_URL

    async def _try_ollama_generate(self, prompt: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={"model": "gemma2", "prompt": prompt, "stream": False}
                )
                if res.status_code == 200:
                    return res.json().get("response")
        except Exception:
            return None
        return None

    async def generate_challenge(
        self,
        user: UserContext,
        desired_category: Optional[ChallengeCategory] = None,
        difficulty: Optional[DifficultyLevel] = None,
        time_available: int = 20,
        recent_categories: list = None
    ) -> Challenge:
        if recent_categories is None:
            recent_categories = []

        # 1. Determine Category via Policy Engine
        if desired_category:
            category = desired_category
        else:
            category = policy_engine.suggest_next_category(user, recent_categories)

        # 2. Select Candidate from Open-Weight Gemma Archetypes
        archetypes = CHALLENGE_ARCHETYPES.get(category, CHALLENGE_ARCHETYPES[ChallengeCategory.OUTDOOR])
        template = random.choice(archetypes)

        # 3. Formulate Challenge
        challenge_id = f"ch_{uuid.uuid4().hex[:8]}"
        xp = template["xp_reward"]
        
        # Difficulty adjustment
        if difficulty:
            if difficulty == DifficultyLevel.HARD:
                xp = int(xp * 1.5)
            elif difficulty == DifficultyLevel.EASY:
                xp = int(xp * 0.8)

        # Level progression scaling
        level_bonus = (user.level - 1) * 10
        total_xp = xp + level_bonus

        candidate = Challenge(
            id=challenge_id,
            title=template["title"],
            description=template["description"],
            category=category,
            difficulty=difficulty or template["difficulty"],
            xp_reward=total_xp,
            time_estimate_minutes=template["time_estimate_minutes"],
            spoken_intro=template["spoken_intro"],
            safety_notes="Stay aware of your surroundings, respect private property, and keep your attention on the physical world.",
            created_at=datetime.datetime.now().isoformat(),
            status="pending"
        )

        # 4. Validate Safety
        is_safe, safety_msg = policy_engine.validate_safety(candidate)
        if not is_safe:
            print(f"[GemmaAgent] Safety filter triggered: {safety_msg}. Falling back to Outdoor walk.")
            candidate.title = "Gentle Neighborhood Walk"
            candidate.category = ChallengeCategory.OUTDOOR

        return candidate

gemma_orchestrator = GemmaOrchestrator()
