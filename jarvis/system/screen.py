import subprocess
import os
import time
import json

class ScreenAwarenessLayer:
    def __init__(self, capture_dir="/tmp/jarvis_vision"):
        self.capture_dir = capture_dir
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir, exist_ok=True)

    def capture_screen(self) -> str:
        """
        Takes a snapshot of the screen using grim (Wayland) or scrot (X11).
        Does NOT send to LLM yet. Just builds the visual reflex storage.
        """
        timestamp = int(time.time())
        filepath = os.path.join(self.capture_dir, f"capture_{timestamp}.png")
        
        try:
            # Attempt to use grim natively to snapshot Wayland compositor
            result = subprocess.run(["grim", filepath], capture_output=True, check=False)
            if result.returncode != 0:
                # Fallback to scrot if grim missing/X11
                subprocess.run(["scrot", filepath], capture_output=True, check=False)
            return filepath
        except Exception:
            return ""

    def get_screen_state(self) -> dict:
        """
        Queries the compositor directly for structural perception.
        """
        state = {
            "active_window": "",
            "active_class": "",
            "timestamp": time.time()
        }
        
        try:
            # Hyprland Primary Hook
            # Returns a JSON representation of the currently focused window
            result = subprocess.run(["hyprctl", "activewindow", "-j"], capture_output=True, text=True, check=False)
            if result.returncode == 0 and result.stdout.strip() != "{}":
                data = json.loads(result.stdout)
                state["active_window"] = data.get("title", "")
                state["active_class"] = data.get("class", "")
                return state
                
            # Sway/wlroots fallback hook
            result = subprocess.run(["swaymsg", "-t", "get_tree"], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                tree = json.loads(result.stdout)
                # Parse swaymsg tree to find focused node
                focused_node = self._find_focused_node_sway(tree)
                if focused_node:
                    state["active_window"] = focused_node.get("name", "")
                    state["active_class"] = focused_node.get("app_id", "")
            
        except Exception:
            pass # Swallow errors if compositors are missing (e.g. testing environments)
            
        return state

    def _find_focused_node_sway(self, node):
        if node.get("focused"):
            return node
        for child in node.get("nodes", []) + node.get("floating_nodes", []):
            focused = self._find_focused_node_sway(child)
            if focused:
                return focused
        return None

    def verify_context(self, expected_window: str) -> bool:
        """
        Closes the perception loop.
        Compares expected context vs what visually/structurally holds compositor focus.
        """
        if not expected_window:
            return True # No verification required
            
        state = self.get_screen_state()
        active_title = state.get("active_window", "").lower()
        active_class = state.get("active_class", "").lower()
        expected = expected_window.lower()
        
        # We check both the Window Title (e.g. "YouTube - Google Chrome")
        # and the Window Class (e.g. "firefox")
        if expected in active_title or expected in active_class:
            return True
            
        return False
