import subprocess
import threading
import time
from enum import Enum
import os
import urllib.request

class Priority(Enum):
    ROUTINE = 0
    ASSIST = 1
    CRITICAL = 2

class VoiceEngine:
    """
    Cinematic Voice Interface for Jarvis OS.
    Upgraded to Phase B: Piper TTS for ultra-realistic neural speech.
    Features voice fatigue tokenization and priority-based filtering.
    """
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # We use a default ONNX model from Piper
        self.model_name = "en_US-lessac-medium.onnx"
        self.model_path = os.path.join(self.models_dir, self.model_name)
        self.json_path = self.model_path + ".json"
        
        self.ensure_model_downloaded()
        
        # Command to pipe text into piper, then to aplay
        self.piper_bin = "piper"  # installed via pip install piper-tts
        
        # Fatigue Tokenizer (max 6 sentences per minute)
        self.history = []
        self.MAX_EVENTS_PER_MIN = 6
        
        # Micro Sound Cues
        self.assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        os.makedirs(self.assets_dir, exist_ok=True)
        
    def ensure_model_downloaded(self):
        """Downloads the ONNX voice model if it's missing (First boot)."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.json_path):
            print("[VoiceEngine] Downloading Neural Voice Model (~50MB)...")
            base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/"
            try:
                urllib.request.urlretrieve(base_url + self.model_name, self.model_path)
                urllib.request.urlretrieve(base_url + self.model_name + ".json", self.json_path)
                print("[VoiceEngine] Voice model installed successfully.")
            except Exception as e:
                print(f"[VoiceEngine] Failed to download voice model: {e}")

    def _cull_history(self):
        current_time = time.time()
        self.history = [t for t in self.history if current_time - t < 60]

    def _run_piper(self, text: str):
        try:
            # We pipe the string into Piper, which outputs raw PCM audio, which we pipe into aplay
            # aplay -r 22050 -f S16_LE -t raw -
            piper_cmd = [self.piper_bin, "-m", self.model_path, "--output-raw"]
            
            p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen(piper_cmd, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p1.stdout.close() 
            
            aplay_cmd = ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"]
            p3 = subprocess.Popen(aplay_cmd, stdin=p2.stdout, stderr=subprocess.DEVNULL)
            p2.stdout.close()
            p3.communicate()
            
        except OSError:
            # Fallback to espeak if piper or aplay fails
            subprocess.Popen(["espeak", "-v", "en-us", text], stderr=subprocess.DEVNULL)

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
        self.history.append(time.time())

    def speak(self, text: str, priority: Priority = Priority.ROUTINE):
        """
        Ultra-realistic TTS. Conditionally speaks text based on priority and fatigue tokens.
        """
        if not self.can_speak(priority):
            return
                
        self.consume_fatigue_token()
        
        # Notify HUD of speaking state
        try:
            from jarvis.interface.overlay import OverlayEngine
            OverlayEngine().speaking(text)
        except Exception:
            pass
            
        t = threading.Thread(target=self._run_piper, args=(text,), daemon=True)
        t.start()

    def play_cue(self, cue_name: str):
        wav_path = os.path.join(self.assets_dir, f"{cue_name}.wav")
        if os.path.exists(wav_path):
            try:
                subprocess.Popen(["aplay", "-q", wav_path], stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                pass
