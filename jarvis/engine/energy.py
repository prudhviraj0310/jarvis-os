import time

class EnergyEngine:
    """
    Phase 31: The Energy Model.
    Provides behavioral self-control by assigning an internal "Energy" scalar [0.0 -> 1.0].
    Dynamically prevents Jarvis from being annoying, overly proactive, or vocal when inappropriate.
    """
    def __init__(self):
        self.last_suggestion_time = 0
        self.FOCUS_APPS = ["vscode", "code", "terminal", "idea", "pycharm"]

    def calculate(self, context: dict, emotion: str = "neutral") -> float:
        """
        Derives the current energy coefficient based on situational context.
        Returns a float mapped between 0.0 (Silence) and 1.0 (Highly Proactive).
        """
        score = 1.0
        now = time.time()

        # 1. User Activity (Idle tracking)
        idle_time = context.get("idle_time", 0)
        if idle_time > 3600:
            # Deep sleep - User has likely left the room. Silence required.
            return 0.0
        elif idle_time > 60:
            # User is away from mouse, good time to verbally prompt if needed
            score += 0.2
        else:
            # User is actively typing/working
            score -= 0.3

        # 2. Time of day
        # e.g. "night" vs "day" string calculated in context layer
        if context.get("time_of_day") == "night":
            score -= 0.2

        # 3. Focus Context (IDE/Work bounds)
        active_app = context.get("active_app", "").lower()
        if any(app in active_app for app in self.FOCUS_APPS):
            score -= 0.5  # Heavy penalty for interrupting deep work

        # 4. Emotional Constraints
        if emotion == "low_energy" or emotion == "urgent":
            score -= 0.3 # Keep responses brutally concise

        # Clamp between 0.0 and 1.0
        return max(0.0, min(score, 1.0))

    def evaluate_proactive_gate(self, context: dict) -> bool:
        """
        Enforces a cooldown block for heavy overarching autonomous suggestions.
        """
        now = time.time()
        
        # 300 second strict cooldown (5 minutes)
        if (now - self.last_suggestion_time) < 300:
            return False
            
        energy_score = self.calculate(context)
        if energy_score > 0.7:
            self.last_suggestion_time = now
            return True
            
        return False
