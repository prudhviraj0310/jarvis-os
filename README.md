<p align="center">
  <h1 align="center">🧠 Jarvis OS</h1>
  <p align="center"><strong>An AI-Native Operating System with Persistent Presence</strong></p>
  <p align="center">
    <em>It doesn't wait for commands. It listens, predicts, acts, and learns.</em>
  </p>
  <p align="center">
    <a href="#-quickstart"><img src="https://img.shields.io/badge/Install-Guide-blue?style=for-the-badge" /></a>
    <a href="./ARCHITECTURE.md"><img src="https://img.shields.io/badge/Architecture-Docs-green?style=for-the-badge" /></a>
    <a href="#-verification"><img src="https://img.shields.io/badge/Tests-73%2F73%20Passed-brightgreen?style=for-the-badge" /></a>
  </p>
</p>

---

## What Is This?

Jarvis OS is a **bootable Linux operating system** where AI isn't an app you open — it's the operating system itself. Built on Arch Linux with the Hyprland Wayland compositor, it ships with an always-listening, always-learning AI daemon that can:

- **Hear you** → Offline wake word detection ("Jarvis, open YouTube")
- **See the screen** → Verifies what's visually focused before acting
- **Remember your habits** → Learns workflow patterns and replays them instantly
- **Control your machine** → Types, clicks, and navigates like a human would
- **Protect you** → Blocks catastrophic commands with heuristic safety gates

This is not a chatbot wrapper. This is a complete operating system you flash to a USB and boot.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    USER (Voice / Keyboard)           │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
        ┌──────▼──────┐        ┌──────▼──────┐
        │  Wake Word  │        │  Terminal   │
        │   (Vosk)    │        │   Input     │
        └──────┬──────┘        └──────┬──────┘
               │                      │
        ┌──────▼──────────────────────▼──────┐
        │         BEHAVIORAL ENGINE          │
        │   Pattern Match → 0ms Execution    │
        │   (Bypasses LLM if confident)      │
        └──────────────┬─────────────────────┘
                       │ Unknown pattern?
                ┌──────▼──────┐
                │  CONTEXT    │
                │  ENGINE     │
                │ L1+L2+L3   │
                │  Memory     │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │   OLLAMA    │
                │  Local LLM  │
                │  (llama3)   │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │  EXECUTION  │
                │   POLICY    │
                │ SAFE/MOD/CRIT│
                └──────┬──────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
   ┌──────▼──┐  ┌──────▼──┐  ┌─────▼─────┐
   │ System  │  │  Input  │  │  Screen   │
   │Commands │  │ Control │  │ Awareness │
   │ (bash)  │  │(ydotool)│  │(hyprctl)  │
   └─────────┘  └─────────┘  └───────────┘
          │            │            │
   ┌──────▼────────────▼────────────▼─────┐
   │          SENSORY OUTPUT              │
   │   Voice (espeak) + HUD (mako)       │
   │   + Sound Cues (ALSA wav)            │
   └──────────────────────────────────────┘
```

> **[Read the full Architecture Document →](./ARCHITECTURE.md)**

---

## ✨ Features

### 🎙️ Always-Listening Presence
Jarvis uses **Vosk** (50MB offline acoustic model) streaming from ALSA at 16kHz. No cloud. No GPU. Say "Jarvis" and it wakes up, strips your command, and executes it. A priority system prevents voice fatigue — critical alerts always speak, routine actions stay silent.

### 🧠 Zero-Latency Prediction
Every successful workflow is stored in the **MemPalace** (persistent JSON at `/var/lib/jarvis/`). The **Behavioral Engine** scans your history before touching the LLM. If it finds a pattern match above 75% confidence, it **bypasses the AI model entirely** and replays the exact sequence in 0ms.

### 👁️ Visual Perception Loop
Jarvis doesn't trust process lists. It queries the **Hyprland compositor** via `hyprctl` to verify which window is visually focused. If it opens Firefox but Firefox doesn't take compositor focus within 5 seconds, the pipeline **aborts safely** instead of blindly typing into the wrong window.

### 🛡️ Execution Safety
Every command flows through the **ExecutionPolicy** classifier:
| Risk Level | Example | Behavior |
|---|---|---|
| `SAFE` | `ls`, `echo`, `pwd` | Auto-execute |
| `MODERATE` | `rm file.txt`, `kill` | Prompt for confirmation |
| `CRITICAL` | `rm -rf /`, `mkfs`, `dd` | Hard block + Safe Mode |

Three consecutive failures trigger **Safe Mode** — all auto-execution suspends globally until manually overridden.

### 🖥️ Full Desktop OS
This isn't a terminal script. It's a complete Arch Linux distribution with:
- **Hyprland** — Tiling Wayland compositor with animations
- **Waybar** — Status bar (battery, WiFi, audio, clock, Jarvis indicator)
- **Firefox** — Web browser
- **Thunar** — File manager  
- **Kitty** — GPU-accelerated terminal
- **Wofi** — App launcher (`Super+D`)
- **Pipewire** — Full audio stack (speakers + microphone)
- **NetworkManager** — WiFi/Ethernet

---

## 🚀 Quickstart

### Option A: Install on Any Existing Linux Desktop (5 minutes)

This installs Jarvis as a **daemon on your current system** without replacing your OS.

```bash
# 1. Clone
git clone https://github.com/prudhviraj0310/jarvis-os.git
cd jarvis-os

