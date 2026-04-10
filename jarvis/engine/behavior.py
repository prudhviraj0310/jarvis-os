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

    def analyze_patterns(self, workflows: List[Dict[str, Any]], intent: str) -> Tuple[List[dict], float]:
        """
        Calculates the probability of what sequence usually follows the current intent.
        Returns the top predicted action sequence and its confidence score.
        """
        if not workflows:
            return [], 0.0
            
        intent_lower = intent.lower()
        matching_workflows = []
        
        # Find workflows triggered by similar intent
        for wf in workflows:
            if intent_lower in str(wf.get("trigger_intent", "")).lower():
                matching_workflows.append(wf["successful_pipeline"])
                
        if not matching_workflows:
            return [], 0.0

        # Frequency scoring: For Phase 6, we just find the most common sequence length and exact items.
        # Natively, we stringify the JSON array to group them.
        sequence_counts = {}
        for seq in matching_workflows:
            import json
            seq_str = json.dumps(seq, sort_keys=True)
            sequence_counts[seq_str] = sequence_counts.get(seq_str, 0) + 1

        if not sequence_counts:
            return [], 0.0
            
        # Find the most frequent
        top_seq_str = max(sequence_counts, key=sequence_counts.get)
        frequency = sequence_counts[top_seq_str]
        
        # Confidence = (How many times this exact sequence happened) / (Total times intent was executed)
        confidence = round(frequency / len(matching_workflows), 2)
        
        import json
        predicted_sequence = json.loads(top_seq_str)
        
        return predicted_sequence, confidence

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
