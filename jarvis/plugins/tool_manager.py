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
            "openclaw": {"bin": "openclaw"}
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
