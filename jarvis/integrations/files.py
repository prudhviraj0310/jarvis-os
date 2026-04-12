import subprocess
import os

class FileIntegration:
    """
    Phase D: The Ecosystem — Deep File Management
    Handles semantic file lookups and safe data operations.
    """
    
    def search(self, query: str, path: str = "~") -> str:
        target = os.path.expanduser(path)
        # Using `find` to do a basic filename search safely.
        # Can scale up to `fd` or `rg` if installed.
        res = subprocess.run(["find", target, "-type", "f", "-iname", f"*{query}*"], capture_output=True, text=True)
        files = res.stdout.strip().split("\n")
        if not files or files == [""]:
            return f"No files found matching '{query}' in {target}."
        
        # Truncate if too many results
        if len(files) > 10:
            return f"Found {len(files)} files. First 10:\n" + "\n".join(files[:10])
        return f"Found {len(files)} files:\n" + "\n".join(files)

    def execute_command(self, cmd_data: dict) -> str:
        action = cmd_data.get("action", "")
        if action == "search":
            return self.search(cmd_data.get("query", ""), cmd_data.get("path", "~"))
        return "Unknown file action."
