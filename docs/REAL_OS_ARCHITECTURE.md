# JARVIS OS — Real Operating System Architecture & Transition Plan

**Status**: ACTIVE ARCHITECTURAL TRANSITION  
**Date**: August 21, 2026  

---

## 1. Phase 0 Audit Statement

> **"SerenityOS cannot host the required modern Linux graphical stack (Wayland, Quickshell, DankMaterialShell, Hyprland/niri, Qt6, and Chromium) without a major multi-year compatibility layer."**

* **Technical Reality**:
  * SerenityOS uses a custom 1990s-era `WindowServer` protocol with software CPU rendering.
  * DankMaterialShell (DMS) is fundamentally built upon the Linux Wayland layer-shell protocol (`wlr-layer-shell-v1`) and Qt6/Quickshell QML rendering.
  * In-tree SerenityOS `LibWeb` / `WebContent` crashes on modern CSS and web standards.
  * To run DankMaterialShell and modern hardware-accelerated browsers at 60–120 FPS with real duplex microphone audio, JARVIS OS must transition its underlying OS kernel and display server to a **Modern Linux 6.x / Wayland Foundation**.

---

## 2. Architecture Comparison

| Evaluation Dimension | Architecture A (SerenityOS + Compat Layer) | Architecture B (Linux 6.x + Wayland + DMS) | Winner |
| :--- | :--- | :--- | :--- |
| **Development Complexity** | Extremely High (Would require porting Wayland, Qt6, Quickshell, and DRM/KMS to Serenity) | Clean, deterministic, modular | **Architecture B** |
| **GPU & Mesa 3D Acceleration** | None (Software CPU rasterizer only) | Full DRM/KMS, Mesa, Vulkan, EGL (VirtIO-GPU VirGL / Bare-metal Intel/AMD/Nvidia) | **Architecture B** |
| **Audio Subsystem** | Basic fixed PCM (`/dev/audio/0`) | Full duplex PipeWire / WirePlumber with real mic stream & VAD | **Architecture B** |
| **Modern Web Browser** | Toy `LibWeb` (crashes on modern web) | Full Chromium / Firefox on Wayland with WebRTC and hardware video decoding | **Architecture B** |
| **DankMaterialShell Compatibility** | Incompatible | 100% Native Upstream (Quickshell QML + Go daemon) | **Architecture B** |
| **Hardware & Laptop Support** | Limited x86 legacy hardware | All modern x86_64 UEFI laptops, Wi-Fi, Bluetooth, battery management | **Architecture B** |
| **Preservation of JARVIS Brain** | Hard to connect to modern ML libraries | Direct C++26 socket IPC to `JarvisService`, `PolicyGate`, and `JournalService` | **Architecture B** |

### Selected Architecture: **ARCHITECTURE B**

---

## 3. The Real Boot Chain

```
                   UEFI Firmware (OVMF / EDK2 x86_64)
                                  │
                                  ▼
                   EFI Bootloader (systemd-boot / GRUB / Syslinux)
                                  │
                                  ▼
                   Linux Kernel 6.x (x86_64 with DRM/KMS)
                                  │
                                  ▼
                   initramfs (Hardware probe, device mount)
                                  │
                                  ▼
                   Root Filesystem (Linux Userspace + systemd / D-Bus)
                                  │
                                  ▼
                   Wayland Compositor (Hyprland / niri)
                                  │
                                  ▼
                   Quickshell Runtime & DankMaterialShell
                                  │
                                  ▼
                   JARVIS Native IPC Bridge (/tmp/jarvis-dms.sock)
                                  │
                                  ▼
                   JARVIS Services (JarvisService, PolicyGate, JournalService)
                                  │
                                  ▼
                   JARVIS OS Modern Desktop Experience (120 FPS)
```

---

## 4. Real Bootable Disk Image Specification

* **Partition Table**: GPT (GUID Partition Table)
* **Partition 1 (ESP)**: FAT32, `EFI/BOOT/BOOTX64.EFI`, Linux kernel (`vmlinuz`), initramfs.
* **Partition 2 (Root)**: Ext4, full Linux userspace with:
  * DRM/KMS, Mesa OpenGL/Vulkan
  * Wayland Compositor (Hyprland / niri)
  * Quickshell & DankMaterialShell (`third_party/DankMaterialShell`)
  * PipeWire duplex audio
  * Real Chromium Web Browser
  * Native JARVIS C++ services (`JarvisService`, `PolicyGate`, `JournalService`)

---

## 5. Machine Sovereignty & Policy Invariant

Under Architecture B, DankMaterialShell serves **strictly as the visual presentation shell**. The AI is **never** the execution authority:

```
User Command / Inbound Event
           ↓
     JARVIS Brain
           ↓
     PolicyGate
           ↓
  DMS Action Proposal Modal (Approve / Reject)
           ↓
     User Decision
           ↓
  Native Capability Dispatch
           ↓
  SHA-256 Block Ledger (/var/log/jarvis_journal.log)
```
