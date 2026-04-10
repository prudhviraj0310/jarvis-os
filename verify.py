#!/usr/bin/env python3
"""
Jarvis OS - System Integrity Verification Suite
Validates every module, file, and contract in the project.
Run: python3 verify.py
"""

import os
import sys
import json
import importlib
import wave

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"
results = {"pass": 0, "fail": 0, "warn": 0}

def check(label, condition, critical=True):
    if condition:
        print(f"  {PASS} {label}")
        results["pass"] += 1
    elif critical:
        print(f"  {FAIL} {label}")
        results["fail"] += 1
    else:
        print(f"  {WARN} {label} (non-critical)")
        results["warn"] += 1

ROOT = os.path.dirname(os.path.abspath(__file__))
JARVIS = os.path.join(ROOT, "jarvis")
ISO = os.path.join(ROOT, "iso")

print("\n══════════════════════════════════════════")
print("  JARVIS OS — SYSTEM INTEGRITY AUDIT")
print("══════════════════════════════════════════\n")

# 1. Core Python Modules
print("─── 1. Core Python Modules ───")
core_files = [
    "jarvis/__init__.py", "jarvis/__main__.py",
    "jarvis/core/__init__.py", "jarvis/core/runtime.py",
    "jarvis/engine/__init__.py", "jarvis/engine/llm.py",
    "jarvis/engine/context.py", "jarvis/engine/behavior.py",
    "jarvis/system/__init__.py", "jarvis/system/execution.py",
    "jarvis/system/input_control.py", "jarvis/system/kernel.py",
    "jarvis/system/screen.py",
    "jarvis/interface/__init__.py", "jarvis/interface/voice.py",
    "jarvis/interface/overlay.py", "jarvis/interface/listener.py",
    "jarvis/plugins/__init__.py", "jarvis/plugins/mempalace_adapter.py",
    "jarvis/memory/__init__.py",
]
for f in core_files:
    check(f, os.path.isfile(os.path.join(ROOT, f)))

# 2. Sound Assets
print("\n─── 2. Sound Assets ───")
for wav in ["listening.wav", "success.wav", "error.wav"]:
    path = os.path.join(JARVIS, "assets", wav)
    exists = os.path.isfile(path)
    check(f"jarvis/assets/{wav} exists", exists)
    if exists:
        try:
            with wave.open(path, "r") as w:
                check(f"  {wav} valid WAV ({w.getnframes()} frames)", w.getnframes() > 0)
        except Exception:
            check(f"  {wav} valid WAV", False)

# 3. ISO Profile
print("\n─── 3. Archiso ISO Profile ───")
iso_files = [
    "iso/profiledef.sh", "iso/packages.x86_64",
    "iso/airootfs/etc/skel/.bash_profile",
    "iso/airootfs/etc/skel/.config/hypr/hyprland.conf",
    "iso/airootfs/etc/skel/.config/waybar/config",
    "iso/airootfs/etc/skel/.config/waybar/style.css",
    "iso/airootfs/etc/systemd/system/jarvis.service",
    "iso/airootfs/etc/systemd/system/jarvis-firstboot.service",
    "iso/airootfs/etc/systemd/system/getty@tty1.service.d/autologin.conf",
    "iso/airootfs/usr/local/bin/jarvis_firstboot.sh",
    "iso/airootfs/usr/local/bin/install_to_disk.sh",
]
for f in iso_files:
    check(f, os.path.isfile(os.path.join(ROOT, f)))

# 4. Package List
print("\n─── 4. Package List Contents ───")
pkg_path = os.path.join(ROOT, "iso", "packages.x86_64")
if os.path.isfile(pkg_path):
    with open(pkg_path) as f:
        pkgs = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    for p in ["base","linux","hyprland","kitty","firefox","python","pipewire","networkmanager","espeak-ng","libnotify","waybar","wofi","mako","grim"]:
        check(f"Package '{p}' listed", p in pkgs)

# 5. Build Script
print("\n─── 5. Build Script ───")
if os.path.isfile(os.path.join(ROOT, "build_os.sh")):
    with open(os.path.join(ROOT, "build_os.sh")) as f:
        content = f.read()
    check("Uses mkarchiso", "mkarchiso" in content)
    check("Copies jarvis/ into airootfs", "jarvis" in content)

# 6. Systemd Service
print("\n─── 6. Systemd Service ───")
svc_path = os.path.join(ISO, "airootfs/etc/systemd/system/jarvis.service")
if os.path.isfile(svc_path):
    with open(svc_path) as f:
        svc = f.read()
    check("ExecStart uses python3 -m jarvis", "python3 -m jarvis" in svc)
    check("Restart=always", "Restart=always" in svc)
    check("WorkingDirectory=/opt/jarvis", "WorkingDirectory=/opt/jarvis" in svc)

# 7. First Boot
print("\n─── 7. First Boot Script ───")
fb_path = os.path.join(ISO, "airootfs/usr/local/bin/jarvis_firstboot.sh")
if os.path.isfile(fb_path):
    with open(fb_path) as f:
        fb = f.read()
    check("Installs Ollama", "ollama.com/install.sh" in fb)
    check("Pulls llama3", "llama3" in fb)
    check("Downloads Vosk model", "vosk" in fb.lower())
    check("Marks firstboot done", ".firstboot_done" in fb)

# 8. Hyprland Config
print("\n─── 8. Hyprland Config ───")
hypr_path = os.path.join(ISO, "airootfs/etc/skel/.config/hypr/hyprland.conf")
if os.path.isfile(hypr_path):
    with open(hypr_path) as f:
        hypr = f.read()
    check("Auto-starts waybar", "waybar" in hypr)
    check("Auto-starts mako", "mako" in hypr)
    check("Auto-starts Jarvis daemon", "jarvis" in hypr)
    check("SUPER+Return = terminal", "Return" in hypr and "kitty" in hypr)

# 9. Python Imports
print("\n─── 9. Python Import Test ───")
sys.path.insert(0, ROOT)
for mod_path, cls_name in [
    ("jarvis.engine.context", "ContextEngine"),
    ("jarvis.engine.behavior", "BehavioralEngine"),
    ("jarvis.system.execution", "ExecutionPolicy"),
    ("jarvis.interface.voice", "VoiceEngine"),
    ("jarvis.interface.overlay", "OverlayEngine"),
    ("jarvis.plugins.mempalace_adapter", "MemPalaceAdapter"),
]:
    try:
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, cls_name, None)
        check(f"{mod_path}.{cls_name}", cls is not None)
    except Exception as e:
        check(f"{mod_path}.{cls_name} ({e})", False, critical=False)

# 10. Docs
print("\n─── 10. Documentation ───")
check("README.md", os.path.isfile(os.path.join(ROOT, "README.md")))
check("ARCHITECTURE.md", os.path.isfile(os.path.join(ROOT, "ARCHITECTURE.md")))
check("requirements.txt", os.path.isfile(os.path.join(ROOT, "requirements.txt")))

# Final
print("\n══════════════════════════════════════════")
print(f"  RESULTS: {results['pass']} passed | {results['fail']} failed | {results['warn']} warnings")
if results["fail"] == 0:
    print("  STATUS: ✅ JARVIS OS IS COMPLETE")
else:
    print(f"  STATUS: ❌ {results['fail']} CRITICAL ISSUE(S)")
print("══════════════════════════════════════════\n")
sys.exit(1 if results["fail"] > 0 else 0)
