import os
import json
import time

class JarvisMonitor:
    """
    Phase X: System Stabilization (Logging Dashboard).
    A CLI widget that tails the execution.jsonl log to render a live health report.
    """
    def __init__(self, log_path="/var/log/jarvis/execution.jsonl"):
        self.log_path = log_path
        if not os.path.exists(self.log_path):
            self.log_path = os.path.expanduser("~/.config/jarvis/logs/execution.jsonl")

    def render_once(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("="*60)
        print(" 🧠  JARVIS OS - ECOLOGY MONITOR  🚀 ")
        print("="*60)
        
        if not os.path.exists(self.log_path):
            print("\n[Status] Logs empty. OS has not executed any intents.")
            return

        logs = []
        try:
            with open(self.log_path, "r") as f:
                for line in f:
                    logs.append(json.loads(line))
        except Exception:
            pass

        # Calculate failure rate
        now = time.time()
        recent = [l for l in logs if (now - l.get("epoch", 0)) < 3600]
        failures = [l for l in recent if l.get("success") is False]
        
        fail_rate = (len(failures) / len(recent) * 100) if recent else 0.0
        
        print("\n[SYSTEM HEALTH]")
        print(f"Total Intents Analyzed (1H): {len(recent)}")
        print(f"Failure Rate (1H):         {fail_rate:.1f}%")
        
        if fail_rate > 30.0:
            print("Status: 🔴 CRITICAL WARNING (High Error Rate)")
        elif fail_rate > 10.0:
            print("Status: 🟡 DEGRADED")
        else:
            print("Status: 🟢 OPTIMAL")

        print("\n[LAST 5 EXECUTIONS]")
        for log in logs[-5:]:
            indicator = "🟢" if log.get('success') else "🔴"
            print(f"{log.get('timestamp', '')[:19]} | {indicator} | {log.get('intent')}")

        print("\n" + "="*60)

    def run(self):
        """Infinite dashboard loop."""
        try:
            while True:
                self.render_once()
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n[Monitor] Terminated.")

if __name__ == "__main__":
    monitor = JarvisMonitor()
    monitor.run()
