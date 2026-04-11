import os
import json
import time
from typing import Dict, Any, List

class MemPalaceAdapter:
    """
    Layer 3: Long-Term Memory (MemPalace integration).
    Follows an OS-safe isolation boundary. 
    Does not halt execution if memory backend is slow.
    Storage structure mimics MemPalace's 'Wings -> Rooms -> Drawers'.
    """
    def __init__(self, data_path="/var/lib/jarvis/mempalace_local.json"):
        # For Phase 5 demo, we simulate MemPalace structure locally.
        # When MemPalace API is ready, we swap the internal implementations here.
        self.data_path = data_path
        self.enabled = True
        
        dir_path = os.path.dirname(self.data_path)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception:
                # Fallback to local user dir if permissions fail
                self.data_path = os.path.expanduser("~/.config/jarvis/mempalace_local.json")
                os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
                
        self._ensure_init()

    def _ensure_init(self):
        if not os.path.exists(self.data_path):
            base_structure = {
                "system_wing": {
                    "routine_room": {"daily_drawer": []},
                    "workflow_room": {"browser_drawer": []}
                },
                "knowledge_wing": {
                    "library_room": {}
                }
            }
            self._save(base_structure)

    def _load(self) -> dict:
        try:
            with open(self.data_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save(self, data: dict):
        try:
            with open(self.data_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[MemPalace] Failed to write memory: {e}")

    def query_history(self, intent: str, context_keys: list = None) -> Dict[str, Any]:
        """
        Retrieves relevant structured historical patterns.
        """
        if not self.enabled:
            return {}

        start_time = time.time()
        
        # Primitive lookup for Phase 5: iterate over workflow_room -> browser_drawer 
        # scanning for keywords related to the intent.
        memory = self._load()
        matched_patterns = []
        
        try:
            drawer = memory.get("system_wing", {}).get("workflow_room", {}).get("browser_drawer", [])
            intent_lower = intent.lower()
            
            for item in drawer:
                if item.get("trigger_intent") and item["trigger_intent"].lower() in intent_lower:
                    matched_patterns.append(item)
                    
            if time.time() - start_time > 1.0:
                print("[MemPalace] WARNING: Query exceeded 1s deadline. Degrading gracefully.")
                return {} # Abort if query is hanging
                
            if matched_patterns:
                # Return the most recent matching pattern
                return {"historical_pattern": matched_patterns[-1]}
                
            return {}
        except Exception as e:
            print(f"[MemPalace] Query failure: {e}")
            return {}

    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Retrieves all stored workflows from the browser drawer for behavioral pattern analysis.
        This provides the raw material for the BehavioralEngine.
        """
        if not self.enabled:
            return []
            
        try:
            memory = self._load()
            return memory.get("system_wing", {}).get("workflow_room", {}).get("browser_drawer", [])
        except Exception as e:
            print(f"[MemPalace] Failed to export workflows: {e}")
            return []

    def _get_time_of_day(self) -> str:
        hour = time.localtime().tm_hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def commit_success(self, intent: str, action_sequence: list):
        """
        Fire-and-forget success storage.
        Jarvis stores the workflow behavior pattern that successfully resolved an intent.
        """
        if not self.enabled or not action_sequence:
            return
            
        try:
            memory = self._load()
            drawer = memory.get("system_wing", {}).get("workflow_room", {}).get("browser_drawer", [])
            
            new_entry = {
                "timestamp": time.time(),
                "time_of_day": self._get_time_of_day(),
                "active_app": "terminal", # Phase 12 Placeholder for Wayland binding
                "trigger_intent": intent,
                "successful_pipeline": action_sequence
            }
            
            drawer.append(new_entry)
            
            # Keep drawer lean (max 50 past workflows)
            if len(drawer) > 50:
                drawer = drawer[-50:]
                
            memory["system_wing"]["workflow_room"]["browser_drawer"] = drawer
            self._save(memory)
        except Exception as e:
            print(f"[MemPalace] Commit failed: {e}")

    def store_knowledge(self, topic: str, content: str):
        """
        Phase 18: Ingests structured domain knowledge directly into the library.
        """
        if not self.enabled:
            return
            
        try:
            memory = self._load()
            library = memory.get("knowledge_wing", {}).get("library_room", {})
            
            # Simple Key-Value for now
            library[topic] = {
                "timestamp": time.time(),
                "content": content
            }
            
            if "knowledge_wing" not in memory:
                memory["knowledge_wing"] = {"library_room": {}}
                
            memory["knowledge_wing"]["library_room"] = library
            self._save(memory)
        except Exception as e:
            print(f"[MemPalace] Knowledge commit failed: {e}")
            
    def query_knowledge(self, topic: str) -> str:
        """
        Returns contextual markdown if it exists in the library.
        """
        try:
            memory = self._load()
            library = memory.get("knowledge_wing", {}).get("library_room", {})
            return library.get(topic, {}).get("content", "")
        except Exception:
            return ""
