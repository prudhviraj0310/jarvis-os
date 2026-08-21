# Capability Blueprint: Desktop & Browser Intelligence

- **Inspired by**: `yashvar23/jarvis` (Desktop Sidecar), `dev-core-busy/jarvis` (Desktop Control), `Friday` (Screen OCR)

---

## 1. Wayland Desktop Awareness
On a modern Linux/Wayland system (Hyprland), the desktop intelligence sidecar inspects:
* Active window class and title via `hyprctl activewindow -j`.
* Current workspace layout and running processes.
* Visible on-screen context via screenshot buffer & local OCR (`tesseract` / Vision API).

---

## 2. Real Web Browser Automation
* Utilizes standard Chromium DevTools Protocol (CDP) or Playwright over Unix domain sockets to inspect active web pages, fill forms, or extract relevant research text without crashing the window manager.
