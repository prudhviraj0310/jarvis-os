import time
import threading

# Import the core interface and engine pieces
from jarvis.interface.voice_stream import StreamingAgent
from jarvis.interface.listener import WakeWordEngine
from jarvis.engine.autonomous import AutonomousEngine
from jarvis.engine.context import ContextEngine
from jarvis.engine.behavior import BehavioralEngine

class ContinuousAwarenessLoop:
    """
    Phase 20: Digital Presence (True Jarvis Mode).
    Runs indefinitely on system startup. Integrates Ambient Audio, Emotional Tone, 
    Autonomous Logic, and System Awareness into one cohesive living cycle.
    """
    def __init__(self):
        print("[Jarvis Presence] Initializing OS Digital Core...")
        
        self.context = ContextEngine()
        self.behavior = BehavioralEngine()
        
        # 1. Boot the Sentient Voice Stream
        # It owns the PyAudio Duplex buffers inherently.
        self.agent = StreamingAgent(self.context, self.behavior)
        
        # 2. Boot the Autonomous Logic layer
        # Giving it a reference to VoiceStream allows it to speak unprompted
        self.auto_engine = AutonomousEngine(voice_stream=self.agent)
        
        # 3. Boot Passive Listener (Hooking into Duplex shared queue ideally)
        # Note: If no shared queue is provided, it falls back to standalone mic read
        # depending on ALSA config. We mock the handler block.
        self.listener = WakeWordEngine(callback=self.on_wake_event, shared_input_queue=getattr(self.agent.audio, "input_queue", None))

    def on_wake_event(self, intent_string: str):
        """
        Triggered asynchronously when the user speaks Jarvis's name or a command.
        """
        # 1. Global Kill Switch (Phase X)
        if "jarvis stop everything" in intent_string.lower():
            print("[Presence Loop] 🚨 GLOBAL KILL SWITCH ACTIVATED 🚨")
            self.auto_engine.guard.cancel_all()
            self._global_shutdown = True # We need a flag for the main while loop
            return
            
        # Immediately halt any autonomous sequences executing erroneously
        self.auto_engine.guard.cancel_all()
        
        if intent_string.lower() == "stop":
            # Just an interruption, do nothing.
            return
            
        print(f"\n[Presence Loop] Heard Intent: {intent_string}")
        
        # Pass the intent into the high-speed streaming LLM cycle
        # The agent will handle Context Enrichment L1-L3, Emotion matching, and Tool routing
        self.agent.handle_voice_input(intent_string)

    def start(self):
        """
        Initiates the Digital Presence. This is designed to be the primary `systemctl` target.
        """
        self._global_shutdown = False
        
        # Start hardware queues
        self.agent.start()
        
        # Start passive wake-word scanning
        self.listener.start()
        
        print("[Jarvis Presence] Online. We are live, sir.")
        
        try:
            while not self._global_shutdown:
                # 4. Ambient Event Loop
                # Ticks the autonomous engine to monitor environment quietly
                self.auto_engine.tick()
                
                # Observe screen or behavior could be hooked here asynchronously (Phase 21 stub)
                
                # Sleep heavily to reduce CPU footprint 
                time.sleep(60) 
                
            if self._global_shutdown:
                print("\n[Jarvis Presence] 🚨 Critical Shutdown complete.")
                
        except KeyboardInterrupt:
            print("\n[Jarvis Presence] Shutting down...")
        finally:
            self.listener.stop()
            self.agent.stop()

if __name__ == "__main__":
    presence = ContinuousAwarenessLoop()
    presence.start()
