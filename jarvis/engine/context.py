from collections import deque
import json
from jarvis.plugins.mempalace_adapter import MemPalaceAdapter

class ContextEngine:
    """
    JARVIS CONTEXT ENGINE (Phase 5)
    Central intelligence node intercepting all intent before Engine logic.
    Maintains a 3-Layered memory cache to enrich sparse prompts.
    """
    def __init__(self):
        # Layer 1: Ephemeral Runtime (Last 10 intent/action cycles)
        self.short_term_memory = deque(maxlen=10)
        
        # Layer 2: Active Session Context 
        self.active_context = {
            "mode": "idle",
            "active_tasks": [],
            "recent_failures": 0
        }
        
        # Layer 3: Long-Term Workflow Recall (Adapter)
        self.mempalace = MemPalaceAdapter()

    def enrich(self, user_intent: str) -> dict:
        """
        Takes raw intent string and packs it with tiered contextual knowledge.
        DOES NOT block execution.
        """
        enriched_payload = {
            "raw_intent": user_intent,
            "L1_recent_actions": list(self.short_term_memory),
            "L2_session_state": self.active_context,
            "L3_workflow_history": None
        }

        # Query Layer 3 only if we need pattern matching.
        # Keeping it lightweight: we just query L3 natively on all intents for Phase 5 demo.
        # But we wrap it securely to prevent blocking.
        try:
            l3_data = self.mempalace.query_history(user_intent)
            if l3_data:
                enriched_payload["L3_workflow_history"] = l3_data
        except Exception as e:
            print(f"[Context Engine] Layer 3 query degraded safely: {e}")

        # Update Layer 2 logic lightly
        if "error" in user_intent.lower() or "wrong" in user_intent.lower():
            self.active_context["recent_failures"] += 1
        else:
            self.active_context["recent_failures"] = 0

        return enriched_payload

    def record_success(self, intent: str, action_sequence: list):
        """
        Called organically by Runtime after a pipeline confirms execution context via Vision layer.
        """
        # Store in Layer 1 (Ephemeral)
        self.short_term_memory.append({
            "intent": intent,
            "sequence": action_sequence
        })
        
        # Fire to Layer 3 for Long-Term pattern extraction
        self.mempalace.commit_success(intent, action_sequence)
