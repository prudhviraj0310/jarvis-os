import os
import json
import time

class UserProfile:
    """
    Phase 32: True Personalization.
    Jarvis tracks habits, application frequencies, and tonal preferences 
    dynamically over time to shape his internal Thought Layer.
    """
    def __init__(self, profile_path="~/.config/jarvis/dynamic_profile.json"):
        self.profile_path = os.path.expanduser(profile_path)
        self.data = {
            "top_apps": {},
            "active_hours": {},
            "preferred_actions": {},
            "tone": "adaptive"
        }
        self._load()

    def _load(self):
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    self.data = json.load(f)
            except Exception:
                pass
        else:
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        with open(self.profile_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def update(self, intent: str, context: dict):
        """Called natively every time the user issues an intent."""
        hour = str(time.localtime().tm_hour)
        app = context.get("active_app", "desktop").lower()

        # Update Hour frequency
        if hour not in self.data["active_hours"]:
            self.data["active_hours"][hour] = 0
        self.data["active_hours"][hour] += 1

        # Update App frequency
        if app not in self.data["top_apps"]:
            self.data["top_apps"][app] = 0
        self.data["top_apps"][app] += 1
        
        # Simple preferred action tracker
        if "youtube" in intent.lower():
            if "youtube" not in self.data["preferred_actions"]:
                self.data["preferred_actions"]["youtube"] = 0
            self.data["preferred_actions"]["youtube"] += 1

        self._save()

    def get_top_app(self) -> str:
        """Returns the most heavily weighted background context app."""
        if not self.data["top_apps"]:
            return ""
        return max(self.data["top_apps"], key=self.data["top_apps"].get)

    def prefers(self, keyword: str) -> bool:
        """Heuristic check if a keyword exceeds threshold bounds."""
        return self.data["preferred_actions"].get(keyword.lower(), 0) > 5
