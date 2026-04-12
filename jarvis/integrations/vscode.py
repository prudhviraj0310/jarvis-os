import subprocess
import os

class VSCodeIntegration:
    """
    Phase D: The Ecosystem — VS Code Control
    Integrates with the `code` CLI to manipulate the editor without GUI interactions.
    """
    
    def __init__(self):
        self.workspace_root = os.path.expanduser("~/")
        
    def open_workspace(self, path: str) -> str:
        # Prevent completely arbitrary path traversal out of standard zones if needed
        # But since Jarvis runs locally on full system, standard paths are fine
        target = os.path.expanduser(path)
        if not os.path.exists(target):
            return f"Path {target} does not exist."
            
        res = subprocess.run(["code", target], capture_output=True, text=True)
        return f"Opened VS Code at {target}" if res.returncode == 0 else f"Failed to open VS Code: {res.stderr.strip()}"
        
    def diff_files(self, file1: str, file2: str) -> str:
        res = subprocess.run(["code", "--diff", file1, file2], capture_output=True, text=True)
        return "Opened diff view." if res.returncode == 0 else f"Failed to diff: {res.stderr.strip()}"

    def execute_command(self, cmd_data: dict) -> str:
        """Entry point for VoiceStream's <call:vscode...> interception."""
        action = cmd_data.get("action", "")
        if action == "open":
            return self.open_workspace(cmd_data.get("path", "."))
        elif action == "diff":
            return self.diff_files(cmd_data.get("file1", ""), cmd_data.get("file2", ""))
        return "Unknown VS Code action."
