import os
import json
from pathlib import Path

class GuidanceEngine:
    """
    JARVIS ONBOARDING & EXPERIENCE LAYER
    Responsible for teaching the user about external AI tools, validating configurations,
    and running CLI setup wizards so the user is never lost.
    """
    
    TOOL_PROFILES = {
        "aider": {
            "description": "Aider is an AI pair programmer. It edits your codebase directly from the terminal.",
            "requirements": ["api_key"],
            "setup": "Enter your Anthropic or OpenAI API key",
            "env_inject": "ANTHROPIC_API_KEY", # Assuming Anthropic by default for Aider
            "risk": "MODERATE"
        },
        "openclaw": {
            "description": "OpenClaw is a headless automation edge agent. It controls browsers and runs shell workflows.",
            "requirements": ["browser_access"],
            "setup": "Grant permissions to control Chrome/Firefox headless driver",
            "env_inject": None,
            "risk": "HIGH"
        },
        "claude_code": {
            "description": "Claude Code is a heavy reasoning coding engine designed for complex codebase architecture.",
            "requirements": ["api_key"],
            "setup": "Enter your Anthropic API key",
            "env_inject": "ANTHROPIC_API_KEY",
            "risk": "MODERATE"
        },
        "n8n": {
            "description": "n8n is a visual workflow automation server. It triggers APIs and builds logic pipelines.",
            "requirements": ["service_running"],
            "setup": "Start the n8n background daemon",
            "env_inject": None,
            "risk": "LOW"
        }
    }

    def __init__(self):
        self.config_dir = Path(os.path.expanduser("~/.config/jarvis"))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.state_file = self.config_dir / "learning_state.json"
        self.keys_file = self.config_dir / "keys.json"
        
        self._load_state()
        self._load_keys()

    def _load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.learned_tools = json.load(f).get("learned_tools", [])
            except Exception:
                self.learned_tools = []
        else:
            self.learned_tools = []

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({"learned_tools": self.learned_tools}, f)

    def _load_keys(self):
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'r') as f:
                    self.keys = json.load(f)
            except Exception:
                self.keys = {}
        else:
            self.keys = {}

    def _save_keys(self):
        # Secure permissions for the keys file
        with open(self.keys_file, 'w') as f:
            json.dump(self.keys, f, indent=2)
        os.chmod(self.keys_file, 0o600)

    def inject_environment(self):
        """Injects loaded keys into the runtime OS environment dynamically."""
        for tool, key_val in self.keys.items():
            profile = self.TOOL_PROFILES.get(tool)
            if profile and profile["env_inject"]:
                os.environ[profile["env_inject"]] = key_val

    def validate_and_onboard(self, pipeline: list, voice_engine) -> bool:
        """
        Takes a DAG pipeline, intercepts it if tools are unconfigured or new,
        and proceeds through the 3 phases: Validate, Teach, Setup.
        """
        for node in pipeline:
            tool = node.get("tool")
            if tool == "system" or tool not in self.TOOL_PROFILES:
                continue # Native system tools require no onboarding
                
            profile = self.TOOL_PROFILES[tool]
            
            # STAGE 1: VALIDATE
            is_configured = self._is_configured(tool, profile)
                
            # STAGE 2: TEACH
            if tool not in self.learned_tools:
                print(f"\n[Jarvis Guidance] First time tool usage detected for: {tool}")
                voice_engine.speak(f"This will use {tool}.")
                
                print(f"==================================================")
                print(f" TOOL: {tool.upper()}")
                print(f" INFO: {profile['description']}")
                print(f" RISK: {profile['risk']}")
                print(f"==================================================")
                
                confirm = input(f"Do you want to proceed with using {tool}? [y/N]: ").strip().lower()
                if confirm != 'y':
                    print("\n[Jarvis] Execution cancelled by user.")
                    return False
                    
                # Mark as learned forever
                self.learned_tools.append(tool)
                self._save_state()

            # STAGE 3: SETUP
            if not is_configured:
                print(f"\n[Jarvis Setup] {tool} is not fully configured.")
                print(f"Requirement: {profile['setup']}")
                
                confirm = input("Would you like me to configure this for you now? [y/N]: ").strip().lower()
                if confirm != 'y':
                    print("\n[Jarvis] Setup aborted. Halting pipeline.")
                    return False
                
                if not self._run_setup_wizard(tool, profile):
                    return False

        return True

    def _is_configured(self, tool: str, profile: dict) -> bool:
        reqs = profile.get("requirements", [])
        if "api_key" in reqs:
            if tool not in self.keys or not self.keys[tool]:
                return False
        return True

    def _run_setup_wizard(self, tool: str, profile: dict) -> bool:
        reqs = profile.get("requirements", [])
        
        if "api_key" in reqs:
            api_key = input(f"[Setup] {profile['setup']}: ").strip()
            if not api_key:
                print("[Setup Error] API key cannot be empty.")
                return False
                
            self.keys[tool] = api_key
            self._save_keys()
            self.inject_environment()
            print(f"[Setup Complete] {tool} API key secured in memory.")
            
        elif "browser_access" in reqs:
            print("[Setup] OpenClaw requires underlying Wayland permissions.")
            print("[Setup Complete] Simulated permission grant successful.")
            
        elif "service_running" in reqs:
            print("[Setup] Attempting to start n8n daemon...")
            print("[Setup Complete] Simulated n8n daemon started globally.")

        return True

    def provide_help(self, tool_name: str, voice_engine) -> None:
        """Universal command hook for 'help with X'"""
        if tool_name not in self.TOOL_PROFILES:
            print(f"[Jarvis] I don't have onboarding documentation for '{tool_name}'.")
            return
            
        profile = self.TOOL_PROFILES[tool_name]
        print(f"\n================ JARVIS GUIDANCE ================")
        print(f" TOOL: {tool_name.upper()}")
        print(f" DESC: {profile['description']}")
        print(f" REQS: {', '.join(profile['requirements'])}")
        print(f"=================================================")
        voice_engine.speak(f"{tool_name} requires {len(profile['requirements'])} configuration steps.")
        
        if not self._is_configured(tool_name, profile):
            confirm = input(f"\n{tool_name} is currently UNCONFIGURED. Setup now? [y/N]: ").strip().lower()
            if confirm == 'y':
                self._run_setup_wizard(tool_name, profile)
        else:
            print(f"\n[Status] {tool_name} is CONFIGURED and ready for action.")
