import os
import shutil
import time
import threading

class HybridMemorySync:
    """
    Phase 26: Distributed Memory
    Syncs the local MemPalace JSON state into a cloud bucket or secondary secure storage
    to allow multi-device continuity (e.g. desktop Jarvis <-> mobile Jarvis).
    """
    def __init__(self, local_db="/var/lib/jarvis/mempalace_local.json", cloud_dir="~/.config/jarvis/cloud_sync/"):
        self.local_db = local_db
        # Mocking cloud directory as a local alias for architectural demonstration
        self.cloud_dir = os.path.expanduser(cloud_dir)
        os.makedirs(self.cloud_dir, exist_ok=True)
        self.is_syncing = False

    def sync_to_cloud(self):
        """Pushes local state to distributed cloud bucket."""
        if not os.path.exists(self.local_db):
            print("[SyncEngine] ⚠️ Local DB not found. Skipping backup.")
            return

        cloud_path = os.path.join(self.cloud_dir, "mempalace_shared_state.json")
        try:
            shutil.copy2(self.local_db, cloud_path)
            print(f"[SyncEngine] ☁️ Memory securely broadcasted to cloud layer.")
        except Exception as e:
            print(f"[SyncEngine] ❌ Cloud Sync Failed: {e}")

    def sync_from_cloud(self):
        """Pulls updated state from distributed cloud bucket."""
        cloud_path = os.path.join(self.cloud_dir, "mempalace_shared_state.json")
        if not os.path.exists(cloud_path):
            return
            
        try:
            # Simple conflict resolution: Always overwrite local for Phase 26 demo
            shutil.copy2(cloud_path, self.local_db)
            print(f"[SyncEngine] ⬇️ Local Memory updated from cloud layer.")
        except Exception as e:
            print(f"[SyncEngine] ❌ Cloud Sync Retrieval Failed: {e}")

    def start_background_daemon(self, interval=3600):
        """Runs the distributed sync periodically."""
        self.is_syncing = True
        
        def _loop():
            while self.is_syncing:
                self.sync_to_cloud()
                time.sleep(interval)
                
        t = threading.Thread(target=_loop, daemon=True)
        t.start()
        print("[SyncEngine] Distributed Hybrid Memory daemon online.")

    def stop(self):
        self.is_syncing = False
