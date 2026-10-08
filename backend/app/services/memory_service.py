import json
import os
import datetime
from typing import Dict, Any, List, Optional
from backend.app.config import settings
from backend.app.models.schemas import UserContext, Challenge, RewardResult, SocialPost

class MemoryService:
    def __init__(self):
        self.local_file = settings.LOCAL_STORAGE_PATH
        self.mongo_client = None
        self.db = None
        self._init_mongo()
        self._init_local_store()

    def _init_mongo(self):
        if settings.MONGODB_URI and not settings.OFFLINE_MODE:
            try:
                from pymongo import MongoClient
                self.mongo_client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
                # verify connection
                self.mongo_client.admin.command('ping')
                self.db = self.mongo_client.touchgrass
                print("[MemoryService] Connected to MongoDB Atlas successfully.")
            except Exception as e:
                print(f"[MemoryService] MongoDB Atlas connection failed or offline ({e}). Using Local-First store.")
                self.mongo_client = None
                self.db = None
        else:
            print("[MemoryService] Operating in Local-First Offline mode.")

    def _init_local_store(self):
        os.makedirs(os.path.dirname(self.local_file), exist_ok=True)
        if not os.path.exists(self.local_file):
            default_state = {
                "users": {
                    "guest_user": {
                        "user_id": "guest_user",
                        "username": "Trailblazer",
                        "level": 1,
                        "xp": 0,
                        "xp_to_next_level": 150,
                        "streak_days": 1,
                        "completed_challenges_count": 0,
                        "badges": [],
                        "unlocked_features": [],
                        "offline_mode": settings.OFFLINE_MODE,
                        "preferred_categories": [],
                        "recent_categories": [],
                    }
                },
                "challenges": {},
                "completions": [],
                "social_feed": [
                    {
                        "id": "post_1",
                        "author_name": "Maya S.",
                        "author_level": 6,
                        "broad_location": "Portland, OR",
                        "challenge_title": "Find 3 distinct tree barks",
                        "category": "Nature",
                        "reflection": "Found a weeping willow near the river trail. Spent an hour sitting by the water instead of scrolling Instagram.",
                        "time_ago": "2 hours ago",
                        "kudos_count": 14,
                        "verified": True
                    },
                    {
                        "id": "post_2",
                        "author_name": "Liam K.",
                        "author_level": 7,
                        "broad_location": "Boulder, CO",
                        "challenge_title": "Help a stranger without prompt",
                        "category": "Kindness",
                        "reflection": "Helped someone load a heavy bicycle rack into their trunk at the park trailhead. We ended up having a great conversation about mountain routes.",
                        "time_ago": "5 hours ago",
                        "kudos_count": 28,
                        "verified": True
                    },
                    {
                        "id": "post_3",
                        "author_name": "Elena R.",
                        "author_level": 5,
                        "broad_location": "Austin, TX",
                        "challenge_title": "Walk 20 minutes without headphones",
                        "category": "Outdoor",
                        "reflection": "Felt weird at first without a podcast, but heard so many cardinals and neighborhood kids playing. Calmed my anxiety immediately.",
                        "time_ago": "1 day ago",
                        "kudos_count": 19,
                        "verified": True
                    }
                ]
            }
            with open(self.local_file, "w") as f:
                json.dump(default_state, f, indent=2)

    def _read_data(self) -> Dict[str, Any]:
        try:
            with open(self.local_file, "r") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "challenges": {}, "completions": [], "social_feed": []}

    def _write_data(self, data: Dict[str, Any]):
        with open(self.local_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_user_context(self, user_id: str = "guest_user") -> UserContext:
        # Try Mongo first if online
        if self.db is not None:
            try:
                user_doc = self.db.users.find_one({"user_id": user_id})
                if user_doc:
                    user_doc.pop("_id", None)
                    return UserContext(**user_doc)
            except Exception as e:
                print(f"[MemoryService] Mongo read fallback to local: {e}")

        # Local read
        data = self._read_data()
        users = data.get("users", {})
        if user_id in users:
            return UserContext(**users[user_id])
        
        # Create default
        new_user = UserContext(user_id=user_id)
        data.setdefault("users", {})[user_id] = new_user.model_dump()
        self._write_data(data)
        return new_user

    def save_user_context(self, context: UserContext):
        # Save to local
        data = self._read_data()
        data.setdefault("users", {})[context.user_id] = context.model_dump()
        self._write_data(data)

        # Sync to Mongo if online
        if self.db is not None and not context.offline_mode:
            try:
                self.db.users.update_one(
                    {"user_id": context.user_id},
                    {"$set": context.model_dump()},
                    upsert=True
                )
            except Exception as e:
                print(f"[MemoryService] Mongo write fallback: {e}")

    def record_challenge(self, challenge: Challenge):
        data = self._read_data()
        data.setdefault("challenges", {})[challenge.id] = challenge.model_dump()
        self._write_data(data)

        if self.db is not None:
            try:
                self.db.challenges.update_one(
                    {"id": challenge.id},
                    {"$set": challenge.model_dump()},
                    upsert=True
                )
            except Exception:
                pass

    def get_challenge(self, challenge_id: str) -> Optional[Challenge]:
        data = self._read_data()
        item = data.get("challenges", {}).get(challenge_id)
        if item:
            return Challenge(**item)
        return None

    def record_completion(self, user_id: str, challenge: Challenge, reflection: str, minutes: int, reward: RewardResult):
        record = {
            "completion_id": f"comp_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "challenge_id": challenge.id,
            "challenge_title": challenge.title,
            "category": challenge.category.value,
            "reflection": reflection,
            "minutes_spent": minutes,
            "xp_earned": reward.total_xp_awarded,
            "timestamp": datetime.datetime.now().isoformat()
        }
        data = self._read_data()
        data.setdefault("completions", []).append(record)
        
        # update recent categories for diversity tracking
        users = data.get("users", {})
        if user_id in users:
            recent = users[user_id].get("recent_categories", [])
            recent.insert(0, challenge.category.value)
            users[user_id]["recent_categories"] = recent[:10]

        self._write_data(data)

        if self.db is not None:
            try:
                self.db.completions.insert_one(record)
            except Exception:
                pass

    def get_recent_categories(self, user_id: str = "guest_user", limit: int = 5) -> List[str]:
        data = self._read_data()
        user = data.get("users", {}).get(user_id, {})
        return user.get("recent_categories", [])[:limit]

    def get_all_completions(self, user_id: str = "guest_user") -> List[Dict[str, Any]]:
        data = self._read_data()
        all_comps = data.get("completions", [])
        return [c for c in all_comps if c.get("user_id") == user_id]

    def get_social_feed(self) -> List[SocialPost]:
        data = self._read_data()
        feed = data.get("social_feed", [])
        return [SocialPost(**item) for item in feed]

memory_service = MemoryService()
