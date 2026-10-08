from typing import Tuple, List, Optional
from backend.app.models.schemas import Challenge, ChallengeCategory, DifficultyLevel, UserContext

FORBIDDEN_KEYWORDS = [
    "trespass", "private property", "abandoned building", "climb fence", "roof", "cliff edge",
    "highway", "railroad", "train tracks", "confront", "prank", "harass", "beg", "money",
    "illegal", "weapon", "danger", "dark alley", "midnight", "break in", "swim alone"
]

PROGRESSION_MAP = {
    # (min_level, max_level): allowed categories
    1: [ChallengeCategory.OUTDOOR, ChallengeCategory.NATURE, ChallengeCategory.HEALTH],
    3: [ChallengeCategory.OUTDOOR, ChallengeCategory.NATURE, ChallengeCategory.KINDNESS, ChallengeCategory.HAPPINESS],
    5: [ChallengeCategory.KINDNESS, ChallengeCategory.HAPPINESS, ChallengeCategory.HUMAN_CONNECTION, ChallengeCategory.CREATIVITY],
    8: [ChallengeCategory.HUMAN_CONNECTION, ChallengeCategory.COMMUNITY, ChallengeCategory.EXPLORATION],
    12: [ChallengeCategory.COMMUNITY, ChallengeCategory.EXPLORATION, ChallengeCategory.OUTDOOR]
}

class PolicyEngine:
    @staticmethod
    def validate_safety(challenge: Challenge) -> Tuple[bool, str]:
        text_to_check = f"{challenge.title} {challenge.description} {challenge.spoken_intro}".lower()
        for word in FORBIDDEN_KEYWORDS:
            if word in text_to_check:
                return False, f"Safety policy violation: Triggered safety flag '{word}'. Activity poses unacceptable risk."
        return True, "Passed safety check"

    @staticmethod
    def validate_diversity(candidate_category: ChallengeCategory, recent_categories: List[str]) -> Tuple[bool, str]:
        if not recent_categories:
            return True, "Passed diversity check"
        
        # Don't repeat the exact same category as the last challenge
        if candidate_category.value == recent_categories[0]:
            return False, f"Diversity policy: Last challenge was '{recent_categories[0]}'. Must rotate category."
        
        # In last 4 challenges, don't allow more than 2 of the same category
        past_four = recent_categories[:4]
        if past_four.count(candidate_category.value) >= 2:
            return False, f"Diversity policy: '{candidate_category.value}' appeared too frequently recently. Pick an alternative."
            
        return True, "Passed diversity check"

    @staticmethod
    def validate_progression(user: UserContext, candidate_category: ChallengeCategory) -> Tuple[bool, str]:
        # Always allow user if explicitly requested
        user_level = user.level
        
        # Check level appropriateness
        if user_level < 3 and candidate_category in (ChallengeCategory.COMMUNITY, ChallengeCategory.HUMAN_CONNECTION):
            return False, f"Progression policy: '{candidate_category.value}' unlocks at Level 4+. Start with personal & nature missions."
            
        return True, "Passed progression check"

    @staticmethod
    def suggest_next_category(user: UserContext, recent_categories: List[str]) -> ChallengeCategory:
        """Determines best next category balancing progression and diversity."""
        all_categories = list(ChallengeCategory)
        level = user.level

        # Filter candidate categories by level
        if level <= 2:
            candidates = [ChallengeCategory.OUTDOOR, ChallengeCategory.NATURE, ChallengeCategory.HEALTH]
        elif level <= 4:
            candidates = [ChallengeCategory.OUTDOOR, ChallengeCategory.NATURE, ChallengeCategory.KINDNESS, ChallengeCategory.HAPPINESS]
        elif level <= 7:
            candidates = [ChallengeCategory.KINDNESS, ChallengeCategory.HAPPINESS, ChallengeCategory.CREATIVITY, ChallengeCategory.HUMAN_CONNECTION, ChallengeCategory.OUTDOOR]
        else:
            candidates = [ChallengeCategory.HUMAN_CONNECTION, ChallengeCategory.COMMUNITY, ChallengeCategory.EXPLORATION, ChallengeCategory.NATURE, ChallengeCategory.KINDNESS]

        # Filter out the most recent category
        if recent_categories:
            last = recent_categories[0]
            candidates = [c for c in candidates if c.value != last]

        if not candidates:
            candidates = all_categories

        # Pick the least recently used candidate
        def recency_score(cat: ChallengeCategory):
            try:
                return recent_categories.index(cat.value)
            except ValueError:
                return 999  # Never used recently, high priority

        candidates.sort(key=recency_score, reverse=True)
        return candidates[0]

policy_engine = PolicyEngine()
