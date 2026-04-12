import subprocess
import threading
import time
from enum import Enum
import os

class Priority(Enum):
    ROUTINE = 0
    ASSIST = 1
    CRITICAL = 2

class VoiceEngine:
    """
    Cinematic Voice Interface for Jarvis OS.
    Features voice fatigue tokenization and priority-based filtering.
    """
    def __init__(self):
        # Settings: Pitch 35 (Deep), Speed 165 (Fast/Cold)
        self.espeak_args = ["espeak", "-v", "en-us", "-s", "165", "-p", "35"]
        
        # Fatigue Tokenizer (max 6 sentences per minute)
        # We store timestamps of recent voice events.
        self.history = []
        self.MAX_EVENTS_PER_MIN = 6
        
        # Micro Sound Cues
        self.assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        os.makedirs(self.assets_dir, exist_ok=True)
        
    def _cull_history(self):
        current_time = time.time()
        self.history = [t for t in self.history if current_time - t < 60]

    def _run_espeak(self, text: str):
        try:
            subprocess.Popen(self.espeak_args + [text], stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass

    def can_speak(self, priority: Priority = Priority.ROUTINE) -> bool:
        """
        Checks if the voice engine is allowed to speak right now based on fatigue rules.
        """
        self._cull_history()
        if priority == Priority.ROUTINE:
            return False
            
        if priority == Priority.ASSIST:
            if len(self.history) >= self.MAX_EVENTS_PER_MIN:
                return False
                
        return True

    def consume_fatigue_token(self):
        """Deducts a token when an external streaming engine speaks."""
        self.history.append(time.time())

    def speak(self, text: str, priority: Priority = Priority.ROUTINE):
        """
        Legacy static TTS. Conditionally speaks text based on priority and fatigue tokens.
        Consider using VoiceStream's DuplexAudioEngine for real-time interactions.
        """
        if not self.can_speak(priority):
            return
                
        # Critical bypasses fatigue checks OR Assist passed fatigue checks
        self.consume_fatigue_token()
        t = threading.Thread(target=self._run_espeak, args=(text,), daemon=True)
        t.start()

    def play_cue(self, cue_name: str):
        """
        Plays a high-fidelity micro sound via ALSA aplay.
        Expected files: listening.wav, success.wav, error.wav
        """
        wav_path = os.path.join(self.assets_dir, f"{cue_name}.wav")
        if os.path.exists(wav_path):
            try:
                subprocess.Popen(["aplay", "-q", wav_path], stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                pass
