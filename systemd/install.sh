#!/usr/bin/env bash
# Jarvis systemd User-Level Installer

SERVICE_NAME="jarvis.service"
USER_SYSTEMD_DIR="${HOME}/.config/systemd/user"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[*] Preparing to install Jarvis Runtime as a User-level service..."

# 1. Create target systemd directory if it doesn't exist
mkdir -p "${USER_SYSTEMD_DIR}"

# 2. Copy the service definition
cp "${PROJECT_DIR}/systemd/${SERVICE_NAME}" "${USER_SYSTEMD_DIR}/"
echo "[+] Copied ${SERVICE_NAME} to ${USER_SYSTEMD_DIR}"

# 3. Reload systemd daemon to recognize the new file
systemctl --user daemon-reload

# 4. Enable it to start automatically on login
systemctl --user enable ${SERVICE_NAME}

# 5. Start the service immediately
systemctl --user restart ${SERVICE_NAME}

echo "[+] Jarvis OS Runtime is now ALIVE and persistent."
echo "    Check logs using: journalctl --user -fu ${SERVICE_NAME}"
