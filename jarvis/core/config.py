import os
from pathlib import Path

class ConfigManager:
    """
    Manages loading API keys and ecosystem secrets.
    Looks for ~/.config/jarvis/.env and populates os.environ safely.
    """
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "jarvis"
        self.env_file = self.config_dir / ".env"
        self._ensure_config()
        self._load_env()
        
    def _ensure_config(self):
        if not self.config_dir.exists():
            try:
                self.config_dir.mkdir(parents=True, exist_ok=True)
                # Create a template env file
                with open(self.env_file, "w") as f:
                    f.write("# JARVIS OS SECRETS\n")
                    f.write("# GROQ_API_KEY=\n")
                    f.write("# OPENAI_API_KEY=\n")
            except Exception:
                pass
                
    def _load_env(self):
        try:
            import dotenv
            dotenv.load_dotenv(self.env_file)
        except ImportError:
            # Fallback simple parser if dotenv is missing
            if self.env_file.exists():
                with open(self.env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ[k.strip()] = v.strip()
                            
    @property
    def groq_key(self):
        return os.getenv("GROQ_API_KEY", "")
        
    @property
    def openai_key(self):
        return os.getenv("OPENAI_API_KEY", "")
