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
                "design app", "build architecture", "complex project", "website prototype"
            ],
            "aider": [
                "edit file", "fix bug", "refactor test", "inline edit", "terminal code"
            ],
            "openclaw": [
                "crawl", "scrape", "repetitive", "organize documents", "background task", "monitor", "continuously"
            ],
            "n8n": [
                "api pipeline", "visual workflow", "connect services", "email trigger automation"
            ],
            "firecrawl": [
                "learn", "study", "read docs", "ingest url", "scrape context", "understand"
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
        if "build" in intent_lower and "scraper" in intent_lower:
            pipeline.append({"tool": "claude_code", "task": f"Write the python code for: {intent}"})
            pipeline.append({"tool": "openclaw", "task": "Execute the newly created scraper and verify outputs"})
            return pipeline
            
        # 2. Check for Heavy Architecture Tasks (Claude)
        if any(keyword in intent_lower for keyword in self.routes["claude_code"]):
            pipeline.append({"tool": "claude_code", "task": intent})
            return pipeline

        # 3. Check for Fast Terminal Coding Tasks (Aider)
        if any(keyword in intent_lower for keyword in self.routes["aider"]):
            pipeline.append({"tool": "aider", "task": intent})
            return pipeline

        # 4. Check for Autonomous Web Agents (Firecrawl) - Phase 17
        if any(keyword in intent_lower for keyword in self.routes["firecrawl"]):
            pipeline.append({"tool": "firecrawl", "task": intent})
            return pipeline

        # 5. Check for Headless Automation (OpenClaw)
        if any(keyword in intent_lower for keyword in self.routes["openclaw"]):
            pipeline.append({"tool": "openclaw", "task": intent})
            return pipeline

        # 6. Check for Visual API Workflows (n8n)
        if any(keyword in intent_lower for keyword in self.routes["n8n"]):
            pipeline.append({"tool": "n8n", "task": intent})
            return pipeline

        # 7. Default to the fast Local LLM (System Control Layer)
        pipeline.append({
            "tool": "system",
            "task": intent
        })
        return pipeline
