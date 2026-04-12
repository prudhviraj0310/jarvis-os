class EmotionEngine:
    """
    Phase 17: Emotional Intelligence Layer
    Infers the user's implicit tone, mood, and urgency, adjusting Jarvis's vocal characteristics
    and conversational padding.
    """
    def __init__(self):
        self.trigger_keywords = {
            "low_energy": ["tired", "exhausted", "sleep", "done", "long day", "burnout"],
            "urgent": ["fast", "quick", "hurry", "urgent", "now", "immediately", "emergency"],
            "casual": ["bro", "hey", "yo", "man", "mate", "dude"]
        }

    def detect(self, text: str) -> str:
        """Lightweight heuristic emotion classifier."""
        text_lower = text.lower()
        
        for state, words in self.trigger_keywords.items():
            if any(word in text_lower for word in words):
                return state
                
        return "neutral"

    def adapt_voice_params(self, emotion: str) -> dict:
        """
        Returns vocal pacing and synthesis parameters tailored to the user's state.
        This allows the TTS engine to modify its speed/pitch seamlessly.
        """
        params = {
            "speed": 1.0,
            "pitch_shift": 0,
            "prefix_filler": ""
        }
        
        if emotion == "low_energy":
            params["speed"] = 0.85
            params["pitch_shift"] = -1
            params["prefix_filler"] = "Got it… take it easy. "
        elif emotion == "urgent":
            params["speed"] = 1.25
            params["pitch_shift"] = 1
            params["prefix_filler"] = "On it. "
        elif emotion == "casual":
            params["speed"] = 1.05
            params["prefix_filler"] = "Done, boss. "
            
        return params

    def apply_filler(self, response: str, emotion: str) -> str:
        """
        Contextually pads the raw AI response with human-like fillers.
        """
        params = self.adapt_voice_params(emotion)
        filler = params["prefix_filler"]
        
        if filler and not response.startswith("<call"):
            return f"{filler}{response}"
            
        return response
