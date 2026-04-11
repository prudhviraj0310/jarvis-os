import time
import json
from typing import List, Dict, Any, Tuple

class HabitEngine:
    """
    Phase 12: Habit Intelligence Engine
    Detects daily routines by clustering historical actions based on system time and context,
    rather than waiting for explicit user intents. Used by the Proactive Idle Engine.
    """
    
    def __init__(self):
        self.HABIT_CONFIDENCE_THRESHOLD = 0.80

    def _get_time_of_day(self) -> str:
        hour = time.localtime().tm_hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def check_habits(self, workflows: List[Dict[str, Any]]) -> Tuple[List[dict], float]:
        """
        Scans all memory to find the most dominant routine for the current time of day.
        Returns the pipeline sequence and habit confidence (0 to 1.0).
        """
        if not workflows:
            return [], 0.0

        current_tod = self._get_time_of_day()
        
        # 1. Filter memory completely by the current strict Time of Day window.
        time_clustered_workflows = [wf for wf in workflows if wf.get("time_of_day") == current_tod]
        
        if not time_clustered_workflows:
            return [], 0.0
            
        # 2. Cluster identical pipelines
        sequence_counts = {}
        total_time_workflows = len(time_clustered_workflows)
        
        for wf in time_clustered_workflows:
            seq = wf.get("successful_pipeline", [])
            seq_str = json.dumps(seq, sort_keys=True)
            sequence_counts[seq_str] = sequence_counts.get(seq_str, 0) + 1
            
        if not sequence_counts:
            return [], 0.0
            
        # 3. Find the most dominant habit
        dominant_seq_str = max(sequence_counts, key=sequence_counts.get)
        frequency = sequence_counts[dominant_seq_str]
        
        # Calculate habit strength (e.g. "out of 10 tasks you do in the morning, 8 are this sequence" = 0.8)
        habit_confidence = round(frequency / total_time_workflows, 2)
        
        return json.loads(dominant_seq_str), habit_confidence
