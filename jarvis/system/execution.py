import subprocess
import enum
import shlex

class RiskLevel(enum.Enum):
    SAFE = "SAFE"
    MODERATE = "MODERATE"
    CRITICAL = "CRITICAL"

class ExecutionPolicy:
    @staticmethod
    def evaluate(command: str) -> RiskLevel:
        """
        Determines the risk of a command based on static heuristics.
        Shield 1: Command Classification
        """
        # Define strict word boundaries to avoid catching substrings by accident
        critical_keywords = [
            "rm -rf", "mkfs", "dd ", "chmod -r", "chown -r", 
            "reboot", "shutdown", "wget ", "curl ", "sudo "
        ]
        moderate_keywords = [
            "kill", "rm ", "mv ", "systemctl restart", "systemctl stop", 
            "apt ", "dpkg ", "pacman "
        ]
        safe_keywords = [
            "ls ", "echo ", "cat ", "ps ", "pwd", "grep ", "whoami"
        ]
        
        lower_cmd = command.lower()
        if any(kw in lower_cmd for kw in critical_keywords):
            return RiskLevel.CRITICAL
        if any(kw in lower_cmd for kw in moderate_keywords):
            return RiskLevel.MODERATE
        
        # If it's not explicitly in the safe list (and isn't just a 1-word safe command),
        # we default to MODERATE to be careful, rather than assuming unknown is SAFE.
        # Here we just check if it starts with a safe command (using `shlex.split` for safety).
        try:
            tokens = shlex.split(lower_cmd)
            if tokens and tokens[0] in [k.strip() for k in safe_keywords]:
                return RiskLevel.SAFE
        except ValueError:
            pass # Unclosed quotes, malformed command
            
        return RiskLevel.MODERATE

def execute_command(command: str) -> dict:
    """
    Executes a system shell command reliably.
    Shield 3: Output Validation and explicit failure capture.
    """
    try:
        # shell=True is dangerous by design, but necessary for an OS control layer
        # The ExecutionPolicy is responsible for gating this.
        result = subprocess.run(
            command, shell=True, check=False, # We don't raise an exception on exit code > 0
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            return {
                "status": "success", 
                "stdout": result.stdout.strip(), 
                "stderr": result.stderr.strip(),
                "code": 0
            }
        else:
            return {
                "status": "error", 
                "stdout": result.stdout.strip(), 
                "stderr": result.stderr.strip(),
                "code": result.returncode
            }
    except Exception as e:
        # Catch unexpected Python errors during execution attempt
        return {
            "status": "error", 
            "stdout": "", 
            "stderr": f"Framework execution failure: {e}", 
            "code": -1
        }
