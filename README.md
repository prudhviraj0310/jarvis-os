# ⚡ JARVIS OS — Holographic Cognitive Operating System

<div align="center">

```
   ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗     ██████╗ ███████╗
   ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ██╔═══██╗██╔════╝
   ██║███████║██████╔╝██║   ██║██║███████╗    ██║   ██║███████╗
   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║    ██║   ██║╚════██║
█████║██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ╚██████╔╝███████║
╚════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝
```

**An Independent, Self-Booting 64-bit Graphical Operating System with a Holographic Tactical HUD, Native IPC Capability Engine, and Cryptographic Syscall Shield.**

[![Architecture](https://img.shields.io/badge/Architecture-x86__64%20UEFI%2FBIOS-00e5ff.svg?style=for-the-badge)](#)
[![Kernel](https://img.shields.io/badge/Kernel-Custom%20C%2B%2B%20Micro--Unix-00ffd5.svg?style=for-the-badge)](#)
[![UI](https://img.shields.io/badge/UI-Holographic%20Arc%20Reactor%20HUD-ffb703.svg?style=for-the-badge)](#)
[![Security](https://img.shields.io/badge/Security-SHA--256%20Chained%20Journal-ff2a5f.svg?style=for-the-badge)](#)

</div>

---

## 🌟 What is JARVIS OS?

**JARVIS OS** is an independent, custom-built 64-bit operating system designed from the metal up. It is **not** a Linux distribution and **not** a browser wrapper — it boots its **own compiled C++ kernel**, initializes its **own device tree & virtual memory manager**, and renders its **own native hardware-composited Cyber Glass desktop & Tactical Holographic HUD**.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    JARVIS OS HOLOGRAPHIC COMMAND MATRIX                         │
├──────────────────────────┬─────────────────────────────┬────────────────────────┤
│   TACTICAL PROTOCOLS     │    [ ARC REACTOR CORE ]     │    DEFENSE VECTORS     │
│   ⚡ System Diagnostics  │    * 16 Rotating Spokes *   │    Syscall: ENFORCED   │
│   🛡️ Ultimate Shield     │    * Concentric Rings *     │    Journal: CHAINED    │
│   🔒 DEFCON-1 Lockdown   │    * Dynamic Audio Wave *   │    VFS: VERIFIED       │
│   📜 SHA-256 Journal     │    * Glowing Cyan Orb *     │    Frequency: 60 FPS   │
├──────────────────────────┴─────────────────────────────┴────────────────────────┤
│   🎙️ Voice Console:  [ Speak or type commands (status, shield, lockdown)... ]   │
├─────────────────────────────────────────────────────────────────────────────────┤
│   >>> [JARVIS OS Holographic Core Online]                                       │
│   Neural Interface & Ultimate Shield Subsystem: ACTIVE                          │
│   IPC Portal: /tmp/portal/jarvis (Operational)                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ Core Architecture

### 1. ⚙️ Custom x86_64 Kernel & Bootstrapping
* **Boot Protocols**: Direct UEFI PE32+ application boot (`Kernel.efi`) and Multiboot BIOS compatibility.
* **Kernel Core**: Preemptive multithreading scheduler, SMP multicore initialization, x86_64 paging matrix, POSIX-compatible VFS (Ext2FS, ProcFS, SysFS, DevPtsFS, RAMFS).
* **Identity**: Native `sys$uname` returning `sysname = "JARVIS OS"`.

### 2. ⚛️ Holographic Arc Reactor HUD (`Userland/Applications/JarvisAssistant/`)
* **Vector Engine**: Real-time 60 FPS animated vector Arc Reactor rendered with `GUI::Painter` directly to the display.
* **Dynamic Modulations**: 16 counter-rotating spokes, concentric plasma rings, and audio-reactive sine waveforms.
* **Threat Matrix Reaction**: Dynamically shifts visual theme and alerts from **Nominal Cyan** (`#00e5ff`) to **DEFCON-1 Red Alert** (`#ff2a5f`).

### 3. 🛡️ The Ultimate Shield & Cryptographic Journal Subsystem
* **IPC Capability Dispatcher (`JarvisService`)**: Typed IPC daemon listening at `/tmp/portal/jarvis` with multi-tier policy gating.
* **Cryptographic Block Hash Ledger (`JournalService`)**: Cryptographically block-hashes every capability execution with SHA-256 and records it to `/var/log/jarvis_journal.log`.
* **DEFCON Lockdown Protocol**: One-click and voice-triggered lockdown restricting unverified kernel syscalls.

### 4. 🪟 Cyber Glass Window Decorator & Compositor (`LibGfx/GlassWindowTheme.cpp`)
* **Obsidian Aero Gradients**: Deep space glass titlebars (`#080e18` to `#122036`).
* **Glowing Neon Accents**: Glowing cyan window borders (`#00e5ff`) and centered high-tech typography.
* **Modern Taskbar**: Replaced legacy 90s widgets with `⚡ JARVIS` telemetry launch tray.

---

## 🚀 Building & Running JARVIS OS

### Prerequisites
* **Operating System**: macOS (Apple Silicon / Intel) or Linux (x86_64)
* **Host Toolchain**: `cmake`, `ninja`, `python3`, `qemu-system-x86_64`, `e2fsprogs`, `xorriso`, `sgdisk`

### 1. Build the OS Source Tree
```bash
# Build the entire kernel, userspace daemons, and holographic HUD
./Meta/serenity.sh build x86_64 GNU
```

### 2. Launch Live in QEMU
```bash
# Boot the operating system with hardware devices and audio support
./Meta/serenity.sh run x86_64 GNU
```

---

## 📦 Physical Machine Boot Artifacts

JARVIS OS builds physical, verified boot artifacts ready for bare-metal flashing:

```bash
# Generate verified GPT disk images and bootable ISOs
python3 Meta/make-release-image.py
```

Generated in `build/releases/`:
* **`jarvis-os-x86_64.img`**: Raw GPT disk image with 64 MB FAT32 ESP (`/EFI/BOOT/BOOTX64.EFI`) + 1.4 GB Ext2 Root filesystem. Flashable directly to USB drives via Rufus or Etcher.
* **`jarvis-os-x86_64.iso`**: Hybrid El Torito bootable ISO for physical laptops and virtual machines.
* **`Kernel.efi`**: Standalone PE32+ 64-bit UEFI application.

---

## ⌨️ CLI Capability Interface

Interact with the JARVIS subsystem directly from the terminal:

```bash
# Query overall system health and defense status
jarvis health

# Run diagnostics capability
jarvis exec system.diagnostics

# Query active process matrix
jarvis exec system.processes

# Check cryptographic defense shield status
jarvis exec security.shield_status

# Engage DEFCON-1 system lockdown
jarvis exec security.lockdown
```

---

## 📜 License

JARVIS OS is distributed under the **BSD 2-Clause License**.
See [LICENSE](LICENSE) for details.
