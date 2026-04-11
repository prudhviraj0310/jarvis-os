import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any

class FirecrawlAdapter:
    """
    Phase 17/18: Information Extraction Engine
    Makes messy internet structures perfectly understandable for the LLM.
    Supports both Cloud API (if key exists) and Self-Hosted Local Docker instances natively.
    """
    def __init__(self):
        # We fetch the key from the Jarvis Vault injected in Runtime
        self.api_key = os.environ.get("FIRECRAWL_API_KEY", "")
        self.local_url = "http://localhost:3002/v0/scrape"
        self.cloud_url = "https://api.firecrawl.dev/v0/scrape"
        
    def _extract_domain_name(self, target_url: str) -> str:
        try:
            return urllib.parse.urlparse(target_url).netloc
        except Exception:
            return "unknown_domain"

    def learn_domain(self, target_url: str) -> Dict[str, Any]:
        """
        Executes headless extraction. Returns raw sanitized markdown.
        """
        print(f"\n[Firecrawl Engine] Initiating high-fidelity extraction on: {target_url}")
        
        payload = json.dumps({"url": target_url}).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
        endpoint = self.local_url
        if self.api_key:
            endpoint = self.cloud_url
            headers['Authorization'] = f'Bearer {self.api_key}'
            print("                   Using Cloud API route.")
        else:
            print("                   Using Self-Hosted Local API route.")

        try:
            req = urllib.request.Request(endpoint, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            if result.get("success"):
                markdown = result.get("data", {}).get("markdown", "")
                title = result.get("data", {}).get("metadata", {}).get("title", self._extract_domain_name(target_url))
                
                print(f"[Firecrawl Engine] Ingestion Complete. {len(markdown)} bytes recovered.")
                return {
                    "source": target_url,
                    "title": title,
                    "markdown": markdown,
                    "status": "success"
                }
            else:
                print(f"[Firecrawl Engine] Ingestion failed inside API: {result.get('error')}")
                return {"status": "error"}
                
        except urllib.error.URLError as e:
            # If the user doesn't have local firecrawl hosting up, return error.
            print(f"[Firecrawl Engine ERROR] Connection failed. Is Firecrawl reachable at {endpoint}?")
            return {"status": "error"}
        except Exception as e:
            print(f"[Firecrawl Engine ERROR] Extraction faulted: {e}")
            return {"status": "error"}
