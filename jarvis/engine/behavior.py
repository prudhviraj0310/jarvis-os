import time
from typing import List, Dict, Any, Tuple

class BehavioralEngine:
    """
    Phase 6: Predicts and anticipates user intent based on historical frequency.
    Converts MemPalace raw pattern data into a scored probability matrix.
    """
    def __init__(self):
        self.SUGGESTION_THRESHOLD = 0.75
        self.AUTO_EXEC_THRESHOLD = 0.90 # Kept for future autonomous phases

    def _get_time_of_day(self) -> str:
        hour = time.localtime().tm_hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "evening"
        else: return "night"

    def analyze_patterns(self, workflows: List[Dict[str, Any]], intent: str) -> Tuple[List[dict], float]:
        """
        Level 2 Contextual Intelligence: Calculates probability using weighted multi-variable context.
        """
        if not workflows:
            return [], 0.0
            
        intent_lower = intent.lower()
        current_time_of_day = self._get_time_of_day()
        now = time.time()
        
        sequence_buckets = {}
        
        # 1. Fuzzy Matching / Grouping
        for wf in workflows:
            stored_intent = str(wf.get("trigger_intent", "")).lower()
            if intent_lower not in stored_intent and stored_intent not in intent_lower:
                continue
                
            seq = wf.get("successful_pipeline", [])
            import json
            seq_str = json.dumps(seq, sort_keys=True)
            if seq_str not in sequence_buckets:
                sequence_buckets[seq_str] = []
            sequence_buckets[seq_str].append(wf)
            
        if not sequence_buckets:
            return [], 0.0

        best_seq_str = None
        highest_confidence = 0.0
        
        # 2. Weighted Matrix Evaluation
        for seq_str, wf_list in sequence_buckets.items():
            freq = len(wf_list)
            # Baseline frequency (max 0.4)
            freq_weight = min(freq * 0.1, 0.4) 
            
            # Analyze contextual properties of the most recent occurrence of this sequence
            best_wf = max(wf_list, key=lambda x: x.get("timestamp", 0))
            
            time_match_weight = 0.3 if best_wf.get("time_of_day") == current_time_of_day else 0.0
            context_match_weight = 0.2 if best_wf.get("active_app") == "terminal" else 0.0
            
            # Recency Decay
            hours_ago = (now - best_wf.get("timestamp", 0)) / 3600.0
            decay = max(0, 0.1 - (hours_ago * 0.005)) 
            
            # Total Score Matrix
            total_confidence = round(freq_weight + time_match_weight + context_match_weight + decay, 2)
            
            if total_confidence > highest_confidence:
                highest_confidence = total_confidence
                best_seq_str = seq_str
                
        import json
        predicted_sequence = json.loads(best_seq_str)
        
        return predicted_sequence, highest_confidence

    def predict_next_action(self, current_intent: str, workflows: List[Dict[str, Any]]) -> dict:
        """
        Determines if Jarvis should intercept the OS loop with an anticipatory suggestion.
        """
        predicted_seq, confidence = self.analyze_patterns(workflows, current_intent)
        
        if confidence >= self.SUGGESTION_THRESHOLD:
            return {
                "prediction": predicted_seq,
                "confidence": confidence,
                "should_suggest": True,
                "should_auto_exec": confidence >= self.AUTO_EXEC_THRESHOLD
            }
            
        return {
            "prediction": [],
            "confidence": confidence,
            "should_suggest": False,
            "should_auto_exec": False
        }
