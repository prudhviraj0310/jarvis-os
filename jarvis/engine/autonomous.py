import time
import threading
import subprocess
from jarvis.engine.energy import EnergyEngine

class InterruptionGuard:
    """
    Ensures safe cancelation of sequences if physically or verbally interrupted.
    """
    def __init__(self):
        self._halt_flag = False

    def is_halted(self) -> bool:
        return self._halt_flag

    def cancel_all(self):
        print("[InterruptionGuard] 🛑 HALT INITIATED. Canceling all active sequences.")
        self._halt_flag = True

    def reset(self):
        self._halt_flag = False

class AutonomousEngine:
    """
    Phase 19: Proactive Automation.
    Jarvis acts before you ask, based on system context and time.
    """
    def __init__(self, voice_stream=None):
        self.guard = InterruptionGuard()
        self.voice_stream = voice_stream  # Link to VoiceStream Agent for spoken alerts
        self.energy = EnergyEngine()
        
        # Load MemPalace directly to trigger GC
        from jarvis.plugins.mempalace_adapter import MemPalaceAdapter
        self.mempalace = MemPalaceAdapter()
        
        self._last_battery_alert = 0
        self._last_gc_run = 0

    def tick(self):
        """
        Runs continuously in the Background Presence Loop.
        Checks for proactive trigger conditions.
        """
        # Phase 31: Evaluate Energy Gate before executing autonomous behaviors
        live_context = self._get_live_context()
        if not self.energy.evaluate_proactive_gate(live_context):
            return
            
        # Pseudo-trigger: 9:00 AM workflow
        current_time = time.localtime()
        if current_time.tm_hour == 9 and current_time.tm_min == 0:
            self._trigger_morning_routine()

        # Pseudo-trigger: MemPalace Garbage Collection (3:00 AM)
        now = time.time()
        if current_time.tm_hour == 3 and (now - self._last_gc_run) > 86400:
            print("[Autonomous] 🌙 Initiating Nightly Memory Compression...")
            self.mempalace.compress()
            self._last_gc_run = now

        # Pseudo-trigger: Battery low
        # In a real system, we'd read /sys/class/power_supply/BAT0/capacity
        self._check_battery()

    def _trigger_morning_routine(self):
        """Simulates an autonomous workflow execution."""
        from jarvis.engine.tool_router import ToolRouter
        try:
            print("[Autonomous] 🌅 Triggering 9:00 AM daily startup...")
            if self.voice_stream:
                # We could ideally stream directly or inject an intent
                print("[Autonomous] Initiating morning sequence.")
        except Exception as e:
            print(f"[Autonomous] Failed routine: {e}")

    def _get_live_context(self) -> dict:
        """Reads real OS context for energy calculations."""
        ctx = {"idle_time": 0, "active_app": "desktop"}
        try:
            # Read idle time via xprintidle (X11) or fallback
            result = subprocess.run(["xprintidle"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                ctx["idle_time"] = int(result.stdout.strip()) / 1000  # ms -> seconds
        except Exception:
            pass
        
        try:
            # Get active window name
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                window_name = result.stdout.strip().lower()
                for app in ["vscode", "code", "terminal", "firefox", "chrome"]:
                    if app in window_name:
                        ctx["active_app"] = app
                        break
        except Exception:
            pass
        
        # Time of day
        hour = time.localtime().tm_hour
        if 22 <= hour or hour < 6:
            ctx["time_of_day"] = "night"
        else:
            ctx["time_of_day"] = "day"
            
        return ctx

    def _check_battery(self):
        """Reads real battery level from /sys/class/power_supply/."""
        battery_level = 100
        try:
            # Try reading real battery (Linux sysfs)
            with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                battery_level = int(f.read().strip())
        except (FileNotFoundError, ValueError, PermissionError):
            # No battery (desktop) or permission denied — skip silently
            return
        
        now = time.time()
        # Trigger battery alert only once every 30 mins
        if battery_level < 20 and (now - self._last_battery_alert) > 1800:
            print("[Autonomous] 🔋 Battery low threshold reached.")
            if self.voice_stream:
                # The voice_stream represents the orchestrator.
                # In real prod we inject pseudo LLM prompts: "Inform user battery is low"
                print("Jarvis Voice: Sir, your battery is heavily depleted. Suggesting termination of heavy processes.")
            self._last_battery_alert = now

    def auto_execute(self, action_sequence: list):
        """
        Fires an action sequence automatically if behavior prediction confidence > 0.90
        Hooks safely into the InterruptionGuard.
        """
        print("[Autonomous] 🤖 Initiating High-Confidence Auto-Execution.")
        self.guard.reset()
        
        for action in action_sequence:
            if self.guard.is_halted():
                print("[Autonomous] Execution Aborted midway due to HALT.")
                break
                
            print(f"[Autonomous Executing] {action}")
            time.sleep(1) # Simulated execution delay
