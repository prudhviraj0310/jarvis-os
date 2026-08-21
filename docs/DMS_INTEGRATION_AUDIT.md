# JARVIS OS — Modern Graphical Shell & DMS Integration Audit

**Date**: August 21, 2026  
**Subject**: Architectural Audit for Replacing the Retro UI with DankMaterialShell (Quickshell/QML + Go on Wayland)

---

## 1. Current Graphics Stack
* **Display Server**: Custom SerenityOS `WindowServer` (software rendering, 1990s beveled desktop widgets, no GPU hardware acceleration).
* **Browser Engine**: Experimental in-tree `LibWeb` / `WebContent` (crashes with SIGILL / `has<T>()` assertion failures on modern CSS).
* **Audio**: Intel HDA `/dev/audio/0` (basic PCM, no dynamic mixer / PipeWire stream routing).

---

## 2. Current Boot & Session Flow
```
Multiboot / GRUB → Serenity Kernel (x86_64) → /init → SystemServer → WindowServer → LoginServer → JarvisAssistant
```
* **Limitation**: The entire GUI session is tightly coupled to the retro `WindowServer` protocol (`WindowServer.ipc`).

---

## 3. Current Window Management & IPC
* **Window Management**: Fixed-function floating window manager with 1990s borders and static taskbar.
* **IPC Framework**: Custom `LibIPC` over local AF_LOCAL sockets (`/tmp/portal/window`, `/tmp/portal/jarvis`).

---

## 4. Current JARVIS Services & Intelligence Subsystems (PRESERVED)
* `JarvisService`: Master background daemon.
* `PolicyGate`: Machine sovereignty enforcement (`Allowed` vs `ConfirmRequired`).
* `JournalService`: Cryptographic SHA-256 block ledger (`/var/log/jarvis_journal.log`).
* `PersonalMemory` & `ContextEngine`: Provenance graph (`[OBSERVED]`, `[DERIVED]`, `[INFERRED]`).
* `MIRAEngine`: Multi-channel gateway, model auto-router, and proactive companion.

---

## 5. DMS Compatibility Analysis
* **DankMaterialShell (DMS)** requires:
  1. A standard **Wayland Compositor** supporting `wlr-layer-shell` protocols (specifically **Hyprland** or **niri**).
  2. **Quickshell** (Qt6/QML Wayland shell library).
  3. **Go 1.22+** runtime for the DMS core backend daemon.
  4. Modern DRM/KMS graphics drivers and Mesa EGL/OpenGL/Vulkan.
* **Verdict**: The legacy SerenityOS `WindowServer` **cannot** run Wayland layer shell protocols or Qt6/Quickshell. The graphics and session foundation must be transitioned to **Linux 6.x + Wayland (Hyprland/niri) + systemd**, while preserving the native JARVIS C++ intelligence daemons.

---

## 6. Compositor Evaluation: Hyprland vs niri

| Feature | Hyprland | niri | Winner for JARVIS OS |
| :--- | :--- | :--- | :--- |
| **Compositing Model** | Dynamic Dwindle / Tiling / Floating | Scrollable Tiling | **Hyprland** (More flexible HUD overlays) |
| **Animation & Visuals** | 120 FPS Fluid Bezier, Dual-pass Kawase Blur | Smooth Scroll | **Hyprland** (Apple/Cyberpunk glassmorphism) |
| **DMS Integration** | Fully Supported | Fully Supported | **Tie** |
| **Hardware Compatibility** | VirtIO-GPU, VirGL, Intel/AMD/Nvidia DRM | DRM/KMS | **Hyprland** (Extensive QEMU & bare metal support) |

* **Selected Compositor**: **Hyprland** (with niri as fallback).

---

## 7. Required Architectural Changes
```
                        JARVIS OS
                            │
                            ▼
                      Linux Kernel 6.x
                            │
                            ▼
                         systemd
                            │
                            ▼
                     Wayland Session
                            │
                            ▼
                    Wayland Compositor
                        (Hyprland)
                            │
                            ▼
                    DankMaterialShell
                  (Quickshell/QML + Go)
                            │
            ┌───────────────┼───────────────┐
            │               │               │
         Panels          Launcher        Widgets
            │               │               │
            └───────────────┼───────────────┘
                            │
                     JARVIS UI Bridge
                    (Unix Socket IPC)
                            │
                    JARVIS Intelligence
             (JarvisService / PolicyGate / Journal)
```

---

## 8. Risk Analysis & Mitigation
* **Risk 1: AI Bypassing PolicyGate via GUI**:
  * *Mitigation*: The DMS UI bridge **never** executes native system calls directly. It only sends `RequestCapability` payloads to `PolicyGate`.
* **Risk 2: Heavy Inference Lagging the Graphical Shell**:
  * *Mitigation*: DMS and Quickshell run strictly as UI presentation processes. All AI reasoning and WhatsApp polling run in decoupled background services.

---

## 9. Recommended Implementation Roadmap
1. **Phase 1**: Import upstream `DankMaterialShell` into `third_party/DankMaterialShell/`.
2. **Phase 2**: Build `jarvis-dms/` native integration layer (IPC bridge, widgets, notification handler).
3. **Phase 3**: Configure Hyprland compositor with DMS autostart and Wayland layer-shell rules.
4. **Phase 4**: Assemble bootable OS image (`build/releases/jarvis-os-nextgen-x86_64.iso`).
5. **Phase 5**: Verify in QEMU and generate SHA-256 release checksums.
