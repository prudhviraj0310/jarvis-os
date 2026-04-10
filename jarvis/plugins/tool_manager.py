import os
import subprocess
import shutil

class ToolManager:
    """
    Manages the lifecycle and execution of external AI agents (Claude, OpenClaw).
    Prevents Jarvis from becoming bloated by dynamically invoking these when verified.
    """
    def __init__(self):
        self.tools = {
            "claude_code": {"bin": "claude"},
            "openclaw": {"bin": "openclaw"},
            "aider": {"bin": "aider"},
            "n8n": {"bin": "n8n"}
        }

    def is_installed(self, tool_name: str) -> bool:
        """Checks if the CLI executable for the agent is installed in the system PATH."""
        if tool_name not in self.tools:
            return False
        return shutil.which(self.tools[tool_name]["bin"]) is not None

    def execute_claude_code(self, intent: str, ui_callback) -> bool:
        """
        Spawns the Claude Code agent.
        Yields terminal control so the user can interact natively with Claude.
        """
        ui_callback("Using Coding Engine", "Delegating to Claude Code...", "normal")
        print("\n[Jarvis Orchestrator] Yielding control to Claude Code...")
        
        try:
            # We construct the Claude Code initialization command.
            # Using -p to pass the prompt directly to Claude.
            cmd = ["claude", "-p", intent]
            
            # We let subprocess maintain control of stdin/stdout. 
            # This is "Option A" - terminal delegation.
            result = subprocess.run(cmd)
            
            print("\n[Jarvis Orchestrator] Resuming control.")
            ui_callback("Coding Complete", "Claude session ended.", "normal")
            return result.returncode == 0
        except Exception as e:
            print(f"[Jarvis ERROR] Claude Code delegation failed: {e}")
            return False

    def execute_openclaw(self, intent: str, ui_callback) -> bool:
        """
        Spawns the OpenClaw automation agent.
        """
        ui_callback("Using Automation Agent", "Delegating to OpenClaw...", "normal")
        print("\n[Jarvis Orchestrator] Yielding control to OpenClaw...")
        
        try:
            cmd = ["openclaw", "run", "--prompt", intent]
            result = subprocess.run(cmd)
            print("\n[Jarvis Orchestrator] Resuming control.")
            ui_callback("Automation Complete", "OpenClaw session ended.", "normal")
            return result.returncode == 0
        except Exception as e:
            print(f"[Jarvis ERROR] OpenClaw delegation failed: {e}")
            return False

    def execute_aider(self, intent: str, ui_callback) -> bool:
        """
        Spawns Aider for fast terminal-based inline coding.
        """
        ui_callback("Using Fast Coder", "Delegating to Aider...", "normal")
        print("\n[Jarvis Orchestrator] Yielding control to Aider...")
        
        try:
            cmd = ["aider", "--message", intent]
            result = subprocess.run(cmd)
            print("\n[Jarvis Orchestrator] Resuming control.")
            ui_callback("Coding Complete", "Aider session ended.", "normal")
            return result.returncode == 0
        except Exception as e:
            print(f"[Jarvis ERROR] Aider delegation failed: {e}")
            return False

    def execute_n8n(self, intent: str, ui_callback) -> bool:
        """
        Triggers an n8n webhook or workflow based on the intent.
        Assuming here n8n is running locally as a service.
        """
        ui_callback("Triggering Workflow", "Piping intent to n8n API...", "normal")
        print("\n[Jarvis Orchestrator] Sending intent to n8n workflow engine...")
        
        try:
            # Here we simulate triggering a generic n8n webhook. 
            # In production, this would map the intent to specific workflow IDs.
            # Example curl to a local n8n instance:
            cmd = ["curl", "-X", "POST", "http://localhost:5678/webhook/jarvis-trigger", "-d", f'{{"intent": "{intent}"}}']
            result = subprocess.run(cmd, capture_output=True)
            print("\n[Jarvis Orchestrator] Workflow dispatched successfully.")
            ui_callback("Workflow Active", "n8n pipeline triggered.", "normal")
            return result.returncode == 0
        except Exception as e:
            print(f"[Jarvis ERROR] n8n execution failed: {e}")
            return False

