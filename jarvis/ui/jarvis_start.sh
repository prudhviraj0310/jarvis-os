#!/bin/bash
# ═══════════════════════════════════════════════════════
# JARVIS OS — System Startup Script
# ═══════════════════════════════════════════════════════
# Launched automatically by Hyprland on every boot.
# Orchestrates: Boot animation → Theme deployment → Engine start
#
# exec-once = /usr/local/bin/jarvis-start.sh

set -e

JARVIS_DIR="/opt/jarvis"
CONFIG_DIR="$HOME/.config/jarvis"
LOG_DIR="$CONFIG_DIR/logs"
mkdir -p "$CONFIG_DIR" "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_DIR/boot.log"
}

# ═══════════════════════════════════════════════════════
# PHASE 1: CINEMATIC BOOT ANIMATION
# ═══════════════════════════════════════════════════════
log "Phase 1: Boot animation..."

# Play the arc reactor boot sequence (fullscreen, ~8 seconds)
if [ -f "$JARVIS_DIR/jarvis/ui/boot_animation.py" ]; then
    python3 "$JARVIS_DIR/jarvis/ui/boot_animation.py" 2>/dev/null &
    BOOT_PID=$!
    # Wait for animation to finish (max 12 seconds)
    timeout 12 wait $BOOT_PID 2>/dev/null || true
fi

# ═══════════════════════════════════════════════════════
# PHASE 2: DEPLOY THEME
# ═══════════════════════════════════════════════════════
log "Phase 2: Deploying visual theme..."

# Install Waybar theme
WAYBAR_DIR="$HOME/.config/waybar"
mkdir -p "$WAYBAR_DIR"
if [ -f "$JARVIS_DIR/jarvis/ui/themes/waybar_config.json" ]; then
    cp "$JARVIS_DIR/jarvis/ui/themes/waybar_config.json" "$WAYBAR_DIR/config"
    cp "$JARVIS_DIR/jarvis/ui/themes/waybar.css" "$WAYBAR_DIR/style.css"
    log "  Waybar theme deployed."
fi

# Restart Waybar with new theme
pkill waybar 2>/dev/null || true
sleep 0.3
waybar &

# ═══════════════════════════════════════════════════════
# PHASE 3: INSTALL DEPENDENCIES (First boot only)
# ═══════════════════════════════════════════════════════

# Python packages
if ! python3 -c "import faster_whisper" 2>/dev/null; then
    log "Phase 3: First boot — installing Python deps..."
    pip install --break-system-packages vosk sounddevice psutil \
        pytesseract Pillow mss requests faster-whisper piper-tts onnxruntime 2>>"$LOG_DIR/pip.log" || true
fi

# Ollama (AI backend)
if ! command -v ollama &>/dev/null; then
    log "Phase 3: Installing Ollama..."
    notify-send -a "Jarvis OS" "First Boot" "Setting up AI engine — this takes a few minutes."
    curl -fsSL https://ollama.com/install.sh | sh 2>>"$LOG_DIR/ollama.log"
    systemctl enable --now ollama 2>/dev/null || true
    sleep 3
    ollama pull llama3 &
    ollama pull llava &
    log "  Ollama installed. Pulling llama3 and llava in background (vision + logic)."
fi

# Vosk model (offline speech recognition)
if [ ! -d "$JARVIS_DIR/vosk-model" ]; then
    log "Phase 3: Downloading Vosk wake word model..."
    cd "$JARVIS_DIR"
    wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip 2>/dev/null
    if [ -f "vosk-model-small-en-us-0.15.zip" ]; then
        unzip -q vosk-model-small-en-us-0.15.zip
        mv vosk-model-small-en-us-0.15 vosk-model
        rm -f vosk-model-small-en-us-0.15.zip
        log "  Vosk model installed."
    fi
fi

# ═══════════════════════════════════════════════════════
# PHASE 4: LAUNCH JARVIS ENGINE
# ═══════════════════════════════════════════════════════
log "Phase 4: Starting Jarvis daemon..."

cd "$JARVIS_DIR"

# Start the HUD overlay (transparent layer shell)
python3 -c "
from jarvis.ui.hud import JarvisHUD
hud = JarvisHUD()
hud.run()
" &>/dev/null &
HUD_PID=$!
log "  HUD overlay active (PID: $HUD_PID)"

# Start the main Jarvis presence daemon
python3 -m jarvis --mode daemon &>>"$LOG_DIR/daemon.log" &
DAEMON_PID=$!
log "  Daemon active (PID: $DAEMON_PID)"

# Write PIDs for management
echo "$HUD_PID" > "$CONFIG_DIR/hud.pid"
echo "$DAEMON_PID" > "$CONFIG_DIR/daemon.pid"

# ═══════════════════════════════════════════════════════
# PHASE 5: ANNOUNCE
# ═══════════════════════════════════════════════════════
sleep 2
notify-send -a "Jarvis OS" "Systems Online" "All neural pathways active. Ready for commands."
espeak-ng "All systems online. Ready for your commands, sir." 2>/dev/null &

log "Boot complete. All systems nominal."
