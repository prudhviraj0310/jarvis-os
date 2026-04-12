#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="jarvis-os"
iso_label="JARVIS_$(date +%Y%m)"
iso_publisher="Prudhviraj <http://prudhviraj-portfolio.onrender.com>"
iso_application="Jarvis OS Live/Rescue CD"
iso_version="$(date +%Y.%m.%d)"
install_dir="arch"
buildmodes=('iso')
bootmodes=('bios.syslinux.mbr' 'bios.syslinux.eltorito'
           'uefi-ia32.grub.esp' 'uefi-x64.grub.esp'
           'uefi-ia32.grub.eltorito' 'uefi-x64.grub.eltorito')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd' '-b' '1M')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/etc/gshadow"]="0:0:400"
  ["/opt/jarvis/"]="0:0:755"
  ["/usr/local/bin/install_to_disk.sh"]="0:0:755"
)
