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

    def route(self, intent: str) -> list:
        """
        Determines the appropriate agent DAG (pipeline) for the user's intent.
        Returns a list of dicts: [{"tool": "claude_code|openclaw|system", "task": "..."}]
        """
        intent_lower = intent.lower()
        pipeline = []
        
        # 1. Multi-Agent DAG Check
        # If the intent requires designing and running, chain them.
        if "build" in intent_lower and "scraper" in intent_lower:
            pipeline.append({"tool": "claude_code", "task": f"Write the python code for: {intent}"})
            pipeline.append({"tool": "openclaw", "task": "Execute the newly created scraper and verify outputs"})
            return pipeline
            
        # 2. Check for coding tasks
        if any(keyword in intent_lower for keyword in self.routes["claude_code"]):
            if "code" in intent_lower or "app" in intent_lower or "script" in intent_lower or "website" in intent_lower or "debug" in intent_lower:
                pipeline.append({
                    "tool": "claude_code",
                    "task": intent
                })
                return pipeline

        # 3. Check for automation/agent tasks
        if any(keyword in intent_lower for keyword in self.routes["openclaw"]):
            pipeline.append({
                "tool": "openclaw",
                "task": intent
            })
            return pipeline

        # 4. Default to the fast Local LLM (System Control Layer)
        pipeline.append({
            "tool": "system",
            "task": intent
        })
        return pipeline
