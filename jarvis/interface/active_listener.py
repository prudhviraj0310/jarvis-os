import queue
import threading
import time
import numpy as np
import io
import wave
try:
    import sounddevice as sd
except ImportError:
    sd = None

class ActiveSessionEngine:
    """
    Phase B: The Voice — Continuous Conversation Mode.
    Uses Voice Activity Detection (VAD) via RMS energy to capture speech,
    then uses faster-whisper to transcribe it with high accuracy.
    """
    def __init__(self, callback, on_close=None):
        self.callback = callback
        self.on_close = on_close
        self.q = queue.Queue()
        self.active = False
        self.samplerate = 16000
        self.channels = 1
        
        # VAD Parameters
        self.energy_threshold = 0.01  # Adjust based on mic sensitivity
        self.silence_limit = 1.5      # Seconds of silence before finalizing utterance
        self.session_timeout = 10.0   # Seconds of absolute silence before closing the session
        
        # Faster Whisper model
        try:
            from faster_whisper import WhisperModel
            import os
            # Use small or base for fast inference locally
            self.model_size = "base.en"
            print(f"[ActiveSession] Loading Whisper model ({self.model_size})...")
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        except ImportError:
            print("[ActiveSession] faster-whisper not installed!")
            self.model = None

    def _audio_callback(self, indata, frames, time_info, status):
        """Pushes raw mic bytes to the processing queue."""
        if status:
            pass # Ignore minor underruns
        self.q.put(indata.copy())

    def _rms(self, data):
        """Compute root-mean-square energy of the audio block."""
        return np.sqrt(np.mean(data**2))

    def _transcribe(self, audio_data: np.ndarray) -> str:
        if not self.model:
            return ""
            
        # faster-whisper expects a filepath or a numpy array of floats (-1.0 to 1.0)
        # However, our audio is int16 if we capture that way, or float32 if default.
        # sounddevice default dtype is float32.
        segments, info = self.model.transcribe(audio_data, beam_size=5, language="en", condition_on_previous_text=False)
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    def _listen_loop(self):
        if not sd:
            print("[ActiveSession] sounddevice missing, cannot start active session.")
            self.active = False
            return
            
        print("[ActiveSession] Conversational Session Opened. Speak freely.")
        
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self._audio_callback):
            while self.active:
                audio_buffer = []
                is_speaking = False
                silence_frames = 0
                total_silence_time = 0.0
                
                # Wait for speech to start or timeout
                while self.active:
                    try:
                        data = self.q.get(timeout=0.1)
                        energy = self._rms(data)
                        
                        if energy > self.energy_threshold:
                            is_speaking = True
                            silence_frames = 0
                            total_silence_time = 0.0
                            audio_buffer.append(data)
                        elif is_speaking:
                            silence_frames += 1
                            audio_buffer.append(data)
                            # Assuming default blocksize of roughly 100-300ms depending on device
                            # We'll calculate time based on length of buffer blocks
                            duration = len(data) / self.samplerate
                            if silence_frames * duration >= self.silence_limit:
                                break # End of utterance
                        else:
                            # Not speaking, waiting for speech
                            duration = len(data) / self.samplerate
                            total_silence_time += duration
                            if total_silence_time >= self.session_timeout:
                                print("[ActiveSession] Session timed out due to inactivity.")
                                self.stop()
                                if self.on_close:
                                    self.on_close()
                                return
                                
                    except queue.Empty:
                        continue
                
                if not self.active or len(audio_buffer) == 0:
                    continue
                    
                # We have a completed utterance.
                # Concatenate the float32 array
                audio_data = np.concatenate(audio_buffer)
                audio_data = audio_data.flatten()
                
                # Small utterances (less than 0.5s) are usually noise
                if len(audio_data) / self.samplerate < 0.5:
                    continue
                    
                # Transcribe
                try:
                    text = self._transcribe(audio_data)
                    if text and len(text) > 2:
                        print(f"[Whisper] Scanned: {text}")
                        # Launch callback in background to avoid blocking VAD loop
                        threading.Thread(target=self.callback, args=(text,), daemon=True).start()
                except Exception as e:
                    print(f"[ActiveSession] Transcription error: {e}")
                    
                # Reset total silence timer after successful utterance
                total_silence_time = 0.0

    def start(self):
        if not self.active:
            self.active = True
            t = threading.Thread(target=self._listen_loop, daemon=True)
            t.start()
            
    def stop(self):
        self.active = False
