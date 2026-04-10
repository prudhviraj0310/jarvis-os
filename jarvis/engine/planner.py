import os
import json
import re

class CrewAIPlanner:
    """
    Dynamically generates the OS Action DAG via LLM planning when 
    the heuristic router is insufficient for complex tasks.
    We isolate the CrewAI import so the OS can boot locally even if CrewAI isn't configured yet.
    """
    
    def __init__(self):
        self.trigger_keywords = ["build", "create", "design", "solve", "architect", "pipeline"]
        
    def should_plan(self, intent: str) -> bool:
        """Determines if the LLM Planner should bypass 0ms heuristics."""
        intent_lower = intent.lower()
        return any(intent_lower.startswith(word) for word in self.trigger_keywords)

    def build_pipeline(self, intent: str) -> list:
        # We lazy-load CrewAI so the OS starts instantly and only incurs the import latency 
        # on the very first time the user runs a "build" command.
        try:
            from crewai import Agent, Task, Crew
            from langchain.chat_models import ChatOpenAI
        except ImportError:
            print("[Jarvis Planner] CrewAI/Langchain not installed. Falling back to default static routing.")
            return [{"tool": "system", "task": intent}]

        print("\n[Jarvis Planner] Waking OS Architect Node...")
        
        # Verify API key exists
        if not os.environ.get("OPENAI_API_KEY"):
            print("[Jarvis Planner] OPENAI_API_KEY missing. CrewAI cannot plan. Fallback to System.")
            return [{"tool": "system", "task": intent}]
            
        try:
            # We use an LLM specifically instructed to return JSON arrays
            architect = Agent(
                role='Jarvis OS Architecture Planner',
                goal='Analyze complex user requests and break them down into an execution pipeline DAG.',
                backstory='You are the central planner of a Linux operating system. You delegate tasks to 4 tools: claude_code (for heavy software architecture), aider (for fast inline coding edits in terminal), openclaw (for browser and system automation), and n8n (for visual workflow creation).',
                verbose=False,
                allow_delegation=False
            )
            
            task_description = f"""
            The user wants to: {intent}
            
            Based on this request, create a sequential array of steps.
            Output ONLY valid JSON. No markdown wrappers. E.g.
            [
              {{"tool": "claude_code", "task": "Design python architecture"}},
              {{"tool": "openclaw", "task": "Run the tests in terminal"}}
            ]
            
            Tools available: claude_code, aider, openclaw, n8n.
            """
            
            planning_task = Task(
                description=task_description,
                expected_output='A JSON array of dictionaries with "tool" and "task" keys.',
                agent=architect
            )
            
            crew = Crew(
                agents=[architect],
                tasks=[planning_task],
                verbose=0
            )
            
            result = crew.kickoff()
            
            # Simple JSON extraction regex since LLMs sometimes wrap in ```json ... ```
            json_str = result
            match = re.search(r'\[.*\]', result, re.DOTALL)
            if match:
                json_str = match.group(0)
                
            pipeline = json.loads(json_str)
            print(f"[Jarvis Planner] Architect generated a {len(pipeline)}-step pipeline.")
            return pipeline
            
        except Exception as e:
            print(f"[Jarvis Planner ERROR] CrewAI compilation failed: {e}")
            return [{"tool": "system", "task": intent}]
