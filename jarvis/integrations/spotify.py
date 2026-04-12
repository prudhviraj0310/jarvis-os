import subprocess
import json

class SpotifyIntegration:
    """
    Phase D: The Ecosystem — Spotify/Media Control
    Uses playerctl to interface with MPRIS DBus compatible players on Linux.
    Provides background control over music playback seamlessly.
    """
    def play_pause(self) -> str:
        res = subprocess.run(["playerctl", "play-pause"], capture_output=True, text=True)
        if res.returncode == 0:
            return "Toggled play/pause."
        return f"Failed to control media: {res.stderr.strip()}"
        
    def next_track(self) -> str:
        res = subprocess.run(["playerctl", "next"], capture_output=True, text=True)
        return "Skipped to next track." if res.returncode == 0 else f"Error: {res.stderr.strip()}"
        
    def prev_track(self) -> str:
        res = subprocess.run(["playerctl", "previous"], capture_output=True, text=True)
        return "Going to previous track." if res.returncode == 0 else f"Error: {res.stderr.strip()}"

    def status(self) -> str:
        res = subprocess.run(["playerctl", "metadata", "--format", "{{artist}} - {{title}} ({{status}})"], 
                             capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return f"Currently playing: {res.stdout.strip()}"
        return "No media is currently active."

    def execute_command(self, cmd_data: dict) -> str:
        """Entry point for VoiceStream's <call:media...> interception."""
        action = cmd_data.get("action", "")
        if "play" in action or "pause" in action or "toggle" in action:
            return self.play_pause()
        elif "next" in action or "skip" in action:
            return self.next_track()
        elif "prev" in action or "back" in action:
            return self.prev_track()
        elif "status" in action or "what" in action:
            return self.status()
        return "Unknown media action."
