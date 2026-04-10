#!/usr/bin/env bash
set -e

echo "========================================"
echo " Jarvis OS Archiso Compiler"
echo "========================================"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

if ! command -v mkarchiso &> /dev/null; then
    echo "[ERROR] archiso is not installed."
    echo "        Run: sudo pacman -S archiso"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="/tmp/jarvis-work"
OUT_DIR="$SCRIPT_DIR/out"

# Clean up previous builds
rm -rf "$WORK_DIR"
mkdir -p "$OUT_DIR"

echo "[*] Copying Jarvis engine to ISO profile..."
# Make sure the target dir exists
mkdir -p "$SCRIPT_DIR/iso/airootfs/opt/jarvis"
# Copy all jarvis code except iso/ and out/ to the airootfs
cp -r "$SCRIPT_DIR/jarvis" "$SCRIPT_DIR/iso/airootfs/opt/jarvis/"
cp "$SCRIPT_DIR/requirements.txt" "$SCRIPT_DIR/iso/airootfs/opt/jarvis/"

# Ensure executable permissions on essential scripts
chmod +x "$SCRIPT_DIR/iso/airootfs/usr/local/bin/install_to_disk.sh" || true
chmod +x "$SCRIPT_DIR/iso/airootfs/usr/local/bin/jarvis_firstboot.sh" || true

echo "[*] Building ISO via mkarchiso (this will take a while)..."
mkarchiso -v -w "$WORK_DIR" -o "$OUT_DIR" "$SCRIPT_DIR/iso/"

echo ""
echo "========================================"
echo " Compilation Complete"
echo "========================================"
echo " Output ISO is located in: $OUT_DIR"
echo " Test with QEMU:"
echo " qemu-system-x86_64 -cdrom $OUT_DIR/jarvis-os-*.iso -m 4G -enable-kvm -smp 2"
echo "========================================"
