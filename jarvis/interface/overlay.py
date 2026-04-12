import subprocess
import time
import os

class OverlayEngine:
    """
    Phase Z: HUD & Soul.
    Cinematic visual feedback layer.
    
    Strategy:
      1. Try native GTK4 HUD (JarvisHUD via layer-shell) — the Iron Man overlay
      2. Fallback to notify-send with Mako semantics — lightweight text notifications
    """
    def __init__(self):
        self.app_name = "Jarvis HUD"
        self.replace_id = "999" 
        self.asset_dir = os.path.expanduser("~/.config/jarvis/assets/sounds")
        self._native_hud = None
        self._debounce_ts = 0
        self._init_native_hud()

    def _init_native_hud(self):
        """Try to connect to the native GTK4 HUD if it's running."""
        try:
            from jarvis.ui.hud import JarvisHUD
            self._native_hud = JarvisHUD()
            self._native_hud.run_background()
            print("[OverlayEngine] Native GTK4 HUD active.")
        except Exception:
            self._native_hud = None

    def _play_sfx(self, filename: str):
        """Asynchronously plays a soft chime via PulseAudio/Pipewire."""
        path = os.path.join(self.asset_dir, filename)
        if os.path.exists(path):
            subprocess.Popen(["paplay", path], stderr=subprocess.DEVNULL)

    def _debounce(self) -> bool:
        """Prevents rapid-fire overlay spam. Returns True if should skip."""
        now = time.time()
        if now - self._debounce_ts < 0.5:
            return True
        self._debounce_ts = now
        return False

    def _dispatch(self, title: str, urgency: str, timeout: str, sfx: str = None):
        """Fallback dispatcher using notify-send (Mako)."""
        if sfx:
            self._play_sfx(sfx)

        try:
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

    # ══════════════════════════════════════════
    # Public API — called from engine layers
    # ══════════════════════════════════════════

    def listening(self):
        """Pulsing arc reactor indicator."""
        if self._debounce():
            return
        if self._native_hud:
            self._native_hud.listening()
        else:
            self._dispatch("● Listening...", "normal", "0", "ping_high.wav")

    def processing(self):
        """Spinning ring animation."""
        if self._debounce():
            return
        if self._native_hud:
            self._native_hud.thinking()
        else:
            self._dispatch("◌ Processing...", "normal", "0")

    def executing(self):
        """Energy flow progress bar."""
        if self._debounce():
            return
        if self._native_hud:
            self._native_hud.executing()
        else:
            self._dispatch("→ Executing", "normal", "1000")

    def success(self):
        """Expanding green confirmation ring."""
        if self._native_hud:
            self._native_hud.success()
        else:
            self._dispatch("✓ Done", "low", "1500", "click.wav")

    def warning(self):
        """Amber warning with alert sound."""
        if self._native_hud:
            self._native_hud.warning("Critical Command Blocked")
        else:
            self._dispatch("⚠ Critical Command Blocked", "critical", "3000", "buzz_low.wav")

    def speaking(self, text=""):
        """Waveform visualization while TTS is playing."""
        if self._native_hud:
            self._native_hud.speaking(text)
        else:
            self._dispatch(f"♪ {text}", "low", "5000")

    def show_status(self, title: str, body: str, urgency: str):
        """Generic status display — used by tests and external callers."""
        if self._debounce():
            return
        if self._native_hud:
            self._native_hud.show("thinking", title, body)
        else:
            self._dispatch(f"{title}: {body}", urgency, "3000")
