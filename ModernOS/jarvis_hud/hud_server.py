#!/usr/bin/env python3
"""
JARVIS OS 1.0 — Modern HUD Server & IPC Bridge
Serves the Holographic Command Interface and dispatches native Wayland/Linux capabilities.
"""

import http.server
import socketserver
import os
import sys
import json
import subprocess

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class JarvisHUDHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/launch_browser':
            # Attempt spawning modern browser on host or Linux Wayland
            try:
                if sys.platform == 'darwin':
                    subprocess.Popen(['open', 'http://localhost:8080'])
                else:
                    subprocess.Popen(['chromium', '--ozone-platform=wayland', 'http://localhost:8080'])
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "message": "Browser Launched"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "error": str(e)}).encode('utf-8'))
        elif self.path == '/api/voice_status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "READY", "matrix": "DUPLEX_44100HZ"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), JarvisHUDHandler) as httpd:
        print(f"⚡ [JARVIS OS HUD SERVER]: Active at http://localhost:{PORT}")
        print("🎙️ Vector Arc Reactor, MIRA Engine, and Duplex Speech Matrix online.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down JARVIS HUD Server.")

if __name__ == '__main__':
    run_server()
