import subprocess
import time

class OverlayEngine:
    """
    Cinematic visual feedback layer using 'notify-send'.
    Features debounce logic to prevent spam.
    """
    
    def __init__(self):
        self.app_name = "Jarvis OS"
        self.last_msg = ""
        self.last_time = 0.0
        # 500ms debounce
        self.DEBOUNCE_DELAY = 0.5
        
    def show_status(self, title: str, message: str, urgency: str = "normal"):
        """
        Displays a non-blocking HUD element. Debounces identical/rapid messages.
        Urgency levels: 'low', 'normal', 'critical'
        """
        current_time = time.time()
        
        # Debounce rapid fire
        if current_time - self.last_time < self.DEBOUNCE_DELAY:
            return
            
        # Optional: Prevent repeating the exact same message back-to-back quickly
        if self.last_msg == message and (current_time - self.last_time < 2.0):
            return

        self.last_msg = message
        self.last_time = current_time

        try:
            # -a "App Name" replaces identical cards implicitly in modern libnotify
            subprocess.Popen([
                "notify-send",
                "-a", self.app_name,
                "-u", urgency,
                "-t", "4000",
                title,
                message
            ], stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass
