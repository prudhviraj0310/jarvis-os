import subprocess
import time
import os

class OverlayEngine:
    """
    Phase Z: HUD & Soul.
    Cinematic visual feedback layer using 'notify-send' with Mako semantics.
    Enforces a single card replacing itself cleanly (ID 1234) and plays sub-chimes.
    """
    def __init__(self):
        self.app_name = "Jarvis HUD"
        # Magic ID ensures notifications overwrite each other instead of stacking visually
        self.replace_id = "999" 
        self.asset_dir = os.path.expanduser("~/.config/jarvis/assets/sounds")

    def _play_sfx(self, filename: str):
        """Asynchronously plays a soft chime via PulseAudio/Pipewire."""
        path = os.path.join(self.asset_dir, filename)
        if os.path.exists(path):
            subprocess.Popen(["paplay", path], stderr=subprocess.DEVNULL)

    def _dispatch(self, title: str, urgency: str, timeout: str, sfx: str = None):
        """Native dispatcher holding the single replace UI."""
        if sfx:
            self._play_sfx(sfx)
            
        try:
            # -p allows grabbing the ID but we use a fixed hint string to force Mako overwrite
            # Note: mako supports `-h string:x-canonical-private-synchronous:jarvis` to group identical cards
            subprocess.Popen([
                "notify-send",
                "-a", self.app_name,
                "-u", urgency,
                "-t", timeout,
                "-h", "string:x-canonical-private-synchronous:jarvis_hud",
                title
            ], stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass

    def listening(self):
        """Top-right small pulse: softly triggers on wake."""
        self._dispatch("● Listening...", "normal", "0", "ping_high.wav") # 0 = sticky until replaced

    def processing(self):
        """Thin circular spinner: triggers when LLM is querying."""
        self._dispatch("◌ Processing...", "normal", "0") # No sfx needed, sticky

    def executing(self):
        """Quick flash for script runs."""
        self._dispatch("→ Executing", "normal", "1000")

    def success(self):
        """Fades instantly on success."""
        self._dispatch("✓ Done", "low", "1500", "click.wav")

    def warning(self):
        """Critical block notification."""
        self._dispatch("⚠ Critical Command Blocked", "critical", "3000", "buzz_low.wav")
