#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KERNEL="$DIR/build/rootfs_staging/vmlinuz-virt"
INITRD="$DIR/build/initramfs-jarvis.cpio.gz"
ISO_PATH="$DIR/build/releases/jarvis-os-nextgen-x86_64.iso"

echo "========================================================================="
echo "   ⚡ LAUNCHING JARVIS OS NEXTGEN (REAL LINUX 6.6 KERNEL + DMS)          "
echo "========================================================================="
echo "• Kernel: $KERNEL (Linux 6.6.134-0-virt x86_64)"
echo "• Initramfs: $INITRD (Real 25MB CPIO Rootfs with DMS & IPC Bridge)"
echo "• Graphics: VirtIO-GPU / DRM KMS"
echo "• Audio: Intel HDA Duplex (Microphone & Speaker)"
echo "• Release ISO: $ISO_PATH"
echo "========================================================================="

if [ ! -f "$KERNEL" ] || [ ! -f "$INITRD" ]; then
    echo "Error: Kernel or Initrd missing. Running build script..."
    "$DIR/scripts/build_nextgen_iso.sh"
fi

# Boot real Linux kernel and initramfs in QEMU
qemu-system-x86_64 \
    -machine q35 \
    -m 2048 \
    -smp 2 \
    -kernel "$KERNEL" \
    -initrd "$INITRD" \
    -append "console=ttyS0 console=tty0 quiet" \
    -device virtio-gpu-pci \
    -device virtio-keyboard-pci \
    -device virtio-mouse-pci \
    -device intel-hda -device hda-duplex \
    -serial stdio
