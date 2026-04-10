# 🚀 JARVIS OS — Boot It Tomorrow (Step-by-Step)

## What You Need
- A USB drive (8GB minimum)
- A laptop/PC to install Jarvis OS on
- WiFi connection

---

## Step 1: Download the Arch Linux ISO (on your Mac)

Go to: **https://archlinux.org/download/**

Scroll down to the mirror list, pick any mirror, download the `.iso` file (~900MB).

Or run this on your Mac terminal:
```bash
curl -LO https://geo.mirror.pkgbuild.com/iso/latest/archlinux-x86_64.iso
```

---

## Step 2: Flash the USB Drive (on your Mac)

1. Insert your USB drive
2. Find the disk name:
```bash
diskutil list
```
Look for your USB (e.g., `/dev/disk4`)

3. Unmount it:
```bash
diskutil unmountDisk /dev/disk4
```

4. Flash the ISO:
```bash
sudo dd if=archlinux-x86_64.iso of=/dev/rdisk4 bs=4m status=progress
```
⚠️ **Replace `disk4` with YOUR disk number. Wrong disk = data loss.**

5. Eject:
```bash
diskutil eject /dev/disk4
```

---

## Step 3: Boot the Target Machine from USB

1. Plug the USB into the laptop/PC where you want Jarvis OS
2. Turn on the machine and enter BIOS/Boot Menu:
   - Most laptops: Press **F2**, **F12**, **Del**, or **Esc** during boot
3. Select `USB` as boot device
4. You'll see `Arch Linux install medium` → Press Enter
5. Wait until you see a `root@archiso` prompt

---

## Step 4: Connect to WiFi

In the Arch live prompt, run:
```bash
iwctl
```
Then inside iwctl:
```
station wlan0 scan
station wlan0 get-networks
station wlan0 connect "YourWiFiName"
```
Type your WiFi password when prompted. Then:
```
exit
```

Verify internet:
```bash
ping -c 3 google.com
```

---

## Step 5: Install Jarvis OS (ONE COMMAND)

```bash
curl -fsSL https://raw.githubusercontent.com/prudhviraj0310/jarvis-os/master/install_jarvis_os.sh | bash
```

This will:
- Ask you which disk to install on
- Partition it (EFI + Swap + Root)
- Install Arch Linux + Hyprland desktop + all apps
- Clone and deploy the Jarvis AI runtime
- Configure auto-login, auto-start Hyprland
- Install GRUB bootloader
- Set up Jarvis to start on every boot

**Takes about 10-15 minutes depending on your internet.**

---

## Step 6: Reboot into Jarvis OS

When it says "INSTALLATION COMPLETE":
1. Remove the USB drive
2. Type: `reboot`
3. Your machine boots into Jarvis OS

---

## What Happens on First Boot

1. Screen goes to Hyprland desktop (tiling Wayland compositor)
2. Waybar shows at top: 🧠 Jarvis OS | Clock | WiFi | Battery
3. Jarvis auto-starts in background and:
   - Installs Ollama (AI engine)
   - Downloads llama3 model (~4GB, first time only)
   - Downloads Vosk wake word model (~50MB)
4. A notification pops up when ready

---

## Using Jarvis OS

| Keybind | Action |
|---|---|
| `Super + Enter` | Open Terminal |
| `Super + D` | App Launcher |
| `Super + F` | Firefox |
| `Super + E` | File Manager |
| `Super + Q` | Close Window |
| `Super + 1-5` | Switch Workspace |

### Interactive Mode (Terminal)
```bash
cd /opt/jarvis && python3 -m jarvis --mode interactive
```
Then type: `open firefox`, `what time is it`, etc.

### Wake Word (after Vosk downloads)
Just say **"Jarvis"** followed by your command.

---

## Login Credentials
- **Username:** `jarvis`
- **Password:** `jarvis`

---

## Connecting to WiFi (After Install)
```bash
nmcli device wifi list
nmcli device wifi connect "YourWiFi" password "YourPassword"
```

---

## Troubleshooting

**Black screen after boot?**
→ Press `Ctrl+Alt+F2` for a TTY terminal. Login as `jarvis`/`jarvis`.

**Hyprland won't start?**
→ Your GPU might need drivers. In TTY:
```bash
sudo pacman -S mesa vulkan-intel    # Intel GPU
sudo pacman -S mesa xf86-video-amdgpu  # AMD GPU
sudo pacman -S nvidia nvidia-utils     # NVIDIA (may need extra config)
```

**No sound?**
→ `wpctl status` to check Pipewire. `wpctl set-default <sink-id>` to select output.

**Jarvis not responding?**
→ Check logs: `journalctl --user -fu jarvis` or restart: `cd /opt/jarvis && python3 -m jarvis`
