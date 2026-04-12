import time
import threading

# Import the core interface and engine pieces
from jarvis.interface.voice_stream import StreamingAgent
from jarvis.interface.listener import WakeWordEngine
from jarvis.engine.autonomous import AutonomousEngine
from jarvis.engine.context import ContextEngine
from jarvis.engine.behavior import BehavioralEngine
from jarvis.interface.active_listener import ActiveSessionEngine


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
        
        # 3. Boot Passive Listener
        self.listener = WakeWordEngine(callback=self.on_wake_event, shared_input_queue=getattr(self.agent.audio, "input_queue", None))
        
        # 4. Boot Active Session Engine (Phase B integration)
        self.active_session = ActiveSessionEngine(callback=self.on_active_intent, on_close=self.on_session_timeout)
        self._in_session = False

    def on_wake_event(self, intent_string: str):
        """
        Triggered asynchronously when the user speaks Jarvis's name.
        Transitions system from passive listening into Active Conversation Session.
        """
        if "jarvis stop everything" in intent_string.lower():
            print("[Presence Loop] 🚨 GLOBAL KILL SWITCH ACTIVATED 🚨")
            self.auto_engine.guard.cancel_all()
            self._global_shutdown = True
            return
            
        self.auto_engine.guard.cancel_all()
        
        if intent_string.lower() == "stop":
            return
            
        print(f"\n[Presence Loop] Heard Wake Word/Intent: {intent_string}")
        
        # Suspend passive wake word listener
        self.listener.stop()
        self._in_session = True
        
        # If the user included a command with the wake word (e.g. "Jarvis open firefox")
        if intent_string != "System Wake":
            self.agent.handle_voice_input(intent_string)
            
        # Enter Continuous Active Session loop
        self.active_session.start()

    def on_active_intent(self, intent_string: str):
        """
        Triggered repeatedly during an Active Session via fast-whisper.
        """
        if "sleep jarvis" in intent_string.lower() or "goodbye" in intent_string.lower() or "go back to sleep" in intent_string.lower():
            print("[Presence Loop] Manually closing active session.")
            self.active_session.stop()
            self.on_session_timeout()
            return
            
        print(f"[Presence Loop] Active Command Received: {intent_string}")
        # Send right to the agent
        self.agent.handle_voice_input(intent_string)

    def on_session_timeout(self):
        """
        Triggered when 10 seconds of silence elapse in an Active Session.
        Resumes passive wake word monitoring.
        """
        print("[Presence Loop] Active Session Complete. Resuming passive monitoring.")
        self._in_session = False
        self.listener.start()

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
