#!/usr/bin/env bash

# Wait for internet
until ping -c1 8.8.8.8 &>/dev/null; do
    sleep 5
done

echo "[*] Jarvis First Boot Initialization..."

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull the core model (llama3 is standard local model)
systemctl start ollama
sleep 5
ollama run llama3 --keepalive 0 "" 

# Install pip dependencies for Jarvis
pip install --break-system-packages psutil vosk sounddevice

# Setup Vosk model
mkdir -p /opt/jarvis/vosk-model
cd /opt/jarvis
if [ ! -f "vosk-model-small-en-us-0.15.zip" ]; then
    wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    unzip -q vosk-model-small-en-us-0.15.zip
    mv vosk-model-small-en-us-0.15/* vosk-model/
    rm -rf vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15.zip
fi

# Mark complete
mkdir -p /var/lib/jarvis
touch /var/lib/jarvis/.firstboot_done

# Voice feedback to user (will play via Pipewire)
espeak-ng -v en-us -s 165 -p 35 "Jarvis OS core downloaded. System ready."