# 2. Install dependencies
pip install -r requirements.txt
sudo pacman -S espeak-ng libnotify ydotool grim   # Arch
# sudo apt install espeak-ng libnotify-bin ydotool grim  # Ubuntu/Debian

# 3. Install Ollama (AI engine)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

# 4. Run interactively
python3 -m jarvis --mode interactive

# 5. Or install as a persistent daemon
bash systemd/install.sh
```

### Option B: Build the Full Bootable ISO (Advanced)

Requires an **Arch Linux** build machine:

```bash
# 1. Install archiso
sudo pacman -S archiso

# 2. Build the ISO
sudo ./build_os.sh

# 3. Test in QEMU
qemu-system-x86_64 -cdrom out/jarvis-os-*.iso -m 8G -enable-kvm -smp 4

# 4. Flash to USB for real hardware
sudo dd if=out/jarvis-os-*.iso of=/dev/sdX bs=4M status=progress
```

### Option C: Install to Bare Metal (From Live USB)

After booting the live USB:
```bash
# Open terminal: Super + Enter
sudo install_to_disk.sh
# Follow prompts → select target disk → reboot → done
```

---

## 🧪 Verification

Run the built-in integrity audit to verify every component:

```bash
python3 verify.py
```

```
══════════════════════════════════════════
  JARVIS OS — SYSTEM INTEGRITY AUDIT
══════════════════════════════════════════

  ✅ 73 passed | 0 failed | 0 warnings
  STATUS: ✅ JARVIS OS IS COMPLETE

══════════════════════════════════════════
```

---

## 📁 Project Structure

```
jarvis-os/
├── jarvis/                      # The AI Brain
│   ├── __main__.py              # Entry point (python3 -m jarvis)
│   ├── core/runtime.py          # Main orchestrator loop
│   ├── engine/
│   │   ├── llm.py               # Ollama wrapper with retry + JSON validation
│   │   ├── context.py           # 3-layer memory (L1 ephemeral, L2 session, L3 persistent)
│   │   └── behavior.py          # Predictive pattern engine (zero-latency bypass)
│   ├── system/
│   │   ├── execution.py         # Risk classifier (SAFE/MODERATE/CRITICAL)
│   │   ├── input_control.py     # Physical mouse/keyboard via ydotool
│   │   ├── screen.py            # Wayland compositor perception (hyprctl/grim)
│   │   └── kernel.py            # OS state snapshot
│   ├── interface/
│   │   ├── voice.py             # Priority-based TTS with fatigue control
│   │   ├── overlay.py           # Debounced HUD notifications (mako)
│   │   └── listener.py          # Offline wake word engine (Vosk + ALSA)
│   ├── plugins/
│   │   └── mempalace_adapter.py # Persistent workflow memory (/var/lib/jarvis/)
│   └── assets/                  # Sound cues (listening.wav, success.wav, error.wav)
├── iso/                         # Archiso profile (builds bootable .iso)
│   ├── profiledef.sh
│   ├── packages.x86_64
│   └── airootfs/                # Root filesystem overlay
│       ├── etc/skel/.config/    # Hyprland + Waybar configs
│       ├── etc/systemd/system/  # jarvis.service + firstboot + autologin
│       └── usr/local/bin/       # install_to_disk.sh + jarvis_firstboot.sh
├── systemd/                     # Daemon installer for existing Linux desktops
├── build_os.sh                  # One-command ISO builder
├── verify.py                    # 73-point integrity test suite
├── ARCHITECTURE.md              # Full system architecture with Mermaid diagrams
└── requirements.txt             # Python dependencies
```

---

## ⌨️ Keybinds (Hyprland Desktop)

| Key | Action |
|---|---|
| `Super + Enter` | Open Terminal |
| `Super + D` | App Launcher |
| `Super + Q` | Close Window |
| `Super + F` | Open Firefox |
| `Super + E` | Open File Manager |
| `Super + V` | Toggle Floating |
| `Super + 1-3` | Switch Workspace |

---

## 🔧 Requirements

| Component | Minimum |
|---|---|
| CPU | x86_64 |
| RAM | 8 GB (4GB for OS + 4GB for llama3) |
| Storage | 20 GB |
| Microphone | Required for wake word |
| GPU | Not required (CPU inference) |

---

## 🧬 How It Works (The Loop)

```
1. User speaks "Jarvis, open YouTube"
2. Vosk detects wake word → strips intent → fires interrupt
3. Behavioral Engine checks MemPalace for pattern match
4. IF match (confidence > 0.75): replay sequence instantly (0ms)
5. ELSE: enrich with 3-layer context → send to Ollama
6. Ollama returns JSON action sequence
7. ExecutionPolicy classifies risk of each action
8. System commands execute via bash
9. Input actions execute via ydotool (type/click/key)
10. Screen Awareness verifies visual result via hyprctl
11. Success → commit workflow to MemPalace for future prediction
12. Voice: "Done." | HUD: fades out | Sound: success.wav
```

---

## 📜 License

MIT

---

<p align="center">
  <strong>Built from scratch. Not a wrapper. Not a chatbot. An operating system.</strong>
</p>
