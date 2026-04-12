import queue
import threading
import json
import sys

class WakeWordEngine:
    """
    Passive Always-Listening Audio Monitor.
    Runs 'Vosk' with 'sounddevice' continuously grabbing 16kHz audio from ALSA.
    It expects 'vosk-model-small-en-us' in the root or /opt/jarvis/.
    """
    def __init__(self, callback, shared_input_queue=None):
        self.callback = callback
        self.q = shared_input_queue if shared_input_queue else queue.Queue()
        self.listening = False
        self._shared_queue_mode = shared_input_queue is not None
        
        # Phase Z: HUD
        from jarvis.interface.overlay import OverlayEngine
        self.hud = OverlayEngine()

    def _audio_callback(self, indata, frames, time, status):
        """This is called continuously by sounddevice for each audio block."""
        if status:
            pass # Usually buffer underflow/overflow, silently ignore
        self.q.put(bytes(indata))

    def _listen_loop(self):
        try:
            import vosk
            import sounddevice as sd
        except ImportError:
            print("[Jarvis Wake] Dependencies missing (vosk, sounddevice). Passive listening disabled.")
            return

        # Suppress vosk C-level logs
        vosk.SetLogLevel(-1)
        
        try:
            # We assume model is deployed at /opt/jarvis/vosk-model (standardized for Buildroot ISO)
            # or in local directory 'vosk-model'
            model_path = "/opt/jarvis/vosk-model"
            import os
            if not os.path.exists(model_path):
                model_path = "vosk-model"
                
            model = vosk.Model(model_path)
        except Exception as e:
            print(f"[Jarvis Wake] Failed to load offline Vosk acoustic model: {e}")
            return

        samplerate = 16000
        rec = vosk.KaldiRecognizer(model, samplerate)

        try:
            self.listening = True
            print("[Jarvis Wake] Sentient presence active. Listening passively.")
            
            # If using shared queue, bypass sounddevice open
            if self._shared_queue_mode:
                while self.listening:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        self._process_result(rec)
            else:
                with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                                       channels=1, callback=self._audio_callback):
                    while self.listening:
                        data = self.q.get()
                        if rec.AcceptWaveform(data):
                            self._process_result(rec)
                            
        except Exception as e:
            print(f"[Jarvis Wake ERROR] Audio capture crashed: {e}")
            self.listening = False

    def _process_result(self, rec):
        result = json.loads(rec.Result())
        text = result.get("text", "")
        # WAKE WORD TRIGGERS HERE
        if "jarvis" in text:
            # Phase Z: Flash Wake Word UI immediately
            self.hud.listening()
            
            # False Trigger Defense: Must have substance or be exactly 'jarvis'
            intent = text.replace("jarvis", "").strip()
            
            # Ignore random single-syllable phantom noise picked up as 'jarvis a'
            if len(intent) > 0 and len(intent) < 3:
                return
                
            if not intent:
                intent = "System Wake" # Generic awake intent
            
            # Fire the background callback
            threading.Thread(target=self.callback, args=(intent,), daemon=True).start()

    def start(self):
        if not self.listening:
            t = threading.Thread(target=self._listen_loop, daemon=True)
            t.start()
            
    def stop(self):
        self.listening = False
