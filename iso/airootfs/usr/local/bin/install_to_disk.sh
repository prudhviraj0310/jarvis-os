#!/usr/bin/env bash
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "======================================"
echo "    Jarvis OS - Persistent Installer  "
echo "======================================"

lsblk
echo ""
read -p "Enter target disk (e.g. /dev/sda or /dev/nvme0n1): " DISK

if [ -z "$DISK" ] || [ ! -b "$DISK" ]; then
    echo "Invalid disk."
    exit 1
fi

echo "WARNING: This will obliterate everything on $DISK."
read -p "Are you absolutely sure? (Type YES to continue): " CONFIRM
if [ "$CONFIRM" != "YES" ]; then
    echo "Aborted."
    exit 1
fi

echo "[*] Partitioning disk..."
parted -s "$DISK" mklabel gpt
parted -s "$DISK" mkpart ESP fat32 1MiB 513MiB
parted -s "$DISK" set 1 boot on
parted -s "$DISK" mkpart Root ext4 513MiB 100%

if [[ $DISK == *"nvme"* ]]; then
    PART_BOOT="${DISK}p1"
    PART_ROOT="${DISK}p2"
else
    PART_BOOT="${DISK}1"
    PART_ROOT="${DISK}2"
fi

echo "[*] Formatting..."
mkfs.fat -F32 "$PART_BOOT"
mkfs.ext4 -F "$PART_ROOT"

echo "[*] Mounting..."
mount "$PART_ROOT" /mnt
mkdir -p /mnt/boot
mount "$PART_BOOT" /mnt/boot

echo "[*] Installing base system..."
pacman -Sy
pacman -b /mnt -r /mnt --noconfirm -S linux linux-firmware base grub efibootmgr networkmanager hyprland kitty firefox thunar pipewire wireplumber espeak-ng libnotify python python-pip waybar wofi mako vim sudo

# Copy Jarvis Runtime
echo "[*] Migrating Jarvis Intelligence Core..."
mkdir -p /mnt/opt/jarvis
cp -r /opt/jarvis/* /mnt/opt/jarvis/

# System configuration
arch-chroot /mnt /bin/bash <<EOF
# Set timezone
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
hwclock --systohc

# Locale
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Hostname
echo "jarvis" > /etc/hostname

# Setup GRUB
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# Enable services
systemctl enable NetworkManager

# Copy Jarvis systemd services
cp /etc/systemd/system/jarvis.service /etc/systemd/system/
cp /etc/systemd/system/jarvis-firstboot.service /etc/systemd/system/
systemctl enable jarvis.service
systemctl enable jarvis-firstboot.service

# Setup autologin
mkdir -p /etc/systemd/system/getty@tty1.service.d
cp /etc/systemd/system/getty@tty1.service.d/autologin.conf /etc/systemd/system/getty@tty1.service.d/

# Setup skel for Hyprland autostart
mkdir -p /etc/skel/.config
cp -r /etc/skel/.config/hypr /etc/skel/.config/
cp -r /etc/skel/.config/waybar /etc/skel/.config/
cp /etc/skel/.bash_profile /etc/skel/

# Create main user
useradd -m -g users -G wheel,audio,video,input -s /bin/bash jarvis_user
# Passwordless sudo
echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel

# Copy firstboot script
cp /usr/local/bin/jarvis_firstboot.sh /usr/local/bin/
chmod +x /usr/local/bin/jarvis_firstboot.sh
EOF

echo "[+] Installation complete! You may now reboot."
umount -R /mnt
