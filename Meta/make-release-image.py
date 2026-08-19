#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import hashlib

SOURCE_DIR = "/Users/prudhviraj/jarvis-os"
BUILD_DIR = os.path.join(SOURCE_DIR, "Build/x86_64")
RELEASE_DIR = os.path.join(SOURCE_DIR, "build/releases")
TMP_DIR = os.path.join(BUILD_DIR, "release_tmp")

os.makedirs(RELEASE_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

IMG_OUTPUT = os.path.join(RELEASE_DIR, "jarvis-os-x86_64.img")
ISO_OUTPUT = os.path.join(RELEASE_DIR, "jarvis-os-x86_64.iso")
ESP_IMG = os.path.join(TMP_DIR, "esp.img")
ROOT_EXT2 = os.path.join(BUILD_DIR, "_disk_image")
KERNEL_EFI = os.path.join(BUILD_DIR, "Kernel/EFIPrekernel/Kernel.efi")

print("[1/5] Verifying required source artifacts...")
if not os.path.isfile(KERNEL_EFI):
    sys.exit(f"Error: Kernel.efi not found at {KERNEL_EFI}")
if not os.path.isfile(ROOT_EXT2):
    sys.exit(f"Error: Root disk image not found at {ROOT_EXT2}")

print(f"  - Kernel.efi: {KERNEL_EFI} ({os.path.getsize(KERNEL_EFI)} bytes)")
print(f"  - Root ext2: {ROOT_EXT2} ({os.path.getsize(ROOT_EXT2)} bytes)")

# 2. Build 64MB FAT32 ESP Image
print("[2/5] Building EFI System Partition (ESP) image...")
ESP_SIZE_MB = 64
if os.path.exists(ESP_IMG):
    os.remove(ESP_IMG)

with open(ESP_IMG, "wb") as f:
    f.truncate(ESP_SIZE_MB * 1024 * 1024)

# Format with mkfs.vfat
subprocess.run(["mkfs.vfat", "-F", "32", "-n", "JARVIS_ESP", ESP_IMG], check=True)

# Create directory structure inside ESP using mcopy/mmd
os.environ["MTOOLSRC"] = "/dev/null"
subprocess.run(["mmd", "-i", ESP_IMG, "::EFI"], check=True)
subprocess.run(["mmd", "-i", ESP_IMG, "::EFI/BOOT"], check=True)
subprocess.run(["mcopy", "-i", ESP_IMG, KERNEL_EFI, "::EFI/BOOT/BOOTX64.EFI"], check=True)
subprocess.run(["mcopy", "-i", ESP_IMG, KERNEL_EFI, "::Kernel.efi"], check=True)

# 3. Create GPT Physical Disk Image (.img)
print("[3/5] Assembling GPT Physical Disk Image (jarvis-os-x86_64.img)...")
SECTOR_SIZE = 512
# ESP: 64MB -> 131072 sectors. Start at sector 2048 (1MB offset)
ESP_START_SECTOR = 2048
ESP_SECTORS = (ESP_SIZE_MB * 1024 * 1024) // SECTOR_SIZE
ESP_END_SECTOR = ESP_START_SECTOR + ESP_SECTORS - 1

# Root ext2: Size in sectors
root_size_bytes = os.path.getsize(ROOT_EXT2)
root_sectors = (root_size_bytes + SECTOR_SIZE - 1) // SECTOR_SIZE
# Align start to 2048 boundary (1MB)
ROOT_START_SECTOR = ((ESP_END_SECTOR + 2048) // 2048) * 2048
ROOT_END_SECTOR = ROOT_START_SECTOR + root_sectors - 1

TOTAL_SECTORS = ROOT_END_SECTOR + 2048 # + 1MB buffer for backup GPT

print(f"  - Partition 1 (ESP): Sectors {ESP_START_SECTOR} to {ESP_END_SECTOR}")
print(f"  - Partition 2 (ROOT): Sectors {ROOT_START_SECTOR} to {ROOT_END_SECTOR}")
print(f"  - Total Image Size: {TOTAL_SECTORS * SECTOR_SIZE / (1024*1024):.2f} MB")

if os.path.exists(IMG_OUTPUT):
    os.remove(IMG_OUTPUT)

with open(IMG_OUTPUT, "wb") as out_f:
    out_f.truncate(TOTAL_SECTORS * SECTOR_SIZE)
    # Write ESP partition data
    out_f.seek(ESP_START_SECTOR * SECTOR_SIZE)
    with open(ESP_IMG, "rb") as esp_f:
        shutil.copyfileobj(esp_f, out_f)
    # Write Root partition data
    out_f.seek(ROOT_START_SECTOR * SECTOR_SIZE)
    with open(ROOT_EXT2, "rb") as root_f:
        shutil.copyfileobj(root_f, out_f)

# Write GPT partition table using sgdisk
subprocess.run(["sgdisk", "-Z", IMG_OUTPUT], check=True) # Zap any existing table
subprocess.run([
    "sgdisk",
    "-n", f"1:{ESP_START_SECTOR}:{ESP_END_SECTOR}",
    "-t", "1:ef00",
    "-c", "1:JARVIS-ESP",
    "-n", f"2:{ROOT_START_SECTOR}:{ROOT_END_SECTOR}",
    "-t", "2:8300",
    "-c", "2:JARVIS-ROOT",
    IMG_OUTPUT
], check=True)

print(f"  -> Successfully generated {IMG_OUTPUT}")

# 4. Generate Bootable UEFI Hybrid ISO (.iso)
print("[4/5] Generating Bootable Hybrid ISO (jarvis-os-x86_64.iso)...")
ISO_ROOT = os.path.join(TMP_DIR, "iso_root")
if os.path.exists(ISO_ROOT):
    shutil.rmtree(ISO_ROOT)
os.makedirs(os.path.join(ISO_ROOT, "EFI/BOOT"), exist_ok=True)
shutil.copyfile(KERNEL_EFI, os.path.join(ISO_ROOT, "EFI/BOOT/BOOTX64.EFI"))
shutil.copyfile(ESP_IMG, os.path.join(TMP_DIR, "efiboot.img"))

subprocess.run([
    "xorriso", "-as", "mkisofs",
    "-iso-level", "3",
    "-full-iso9660-filenames",
    "-volid", "JARVIS_OS_1_0",
    "-eltorito-alt-boot",
    "-e", "efiboot.img",
    "-no-emul-boot",
    "-isohybrid-gpt-basdat",
    "-output", ISO_OUTPUT,
    TMP_DIR,
    ISO_ROOT
], check=True)

print(f"  -> Successfully generated {ISO_OUTPUT}")

# 5. Compute Checksums
print("[5/5] Calculating SHA-256 Checksums...")
def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

img_hash = sha256_file(IMG_OUTPUT)
iso_hash = sha256_file(ISO_OUTPUT)
kernel_hash = sha256_file(KERNEL_EFI)

sums_path = os.path.join(RELEASE_DIR, "SHA256SUMS")
with open(sums_path, "w") as f:
    f.write(f"{img_hash}  jarvis-os-x86_64.img\n")
    f.write(f"{iso_hash}  jarvis-os-x86_64.iso\n")
    f.write(f"{kernel_hash}  Kernel.efi\n")

print(f"Checksums saved to {sums_path}:")
print(f"  - jarvis-os-x86_64.img: {img_hash}")
print(f"  - jarvis-os-x86_64.iso: {iso_hash}")
print(f"  - Kernel.efi:           {kernel_hash}")
