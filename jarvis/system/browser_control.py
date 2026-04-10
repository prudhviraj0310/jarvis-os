import os
import json
from pathlib import Path

class BrowserSessionManager:
    """
    JARVIS BROWSER SECURITY & SESSION INTERCEPTOR
    Since AI agents fail horribly at CAPTCHA and 2FA, this module handles launching a
    human-controlled UI for target architectures. It saves the authenticated cookie state,
    and then silently passes that state to headless agents in the future.
    """
    
    def __init__(self, session_dir="~/.config/jarvis/browser_sessions"):
        self.session_dir = Path(os.path.expanduser(session_dir))
        self.session_dir.mkdir(parents=True, exist_ok=True)
        # We ensure session configs are tightly permissioned
        os.chmod(self.session_dir, 0o700)

    def _get_session_path(self, domain: str) -> Path:
        """Returns the isolated json cookie path for a specific domain."""
        sanitized = domain.replace("https://", "").replace("http://", "").split("/")[0]
        return self.session_dir / f"{sanitized}.json"

    def has_session(self, domain: str) -> bool:
        """Determines if Jarvis holds an authenticated state for this target."""
        return self._get_session_path(domain).exists()

    def get_session_path(self, domain: str) -> str:
        """Returns the string path to the JSON state if it exists."""
        ext = self._get_session_path(domain)
        if ext.exists():
            return str(ext)
        return ""

    def authenticate(self, domain: str):
        """
        Pauses OS AI operation, spawns a visual Chromium browser, and waits for the user
        to login manually. Dumps the session upon exit.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[Jarvis ERROR] Playwright is not installed. Cannot authenticate.")
            return False

        print(f"\n[Jarvis Auth Overlay] Launching secure portal to {domain}")
        print("                      Please log in, complete any 2FA/CAPTCHA, and close the window.")
        
        session_path = self._get_session_path(domain)
        
        with sync_playwright() as p:
            # We open visibly so the human can interact
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                page.goto(domain)
            except Exception as e:
                print(f"[Jarvis Auth Overlay] Network failure accessing domain: {e}")
                browser.close()
                return False
                
            # We wait until the human closes the page physically
            print("[Jarvis Auth Overlay] Waiting for user to complete login flow...")
            try:
                page.wait_for_event("close", timeout=0) # 0 means wait forever until closed
            except Exception:
                pass # Expected close exception
                
            # Save the state explicitly to the vault
            context.storage_state(path=str(session_path))
            browser.close()
            
        # Secure the cookies from standard user read actions
        os.chmod(session_path, 0o600)
        print(f"\n[Jarvis Auth Overlay] Session state captured successfully. Returning control to pipeline.")
        return True
