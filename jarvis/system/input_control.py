import subprocess
import time
import shlex

from jarvis.system.screen import ScreenAwarenessLayer

class RateLimitError(Exception):
    pass

class SafetyCheckError(Exception):
    pass

class InputControlLimiter:
    def __init__(self, max_actions_per_second: int = 5):
        self.max_rate = max_actions_per_second
        self.action_timestamps = []

    def check_rate(self):
        now = time.time()
        # Clean up events older than 1 second
        self.action_timestamps = [t for t in self.action_timestamps if now - t < 1.0]
        
        if len(self.action_timestamps) >= self.max_rate:
            raise RateLimitError("Physical action rate limit exceeded. Preventing loop chaos.")
        
        self.action_timestamps.append(now)

class InputControlLayer:
    def __init__(self):
        self.limiter = InputControlLimiter(max_actions_per_second=5)
        self.screen_layer = ScreenAwarenessLayer()

    def _ensure_active_window(self, target_window: str):
        # Phase 4 hook: Route directly to compositor perception logic
        if not target_window:
            return # No context restriction requested
            
        verified = self.screen_layer.verify_context(target_window)
        if not verified:
            raise SafetyCheckError(f"Context mismatch: Expected '{target_window}' but it does not have compositor focus.")

    def _actuate_ydotool(self, args: list, target_window: str = None) -> dict:
        """Raw unified executor for ydotool arguments."""
        # 1. Rate limiting
        self.limiter.check_rate()
        
        # 2. Window safety check (True Visual Perception)
        try:
            self._ensure_active_window(target_window)
        except SafetyCheckError as e:
            return {"status": "error", "error": str(e)}
        
        # 3. Execution
        cmd = ["ydotool"] + args
        try:
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                return {"status": "error", "error": result.stderr.strip()}
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def execute_input_action(self, payload: dict) -> dict:
        """
        The deterministic muscle action contract.
        payload = {"type": "type|key|mousemove|click", "value": ..., "target_window": "firefox"}
        """
        action_type = payload.get("action", "")  # We updated the llm.py schema to use "action" here instead of "type" which is "input"/"system" at top level
        # Wait, the prompt said: {"type": "input", "action": "type", "value": "youtube.com"} -> but the LLM schema we used says type: input, action: type. Let me double check what parameter LLM enforces. In phase 3.5 it was "action" on the input item!
        # Ah! Let me properly pull action:
        if "action" in payload:
            action_type = payload.get("action", "")
        else:
            action_type = payload.get("type", "") 

        target_window = payload.get("target_window", None)
        
        if action_type == "type":
            text = payload.get("value", "")
            if not text:
                return {"status": "error", "error": "Empty text payload."}
            return self._actuate_ydotool(["type", text], target_window)
            
        elif action_type == "key":
            key_code = payload.get("value", "")
            if not key_code:
                return {"status": "error", "error": "Empty key payload."}
            return self._actuate_ydotool(["key", str(key_code)], target_window)
            
        elif action_type == "mousemove":
            coords = payload.get("value", {})
            try:
                x = int(coords.get("x", -1))
                y = int(coords.get("y", -1))
                if x < 0 or y < 0:
                    raise ValueError
            except:
                return {"status": "error", "error": "Invalid coordinates for mousemove."}
            
            return self._actuate_ydotool(["mousemove", str(x), str(y)], target_window)
            
        elif action_type == "click":
            # "0xC0" for left, "0xC1" for right
            btn = payload.get("value", "0xC0")
            return self._actuate_ydotool(["click", str(btn)], target_window)
            
        else:
            return {"status": "error", "error": f"Unknown input action type: {action_type}"}
