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

class StatefulBrowserProxy:
    """
    Phase 13: Digital Operator Core
    Allows Jarvis to directly orchestrate website flows inherently without relying on external bots.
    Loads Playwright persistently and routes commands in sequential pipelines.
    """
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.is_active = False

    def _ensure_active(self, domain: str = ""):
        if self.is_active:
            return
            
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            
            # Check for existing session from Phase 14 Vault
            session_mgr = BrowserSessionManager()
            session_path = session_mgr.get_session_path(domain)
            
            if session_path:
                print(f"[Jarvis Browser Proxy] Booting Headless Context (Authenticating with {os.path.basename(session_path)})")
                self.context = self.browser.new_context(storage_state=session_path)
            else:
                print(f"[Jarvis Browser Proxy] Booting Headless Context (Anonymous)")
                self.context = self.browser.new_context()
                
            self.page = self.context.new_page()
            self.is_active = True
        except Exception as e:
            print(f"[Jarvis Browser Proxy] Initialization failure: {e}")

    def execute_action(self, action: dict) -> bool:
        """
        Executes granular atomic actions mapped from LLM pipeline.
        Supported methods: open_url, click_element, type_text, save_session
        """
        method = action.get("method")
        
        try:
            if method == "open_url":
                target = action.get("target")
                self._ensure_active(target)
                self.page.goto(target)
                print(f"         [Browser] Navigated to {target}")
                return True
                
            elif method == "click_element":
                selector = action.get("target")
                self.page.click(selector)
                print(f"         [Browser] Clicked {selector}")
                return True
                
            elif method == "type_text":
                selector = action.get("target")
                text = action.get("payload")
                self.page.fill(selector, text)
                print(f"         [Browser] Typed content into {selector}")
                return True
                
            elif method == "save_session":
                domain = action.get("target")
                session_mgr = BrowserSessionManager()
                session_path = session_mgr._get_session_path(domain)
                self.context.storage_state(path=str(session_path))
                os.chmod(session_path, 0o600)
                print(f"         [Browser/Vault] Live session stored securely.")
                return True
                
            print(f"         [Browser] Unrecognized method: {method}")
            return False
            
        except Exception as e:
            print(f"         [Browser] Failure executing {method}: {e}")
            return False

    def close(self):
        if not self.is_active:
            return
            
        print("[Jarvis Browser Proxy] Tearing down headless context...")
        try:
            if self.page: self.page.close()
            if self.context: self.context.close()
            if self.browser: self.browser.close()
            if self.playwright: self.playwright.stop()
        except Exception as e:
            print(f"[Jarvis Browser Proxy] Teardown error: {e}")
            
        self.is_active = False
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
