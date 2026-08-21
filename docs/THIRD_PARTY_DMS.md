# Third-Party Attribution & Integration Record: DankMaterialShell (DMS)

- **Upstream Repository**: `https://github.com/AvengeMedia/DankMaterialShell.git`
- **Upstream Commit SHA**: `2f4afeb8892c6c2b5a3519771e465af499762a2f`
- **License**: MIT License (Copyright (c) 2026 AvengeMedia)
- **Submodules Imported**:
  - `dank-qml-common` (`https://github.com/AvengeMedia/dank-qml-common.git` @ `fbbdddc47b5564dcf67aa05bd7bf1d3af8f5aad5`)
- **Import Location**: `third_party/DankMaterialShell/`

---

## 🧩 Architectural Role of DMS in JARVIS OS
DMS is the primary **Wayland Graphical Desktop Shell**. It replaces all retro/ad-hoc desktop panels, window titlebars, launchers, system controls, and lock screens with:
1. **Quickshell / QML Material 3 Shell Engine**: Declarative, high-performance GPU-composited UI widgets.
2. **Go Core Daemon (`core/`)**: System monitoring, Matugen dynamic theming, audio/network control, and IPC dispatch.
3. **Compositor Support**: Native integration with Wayland compositors (**Hyprland** and **niri**).

---

## 🔒 JARVIS OS Modifications & Extensions
* Added `jarvis-dms/` native integration bridge connecting DMS panels directly to `JarvisService`, `PolicyGate`, and `JournalService` via Unix domain sockets.
* Enhanced telemetry modules to display academic attendance (`87.5%`), WhatsApp unread counters, and executive briefing state.
