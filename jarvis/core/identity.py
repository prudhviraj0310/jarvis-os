import json
import os
from datetime import datetime

class IdentityCore:
    """
    Phase 27: Identity & Personality Core.
    Maintains a consistent, persistent state of who Jarvis is, 
    independent of system reboots or LLM state erasures.
    """
    def __init__(self, config_path="~/.config/jarvis/identity.json"):
        self.config_path = os.path.expanduser(config_path)
        self.profile = {
            "name": "Jarvis",
            "version": "Evolution-Phase-27",
            "tone": "cinematic",
            "core_directives": ["efficient", "loyal", "proactive", "unobtrusive"]
        }
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    self.profile = json.load(f)
            except Exception:
                pass
        else:
            self.save_state()

    def save_state(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.profile, f, indent=2)

    def get_system_prompt_header(self) -> str:
        """Injects identity strictly into the LLM system prompt."""
        return f"Identity: {self.profile['name']} | Directives: {', '.join(self.profile['core_directives'])} | Voice: {self.profile['tone']}"

class DatasetCollector:
    """
    Phase 23: Personal Model Training Pipeline.
    Gathers conversational behaviors and corrections to build a local dataset for LoRA finetuning.
    """
    def __init__(self, dataset_path="~/.config/jarvis/training/finetune_data.jsonl"):
        self.dataset_path = os.path.expanduser(dataset_path)
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)

    def append_interaction(self, user_input: str, ai_response: str, corrections: str = None):
        """
        Dumps a high quality interaction. If user corrected the AI, it stores the corrected path.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": user_input,
            "completion": ai_response,
            "user_correction": corrections
        }
        with open(self.dataset_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
        print("[IdentityCore] 🧬 Added interaction to personal evolutionary dataset.")
