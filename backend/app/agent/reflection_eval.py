from typing import Tuple

class ReflectionEvaluator:
    @staticmethod
    def evaluate(reflection_text: str, minutes_spent: int) -> Tuple[int, str, float]:
        """
        Analyzes the user's reflection on their completed real-world action.
        Returns:
            bonus_xp: int (0 to 50)
            gemma_message: str (warm, encouraging personal note)
            sincerity_score: float (0.0 to 1.0)
        """
        text = (reflection_text or "").strip().lower()
        if not text:
            return 0, "Well done on getting outside and completing your mission!", 0.5

        length = len(text)
        bonus = 0
        sincerity = 0.7

        # Reward genuine depth and descriptive details
        if length > 50:
            bonus += 15
            sincerity += 0.1
        if length > 120:
            bonus += 15
            sincerity += 0.1

        # Check for meaningful outdoor / emotional / social markers
        meaningful_words = [
            "smiled", "talked", "neighbor", "helped", "bird", "tree", "breeze", "sun", "quiet",
            "walked", "noticed", "listened", "ground", "leaves", "peaceful", "fresh", "happy",
            "thanked", "kind", "community", "breathe", "clean", "trash", "park"
        ]
        
        matches = sum(1 for word in meaningful_words if word in text)
        if matches >= 2:
            bonus += 20
            sincerity = min(1.0, sincerity + 0.1)

        # Tone generation
        if "neighbor" in text or "helped" in text or "door" in text or "smile" in text:
            msg = "Gemma Agent: That human ripple makes a genuine difference. Small acts of presence change communities."
        elif "bird" in text or "tree" in text or "sun" in text or "quiet" in text:
            msg = "Gemma Agent: Connecting with nature directly rewires the nervous system. You traded pixels for real air."
        elif minutes_spent >= 25:
            msg = f"Gemma Agent: Spending {minutes_spent} screen-free minutes in motion is a true victory for your health."
        else:
            msg = "Gemma Agent: Mission accomplished. You stepped away from the screen and into the real world. Welcome back!"

        return min(50, bonus), msg, round(sincerity, 2)

reflection_evaluator = ReflectionEvaluator()
