#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "========================================================================="
echo "   ⚡ JARVIS OS 1.0 — MODERN GLASSMORPHIC LINUX & WAYLAND OS SHELL       "
echo "========================================================================="
echo "• Compositor: Hyprland / Modern Wayland (120 FPS Fluid Animations)"
echo "• Topbar: Waybar Holographic Cyber HUD (Attendance 87.5%, MIRA Telemetry)"
echo "• Browser: Chromium / Full GPU WebRTC & Real Microphone"
echo "• Audio Subsystem: PipeWire 44.1 kHz Duplex Audio Matrix"
echo "• Intelligence: MIRA Multi-Channel Gateway (8 Channels) & Model Router"
echo "========================================================================="

# Start background HUD server if not already running
if ! lsof -i :8080 >/dev/null 2>&1; then
    echo "Starting JARVIS HUD Server on port 8080..."
    python3 "$DIR/jarvis_hud/hud_server.py" >/dev/null 2>&1 &
    sleep 1
fi

echo "Launching Modern JARVIS OS Interface in Full Screen..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "http://localhost:8080"
else
    if command -v chromium >/dev/null 2>&1; then
        chromium --app="http://localhost:8080" --ozone-platform=wayland --enable-features=UseOzonePlatform &
    elif command -v google-chrome >/dev/null 2>&1; then
        google-chrome --app="http://localhost:8080" &
    elif command -v firefox >/dev/null 2>&1; then
        firefox --new-window "http://localhost:8080" &
    fi
fi

echo "✔ JARVIS OS Modern Edition is live at http://localhost:8080"
