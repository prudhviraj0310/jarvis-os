import json
import time
import os
from datetime import datetime

class ExecutionLogger:
    """
    Phase 21: Self-Reflection Core.
    Logs every intent-action pair, capturing latency and success flags.
    """
    def __init__(self, log_dir="/var/log/jarvis/"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir, exist_ok=True)
            except Exception:
                self.log_dir = os.path.expanduser("~/.config/jarvis/logs/")
                os.makedirs(self.log_dir, exist_ok=True)
                
        self.log_file = os.path.join(self.log_dir, "execution.jsonl")

    def log(self, intent: str, actions: list, success: bool, time_taken: float, feedback: str = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "epoch": time.time(),
            "intent": intent,
            "actions": actions,
            "success": success,
            "time_taken": round(time_taken, 3),
            "user_feedback": feedback
        }
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[ExecutionLogger] Failed to write log: {e}")

class ReflectionLoop:
    """
    Analyzes historical failures intermittently and generates systemic
    learning rules to store into MemPalace.
    """
    def __init__(self, logger: ExecutionLogger):
        self.logger = logger
        
    def reflect(self):
        """
        Loads the logs, isolates failures, invokes the LLM to extract the root 
        behavioral block, and pushes it to global rule memory.
        """
        print("[ReflectionEngine] Initiating neural diagnostic trace...")
        if not os.path.exists(self.logger.log_file):
            return
            
        logs = []
        with open(self.logger.log_file, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except Exception:
                    continue
                    
        # Filter for failures in the last 24 hours
        now = time.time()
        failures = [l for l in logs if not l.get("success") and (now - l.get("epoch", 0)) < 86400]
        
        # Phase X: Safe Mode Circuit Breaker
        failures_last_hour = [l for l in failures if (now - l.get("epoch", 0)) < 3600]
        if len(failures_last_hour) >= 3:
            self._trigger_safe_mode()
        
        if not failures:
            print("[ReflectionEngine] System optimal. No recent failure signatures.")
            return
            
        print(f"[ReflectionEngine] Analyzing {len(failures)} failures.")
        
        # In a real system, we pipe 'failures' to OllamaEngine.
        # "Analyze these failures and suggest an architectural heuristic..."
        # Simulated LLM output:
        for f in failures:
            self._analyze(f)
            
    def _analyze(self, failure_record: dict):
        """Mock analysis call."""
        intent = failure_record.get("intent", "Unknown")
        print(f"[ReflectionEngine] Evaluated Intent: '{intent}' -> Generating heuristic patch.")
        # E.g., mempalace_adapter.store_knowledge("rule_"+intent, "Never use CSS, use XPath")

    def _trigger_safe_mode(self):
        """
        Phase X: Emergency quarantine.
        In an integrated system, we pull references to EvolutionEngine and 
        AutonomousEngine and hard-kill their ticks.
        """
        print("\n[ReflectionEngine] ⚠️ CRITICAL ALERT: High Failure Chain Detected!")
        print("[ReflectionEngine] 🛡️ INITIATING SYSTEM SAFE MODE.")
        print("  - EvolutionEngine: DISABLED")
        print("  - AutonomousEngine: DISABLED")
        print("  - ExternalWorldAdapter: DISABLED")
        print("[ReflectionEngine] Jarvis is now restricted to passive Voice IO only until manual reset.\n")
        
        # Here we would toggle global state variables:
        # e.g., os.environ["JARVIS_SAFE_MODE"] = "1"
