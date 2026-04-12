import requests
import json
import os

class ExternalWorldAdapter:
    """
    Phase 25: External World Control Layer
    Allows Jarvis to step out of the desktop OS domain and interact with APIs, IoT, and Webhooks.
    """
    def __init__(self):
        # Load credentials safely
        self.telegram_token = os.getenv("JARVIS_TELEGRAM_BOT_TOKEN")
        self.home_assistant_url = os.getenv("JARVIS_HA_URL")
        self.home_assistant_token = os.getenv("JARVIS_HA_TOKEN")

    def register_to_router(self, router_instance):
        """
        Binds these external physical methods to the OS Tool Router.
        """
        router_instance.register("send_telegram", self.send_telegram_message)
        router_instance.register("control_smart_home", self.control_smart_home)
        print("[ExternalWorld] 🌍 IoT and API hooks registered natively.")

    def send_telegram_message(self, **kwargs) -> str:
        """Sends a notification to a predefined user on Telegram."""
        if not self.telegram_token:
            print("[ExternalWorld] Telegram Token missing.")
            return "Failed: Missing external API tokens."
            
        chat_id = kwargs.get("chat_id", os.getenv("JARVIS_TELEGRAM_OWNER_ID"))
        message = kwargs.get("message", "Jarvis automated ping.")
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            result = response.json()
            if result.get("ok"):
                print(f"[ExternalWorld] 📱 Sent to Telegram (Chat: {chat_id}): {message}")
                return "Success"
            else:
                print(f"[ExternalWorld] Telegram API error: {result}")
                return f"API Error: {result}"
        except Exception as e:
            print(f"[ExternalWorld] Telegram request failed: {e}")
            return f"API Failure: {e}"

    def control_smart_home(self, **kwargs) -> str:
        """Interacts with Home Assistant APIs to flip physical relays."""
        if not self.home_assistant_url:
            print("[ExternalWorld] Home Assistant URL missing.")
            return "Failed: HA not configured."
            
        entity_id = kwargs.get("entity_id")
        action = kwargs.get("action", "toggle")
        
        url = f"{self.home_assistant_url}/api/services/light/{action}"
        headers = {
            "Authorization": f"Bearer {self.home_assistant_token}",
            "Content-Type": "application/json"
        }
        
        try:
            payload = {"entity_id": entity_id}
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            print(f"[ExternalWorld] 💡 Smart Home '{entity_id}' -> '{action}' (HTTP {response.status_code})")
            return f"Smart Home {action}: HTTP {response.status_code}"
        except Exception as e:
            print(f"[ExternalWorld] Home Assistant request failed: {e}")
            return f"HA Failure: {e}"
