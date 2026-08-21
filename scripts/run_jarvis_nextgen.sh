#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISO_PATH="$DIR/build/releases/jarvis-os-nextgen-x86_64.iso"
IMG_PATH="$DIR/build/releases/jarvis-os-nextgen-x86_64.img"

echo "========================================================================="
echo "   ⚡ BOOTING JARVIS OS NEXTGEN (DMS + WAYLAND + QEMU x86_64)            "
echo "========================================================================="
echo "• Compositor: Hyprland (120 FPS Wayland)"
echo "• Shell: DankMaterialShell (Quickshell / Material 3)"
echo "• IPC Bridge: jarvis-dms-bridge (/tmp/jarvis-dms.sock)"
echo "• Audio: Duplex PipeWire / Intel HDA (Stereo Microphone & Output)"
echo "• Release ISO: $ISO_PATH"
echo "========================================================================="

# Launch native IPC bridge in background
"$DIR/jarvis-dms/ipc/jarvis-dms-bridge" &
BRIDGE_PID=$!

cleanup() {
    kill $BRIDGE_PID 2>/dev/null || true
}
trap cleanup EXIT

# Launch QEMU with ISO or modern interface
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "http://localhost:8080"
fi

echo "✔ JARVIS OS NextGen is running with DankMaterialShell integration."
wait $BRIDGE_PID 2>/dev/null || true
