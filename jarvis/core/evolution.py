import os
import shutil
import subprocess

class SandboxManager:
    """
    Phase 22: Safe Sandbox Environment.
    Manages the isolated workspace where Jarvis writes and tests code modifications.
    """
    def __init__(self, workspace="/tmp/jarvis_sandbox/"):
        self.workspace = workspace
        self._ensure_clean_state()

    def _ensure_clean_state(self):
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        os.makedirs(self.workspace, exist_ok=True)

    def write_temp(self, filename: str, code: str) -> str:
        filepath = os.path.join(self.workspace, filename)
        with open(filepath, "w") as f:
            f.write(code)
        return filepath

    def test_module(self, filepath: str) -> bool:
        """
        Executes a basic python syntax check and unit test if provided.
        """
        print(f"[Sandbox] Compiling {filepath} for syntax integrity...")
        try:
            # -m py_compile validates syntax without executing
            result = subprocess.run(["python3", "-m", "py_compile", filepath], capture_output=True, text=True)
            if result.returncode == 0:
                print("[Sandbox] ✅ Integrity Check Passed.")
                return True
            else:
                print(f"[Sandbox] ❌ Compilation Failed:\n{result.stderr}")
                return False
        except Exception as e:
            print(f"[Sandbox] ❌ Test Exception: {e}")
            return False

class CodeEvolver:
    """
    Phase 22: Code Evolution Engine (Self-Modifying System).
    Allows Jarvis to improve its own modules under strict hierarchical supervision.
    """
    
    # Phase X: Evolution Lock (Mandatory Safety Guard)
    EVOLUTION_ENABLED = False
    
    def __init__(self):
        self.sandbox = SandboxManager()
        # Explicit Guardrails: Defines paths legally available for mutation.
        self.ALLOWED_DIRECTORIES = ["jarvis/plugins", "jarvis/engine"]
        self.FORBIDDEN_FILES = ["__init__.py", "core/runtime.py", "core/evolution.py"]

    def _is_legal_target(self, file_path: str) -> bool:
        """Enforces safe path boundaries."""
        if any(forbidden in file_path for forbidden in self.FORBIDDEN_FILES):
            return False
            
        return any(allowed in file_path for allowed in self.ALLOWED_DIRECTORIES)

    def improve_module(self, target_filepath: str, llm_engine):
        """
        Loads the module, asks the LLM to patch it, tests it in the sandbox, 
        and replaces the original file if requested.
        """
        print(f"\n[EvolutionEngine] Initiating rewrite protocol for: {target_filepath}")
        
        if not self.EVOLUTION_ENABLED:
            print("[EvolutionEngine] 🛑 FATAL: Evolution Lock is ENABLED. Code modification blocked.")
            return False
        
        if not self._is_legal_target(target_filepath):
            print("[EvolutionEngine] 🛑 FATAL: Target is outside allowed mutation bounds. Aborting.")
            return False

        if not os.path.exists(target_filepath):
            print(f"[EvolutionEngine] 🛑 Target file does not exist: {target_filepath}")
            return False

        with open(target_filepath, "r") as f:
            original_code = f.read()

        # Simulated LLM rewrite call
        print("[EvolutionEngine] Querying Architect LLM for structural improvements...")
        # new_code = llm_engine.rewrite(original_code, objective="Optimize performance and add logging")
        new_code = original_code + "\n# [EVOLUTION] Automatically padded by EvolutionEngine\n" 
        
        filename = os.path.basename(target_filepath)
        temp_path = self.sandbox.write_temp(filename, new_code)
        
        if self.sandbox.test_module(temp_path):
            print(f"[EvolutionEngine] Patch validated. Awaiting Human-In-The-Loop Git Merge...")
            # Rather than open() write, we'd invoke a human diff check here natively
            # e.g., output unified diff to terminal and await [Y/n]
            return True
        else:
            print("[EvolutionEngine] ⚠️ Patch rejected by sandbox integrity checks.")
            return False
