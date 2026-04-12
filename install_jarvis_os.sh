#!/usr/bin/env bash
#
# ╔═══════════════════════════════════════════════════════╗
# ║           JARVIS OS — One-Command Installer           ║
# ║   Boot from Arch Linux USB → Run this → Reboot        ║
# ╚═══════════════════════════════════════════════════════╝
#
# Usage:
#   1. Boot from official Arch Linux USB
#   2. Connect to WiFi:  iwctl station wlan0 connect <SSID>
#   3. Run: curl -fsSL https://raw.githubusercontent.com/prudhviraj0310/jarvis-os/master/install_jarvis_os.sh | bash
#
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "  ╔═══════════════════════════════════════╗"
    echo "  ║         JARVIS OS INSTALLER           ║"
    echo "  ║     AI-Native Operating System        ║"
    echo "  ╚═══════════════════════════════════════╝"
    echo -e "${NC}"
}

info()  { echo -e "  ${CYAN}[*]${NC} $1"; }
ok()    { echo -e "  ${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "  ${YELLOW}[!]${NC} $1"; }
err()   { echo -e "  ${RED}[✗]${NC} $1"; exit 1; }
ask()   { echo -e "  ${YELLOW}[?]${NC} $1"; }

banner

# ── Pre-flight checks ──
[ "$EUID" -ne 0 ] && err "Run as root. Use: sudo bash install_jarvis_os.sh"

info "Checking internet connection..."
ping -c 1 archlinux.org &>/dev/null || err "No internet. Connect first: iwctl station wlan0 connect <SSID>"
ok "Internet connected"

# ── Disk selection ──
echo ""
info "Available disks:"
echo ""
lsblk -d -o NAME,SIZE,MODEL | grep -v "loop\|sr\|ram"
echo ""
ask "Enter target disk (e.g., sda or nvme0n1): "
read -r DISK_NAME
DISK="/dev/$DISK_NAME"

[ ! -b "$DISK" ] && err "Disk $DISK not found"

echo ""
warn "THIS WILL ERASE ALL DATA ON $DISK"
ask "Type 'YES' to continue: "
read -r CONFIRM
[ "$CONFIRM" != "YES" ] && err "Aborted."

# ── Detect disk type (NVMe vs SATA) ──
if [[ "$DISK" == *"nvme"* ]]; then
    PART1="${DISK}p1"
    PART2="${DISK}p2"
    PART3="${DISK}p3"
else
    PART1="${DISK}1"
    PART2="${DISK}2"
    PART3="${DISK}3"
fi

# ── Partition ──
info "Partitioning $DISK..."
wipefs -a "$DISK" &>/dev/null
parted -s "$DISK" mklabel gpt
parted -s "$DISK" mkpart "EFI"  fat32  1MiB    513MiB
parted -s "$DISK" set 1 esp on
parted -s "$DISK" mkpart "SWAP" linux-swap 513MiB  4GiB
parted -s "$DISK" mkpart "ROOT" ext4   4GiB    100%
ok "Partitioned: EFI (512M) + Swap (3.5G) + Root (rest)"

# ── Format ──
info "Formatting..."
mkfs.fat -F32 "$PART1" &>/dev/null
mkswap "$PART2" &>/dev/null
swapon "$PART2"
mkfs.ext4 -F "$PART3" &>/dev/null
ok "Formatted"

# ── Mount ──
mount "$PART3" /mnt
mkdir -p /mnt/boot
mount "$PART1" /mnt/boot
ok "Mounted"

# ── Install base system ──
info "Installing Arch Linux base system (this takes 5-10 minutes)..."
pacstrap -K /mnt \
    base linux linux-firmware \
    intel-ucode amd-ucode \
    networkmanager \
    git wget curl vim nano sudo \
    grub efibootmgr \
    wayland hyprland waybar kitty ttf-jetbrains-mono-nerd rofi mako libnotify \
    pipewire pipewire-pulse wireplumber espeak-ng xdg-desktop-portal-hyprland \
    polkit-kde-agent qt5-wayland qt6-wayland xdotool xprintidle playerctl grim slurp wl-clipboard \
    firefox thunar \
    pipewire pipewire-pulse pipewire-alsa wireplumber \
    espeak-ng libnotify \
    bluez bluez-utils brightnessctl \
    python python-pip python-psutil \
    ttf-fira-code noto-fonts \
    polkit

ok "Base system installed"

# ── Generate fstab ──
genfstab -U /mnt >> /mnt/etc/fstab
ok "fstab generated"

# ── Clone Jarvis OS into the system ──
info "Deploying Jarvis OS intelligence core..."
arch-chroot /mnt git clone https://github.com/prudhviraj0310/jarvis-os.git /opt/jarvis 2>/dev/null || true
ok "Jarvis core deployed to /opt/jarvis"

# ── Configure inside chroot ──
info "Configuring system..."

arch-chroot /mnt /bin/bash <<'CHROOT_END'

# ── Timezone & Locale ──
ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
hwclock --systohc
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# ── Hostname ──
echo "jarvis" > /etc/hostname
cat > /etc/hosts <<EOF
127.0.0.1   localhost
::1         localhost
127.0.1.1   jarvis.localdomain jarvis
EOF

# ── Create user ──
useradd -m -G wheel,audio,video,input -s /bin/bash jarvis
echo "jarvis:jarvis" | chpasswd
echo "root:jarvis" | chpasswd
echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel

# ── GRUB Bootloader ──
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=JARVIS --removable 2>/dev/null || \
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=JARVIS

# ── GRUB Theme (Iron Man boot screen) ──
python3 /opt/jarvis/jarvis/ui/grub_theme.py --install 2>/dev/null || true
if [ -f /boot/grub/themes/jarvis/theme.txt ]; then
    sed -i 's|^#*GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/jarvis/theme.txt"|' /etc/default/grub
    echo 'GRUB_TIMEOUT_STYLE=menu' >> /etc/default/grub
    echo 'GRUB_TIMEOUT=5' >> /etc/default/grub
fi

grub-mkconfig -o /boot/grub/grub.cfg

# ── Enable core services ──
systemctl enable NetworkManager
systemctl enable bluetooth

# ── Auto-login on tty1 ──
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf <<EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty -o '-p -f -- \\u' --noclear --autologin jarvis - \$TERM
EOF

# ── Auto-start Hyprland on login ──
cat > /home/jarvis/.bash_profile <<'EOF'
if [ -z "${WAYLAND_DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
    export QT_QPA_PLATFORM="wayland;xcb"
    export GDK_BACKEND="wayland,x11"
    export MOZ_ENABLE_WAYLAND=1
    exec Hyprland
fi
EOF
chown jarvis:jarvis /home/jarvis/.bash_profile

# ── Hyprland config ──
mkdir -p /home/jarvis/.config/hypr
cat > /home/jarvis/.config/hypr/hyprland.conf <<'EOF'
monitor=,preferred,auto,auto

exec-once = waybar
exec-once = mako
exec-once = bash /opt/jarvis/jarvis/ui/jarvis_start.sh

env = XCURSOR_SIZE,24

input {
    kb_layout = us
    follow_mouse = 1
    touchpad {
        natural_scroll = yes
    }
    sensitivity = 0
}

general {
    gaps_in = 5
    gaps_out = 15
    border_size = 2
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.inactive_border = rgba(595959aa)
    layout = dwindle
}

decoration {
    rounding = 10
    drop_shadow = yes
    shadow_range = 4
    shadow_render_power = 3
    col.shadow = rgba(1a1a1aee)
}

animations {
    enabled = yes
    bezier = ease, 0.05, 0.9, 0.1, 1.05
    animation = windows, 1, 7, ease
    animation = windowsOut, 1, 7, default, popin 80%
    animation = fade, 1, 7, default
    animation = workspaces, 1, 6, default
}

dwindle {
    pseudotile = yes
    preserve_split = yes
}

$mainMod = SUPER
bind = $mainMod, Return, exec, kitty
bind = $mainMod, Q, killactive,
bind = $mainMod, M, exit,
bind = $mainMod, E, exec, thunar
bind = $mainMod, V, togglefloating,
bind = $mainMod, D, exec, wofi --show drun
bind = $mainMod, F, exec, firefox
bind = $mainMod, left, movefocus, l
bind = $mainMod, right, movefocus, r
bind = $mainMod, up, movefocus, u
bind = $mainMod, down, movefocus, d
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
bind = $mainMod, 4, workspace, 4
bind = $mainMod, 5, workspace, 5
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2
bind = $mainMod SHIFT, 3, movetoworkspace, 3
EOF
chown -R jarvis:jarvis /home/jarvis/.config

# ── Waybar config ──
mkdir -p /home/jarvis/.config/waybar
cat > /home/jarvis/.config/waybar/config <<'EOF'
{
    "layer": "top",
    "position": "top",
    "height": 30,
    "modules-left": ["custom/jarvis", "hyprland/workspaces"],
    "modules-center": ["clock"],
    "modules-right": ["pulseaudio", "network", "battery", "tray"],
    "custom/jarvis": {
        "format": "🧠 Jarvis OS",
        "tooltip": false
    },
    "clock": { "format": "{:%H:%M  %a %b %d}" },
    "battery": {
        "format": "{capacity}% {icon}",
        "format-icons": ["", "", "", "", ""]
    },
    "network": {
        "format-wifi": "{essid} ",
        "format-disconnected": "Disconnected ⚠"
    },
    "pulseaudio": {
        "format": "{volume}% {icon}",
        "format-icons": { "default": ["", ""] }
    }
}
EOF

cat > /home/jarvis/.config/waybar/style.css <<'EOF'
* { font-family: "FiraCode Nerd Font", monospace; font-size: 13px; }
window#waybar { background-color: rgba(20, 20, 30, 0.92); color: #ffffff; border-bottom: 2px solid rgba(51, 204, 255, 0.4); }
#custom-jarvis { background-color: #2980b9; color: white; border-radius: 5px; padding: 0 10px; margin: 4px; }
#workspaces button { padding: 0 5px; color: #ffffff; }
#workspaces button.active { background-color: #64727D; }
#clock, #battery, #network, #pulseaudio, #tray { padding: 0 10px; }
EOF
chown -R jarvis:jarvis /home/jarvis/.config/waybar

# ── Jarvis startup script ──
cat > /usr/local/bin/jarvis-start.sh <<'STARTUP'
#!/bin/bash
# Wait for Wayland to be ready
sleep 2

# Install pip dependencies if not present
pip install --break-system-packages vosk sounddevice 2>/dev/null

# Check if Ollama is installed
if ! command -v ollama &>/dev/null; then
    notify-send -a "Jarvis OS" "First Boot" "Setting up AI engine... This takes a few minutes."
    curl -fsSL https://ollama.com/install.sh | sh
    systemctl enable --now ollama
    sleep 3
    ollama pull llama3 &
fi

# Download Vosk model if missing
if [ ! -d "/opt/jarvis/vosk-model" ]; then
    mkdir -p /opt/jarvis/vosk-model
    cd /opt/jarvis
    wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip 2>/dev/null
    if [ -f "vosk-model-small-en-us-0.15.zip" ]; then
        unzip -q vosk-model-small-en-us-0.15.zip
        mv vosk-model-small-en-us-0.15/* vosk-model/
        rm -rf vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15.zip
    fi
fi

# Start Jarvis daemon
cd /opt/jarvis
python3 -m jarvis --mode daemon &
STARTUP
chmod +x /usr/local/bin/jarvis-start.sh

# ── Persistence directory ──
mkdir -p /var/lib/jarvis
chown -R jarvis:jarvis /var/lib/jarvis

# ── Install Python dependencies ──
pip install --break-system-packages psutil crewai langchain playwright faster-whisper piper-tts onnxruntime openai python-dotenv 2>/dev/null || true
playwright install --with-deps chromium 2>/dev/null || true

CHROOT_END

ok "System configured"

# ── Unmount ──
info "Finishing up..."
umount -R /mnt

# ── Done ──
echo ""
echo -e "${GREEN}${BOLD}"
echo "  ╔═══════════════════════════════════════╗"
echo "  ║      INSTALLATION COMPLETE! 🎉        ║"
echo "  ╠═══════════════════════════════════════╣"
echo "  ║                                       ║"
echo "  ║  Username: jarvis                     ║"
echo "  ║  Password: jarvis                     ║"
echo "  ║                                       ║"
echo "  ║  Remove USB → Reboot → Jarvis awaits  ║"
echo "  ║                                       ║"
echo "  ║  Keybinds:                            ║"
echo "  ║    Super+Enter  = Terminal            ║"
echo "  ║    Super+D      = App Launcher        ║"
echo "  ║    Super+F      = Firefox             ║"
echo "  ║    Super+Q      = Close Window        ║"
echo "  ║                                       ║"
echo "  ╚═══════════════════════════════════════╝"
echo -e "${NC}"
echo -e "  ${CYAN}Reboot now with: ${BOLD}reboot${NC}"
echo ""
