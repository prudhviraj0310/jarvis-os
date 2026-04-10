# Jarvis OS 

An AI-Native Operating System runtime built on Arch Linux.
Jarvis is not an app. It is a persistent daemon that continuously listens, perceives the Wayland compositor state, predicts workflows, and executes physical inputs as a true Presence layer above the Linux kernel.

## Features
- **Wake Word Interrupt**: Fully offline Vosk listener tied to ALSA that doesn't melt your CPU.
- **Continuous Perception**: Validates execution natively using Hyprland compositor hooks and raw screen parsing.
- **Behavioral Memory**: Learns your workflows and auto-chains repeated sequences instantly (0ms latency, bypassing the LLM).
- **Cinematic Interface**: Lightweight HUD overlays (`mako`/`libnotify`) and strict, priority-driven Voice outputs (`espeak`).
- **Complete Arch Base**: Comes out-of-the-box with `pacman`, `hyprland`, WiFi, and Pipewire so you can use it as a daily driver.

> **Read the [Full System Architecture Document](./ARCHITECTURE.md) to see how the Wayland perception and behavioral engines interlock.**

---

## 💿 Installation Instructions

### 1. Build the ISO
You must be on an Arch Linux distribution to compile the ISO:
```bash
sudo pacman -S archiso
./build_os.sh
```

### 2. Boot the ISO (Testing / VM)
Test the generated ISO immediately in QEMU:
```bash
qemu-system-x86_64 -cdrom out/jarvis-os-*.iso -m 8G -enable-kvm -smp 4
```

### 3. Install to Physical Hardware
1. Flash the ISO to a USB stick using `dd` or Rufus.
2. Boot your laptop from the USB.
3. Open the terminal (`SUPER + Enter`) and run the installer:
   ```bash
   sudo install_to_disk.sh
   ```
4. Follow the prompts. The installer will wipe the target disk, partition EFI/Root, deploy the Jarvis Core, and configure your systemd autologin services.

---

## 🛠️ The First Boot Experience

When you reboot into the physical install:
1. You will be auto-logged into the **Hyprland Desktop**.
2. Assuming you are connected to the internet (`nmcli dev wifi connect <SSID> password <PASS>`), Jarvis will perform a crucial **Initialization**:
   - Downloads and installs `Ollama` 
   - Pulls the `llama3` core AI weights
   - Fetches the `Vosk` offline acoustic model for the wake word
3. You will hear: *"Jarvis OS core downloaded. System ready."*
4. Say **"Jarvis"** to begin.
