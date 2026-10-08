from typing import List, Tuple
from backend.app.models.schemas import UserContext, Challenge, RewardResult, ChallengeCategory

ALL_BADGES = {
    "earth_helper": {"id": "earth_helper", "title": "Earth Helper", "icon": "🌱", "desc": "Nurtured living nature or environmental surroundings"},
    "mood_maker": {"id": "mood_maker", "title": "Mood Maker", "icon": "😊", "desc": "Brought a genuine smile or positive ripple to someone"},
    "good_human": {"id": "good_human", "title": "Good Human", "icon": "🤝", "desc": "Completed a selfless act of real-world kindness"},
    "outside_person": {"id": "outside_person", "title": "Outside Person", "icon": "🏃", "desc": "Logged meaningful movement and fresh air outside"},
    "early_bird": {"id": "early_bird", "title": "Early Bird", "icon": "🌅", "desc": "Greeted natural daylight in the early morning"},
    "community_builder": {"id": "community_builder", "title": "Community Builder", "icon": "🏘️", "desc": "Took action to improve shared public spaces"}
}

class RewardService:
    @staticmethod
    def calculate_level(total_xp: int) -> Tuple[int, int]:
        """Returns (level, xp_needed_for_next_level)"""
        level = 1
        xp_threshold = 150
        cumulative = 0

        while total_xp >= (cumulative + xp_threshold):
            cumulative += xp_threshold
            level += 1
            xp_threshold = int(xp_threshold * 1.35)

        remaining_needed = (cumulative + xp_threshold) - total_xp
        return level, remaining_needed

    @staticmethod
    def evaluate_reward(
        user: UserContext,
        challenge: Challenge,
        bonus_xp: int,
        encouragement: str,
        sincerity_score: float
    ) -> RewardResult:
        base_xp = challenge.xp_reward
        total_awarded = base_xp + bonus_xp

        old_level = user.level
        old_xp = user.xp
        new_xp = old_xp + total_awarded
        new_level, needed_next = RewardService.calculate_level(new_xp)
        level_up = new_level > old_level

        # Evaluate Badges
        new_badges = []
        user_badges = list(user.badges)

        cat = challenge.category
        if cat in (ChallengeCategory.NATURE, ChallengeCategory.OUTDOOR) and "earth_helper" not in user_badges:
            new_badges.append("earth_helper")
            user_badges.append("earth_helper")
        elif cat == ChallengeCategory.HAPPINESS and "mood_maker" not in user_badges:
            new_badges.append("mood_maker")
            user_badges.append("mood_maker")
        elif cat == ChallengeCategory.KINDNESS and "good_human" not in user_badges:
            new_badges.append("good_human")
            user_badges.append("good_human")
        elif cat in (ChallengeCategory.OUTDOOR, ChallengeCategory.HEALTH) and "outside_person" not in user_badges:
            new_badges.append("outside_person")
            user_badges.append("outside_person")
        elif cat == ChallengeCategory.COMMUNITY and "community_builder" not in user_badges:
            new_badges.append("community_builder")
            user_badges.append("community_builder")

        # Evaluate Feature Unlocks
        new_unlocks = []
        user_unlocks = list(user.unlocked_features)

        if new_level >= 5 and "social_mode" not in user_unlocks:
            new_unlocks.append("social_mode")
            user_unlocks.append("social_mode")
        if new_level >= 10 and "journey_sharing" not in user_unlocks:
            new_unlocks.append("journey_sharing")
            user_unlocks.append("journey_sharing")
        if new_level >= 15 and "group_challenges" not in user_unlocks:
            new_unlocks.append("group_challenges")
            user_unlocks.append("group_challenges")

        # Update UserContext
        user.xp = new_xp
        user.level = new_level
        user.xp_to_next_level = needed_next
        user.completed_challenges_count += 1
        user.badges = user_badges
        user.unlocked_features = user_unlocks

        return RewardResult(
            challenge_id=challenge.id,
            base_xp=base_xp,
            bonus_xp=bonus_xp,
            total_xp_awarded=total_awarded,
            previous_level=old_level,
            new_level=new_level,
            level_up=level_up,
            new_badges=new_badges,
            unlocked_features=new_unlocks,
            gemma_encouragement=encouragement,
            sincerity_score=sincerity_score
        )

reward_service = RewardService()
