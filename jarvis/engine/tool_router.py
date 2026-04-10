class ToolRouter:
    """
    JARVIS AI ORCHESTRATION LAYER
    This router inspects the raw intent and routes it to specialized AI agents.
    If no specialized agent is required, it defaults to the OS-native execution layer.
    """
    def __init__(self):
        # Semantic hints for routing (Phase 1: Heuristic based for 0ms execution)
        # For a full implementation, you could use a fast classifier LLM here.
        self.routes = {
            "claude_code": [
                "build", "code", "write", "debug", "refactor", "app", 
                "website", "script", "program", "function", "compile"
            ],
            "openclaw": [
                "automate", "workflow", "crawl", "scrape", "repetitive", 
                "monitor", "organize documents", "background task"
            ]
        }

    def route(self, intent: str) -> dict:
        """
        Determines the appropriate agent for the user's intent.
        Returns a dict: {"tool": "claude_code|openclaw|system", "reason": "..."}
        """
        intent_lower = intent.lower()
        
        # 1. Check for coding tasks
        if any(keyword in intent_lower for keyword in self.routes["claude_code"]):
            # Prevent false positives like "build a habit"
            if "code" in intent_lower or "app" in intent_lower or "script" in intent_lower or "website" in intent_lower or "debug" in intent_lower:
                return {
                    "tool": "claude_code",
                    "reason": "semantic match for complex software engineering task"
                }

        # 2. Check for automation/agent tasks
        if any(keyword in intent_lower for keyword in self.routes["openclaw"]):
            return {
                "tool": "openclaw",
                "reason": "semantic match for autonomous workflow execution"
            }

        # 3. Default to the fast Local LLM (System Control Layer)
        return {
            "tool": "system",
            "reason": "default OS execution pipeline"
        }
