from jarvis.engine.profile import UserProfile

class ThoughtEngine:
    """
    Phase 29: The Thought Layer.
    Adds implicit reasoning, allowing Jarvis to inject internal context 
    into his LLM prior to execution.
    """
    def __init__(self):
        self.profile = UserProfile()

    def generate_thoughts(self, intent: str, context: dict) -> dict:
        """
        Fast heuristic rules to append silent reasoning blocks.
        """
        intent_lower = intent.lower()
        thoughts = {
            "intent": [],
            "memory": [],
            "vision": [],
            "prediction": []
        }

        # 1. Intent Level Heuristics
        if "youtube" in intent_lower or "music" in intent_lower:
            thoughts["intent"].append("User likely wants media playback.")

        if "code" in intent_lower or "build" in intent_lower:
            thoughts["intent"].append("User is in developer mode. Favor terminal/editor actions.")

        # 2. Memory Hook Heuristics (Mocking historical context bindings)
        # e.g., contextualizing L3_workflow_history
        l3_history = context.get("L3_workflow_history", {})
        
        # Phase 32: Dynamic Personalization Hook
        if self.profile.prefers("youtube") and "youtube" in intent_lower:
            thoughts["memory"].append("User historically prefers 'lofi hip hop' when launching media.")
            thoughts["prediction"].append("I should proactively auto-search lofi.")
            
        top_app = self.profile.get_top_app()
        if top_app in ["vscode", "terminal"] and "code" in intent_lower:
            thoughts["intent"].append(f"User is heavily working in {top_app}. Enforce execution precision.")

        # 3. Vision Hook Heuristics
        visual_map = context.get("visual_map")
        if visual_map:
            thoughts["vision"].append(f"Screen currently active with {len(visual_map)} recognized bounding boxes.")
            
            if "submit" in [k.lower() for k in visual_map.keys()]:
                 thoughts["vision"].append("Identified standard form interactions on screen.")

        # Extract only populated categories
        return {k: v for k, v in thoughts.items() if v}

    def format_for_prompt(self, thoughts_dict: dict) -> str:
        """Flattens the structured dictionary into a concise prompt block."""
        output = []
        for category, lines in thoughts_dict.items():
            for line in lines:
                output.append(f"-> [{category.upper()}]: {line}")
        return "\n".join(output)
