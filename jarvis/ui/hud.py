#!/usr/bin/env python3
"""
JARVIS OS — Native HUD Overlay Shell
=====================================
A transparent, always-on-top GTK4 + Cairo overlay that renders the Iron Man HUD
directly on the Wayland compositor via gtk4-layer-shell.

This is NOT a window. It's a compositor layer — it sits above everything,
passes through mouse clicks, and renders only when Jarvis has something to say.

Requires: gtk4, gtk4-layer-shell, python-gobject, cairo
"""

import gi
import math
import time
import threading

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, GLib

# Try to import layer shell for true Wayland overlay
try:
    gi.require_version('Gtk4LayerShell', '1.0')
    from gi.repository import Gtk4LayerShell
    HAS_LAYER_SHELL = True
except (ValueError, ImportError):
    HAS_LAYER_SHELL = False

import cairo


class HUDState:
    """Enumeration of visual states the HUD can be in."""
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    EXECUTING = "executing"
    SUCCESS = "success"
    WARNING = "warning"
    SPEAKING = "speaking"
    BOOT = "boot"


class JarvisHUD:
    """
    The Iron Man HUD — painted in real-time with Cairo on a transparent GTK4 window.
    Uses Wayland layer-shell protocol to float above everything without stealing input.
    """

    # ── Color Palette (Iron Man / Arc Reactor) ──
    COLORS = {
        "arc_blue":      (0.20, 0.78, 1.00),   # Primary arc reactor cyan
        "arc_blue_dim":  (0.10, 0.40, 0.60),   # Dimmed blue
        "arc_glow":      (0.30, 0.85, 1.00),   # Bright glow
        "success_green": (0.18, 0.90, 0.45),
        "warning_amber": (1.00, 0.75, 0.20),
        "danger_red":    (1.00, 0.25, 0.25),
        "text_white":    (0.95, 0.95, 0.97),
        "text_dim":      (0.50, 0.55, 0.65),
        "glass_bg":      (0.04, 0.05, 0.08),   # Near-black glass
    }

    def __init__(self):
        self._state = HUDState.IDLE
        self._status_text = ""
        self._sub_text = ""
        self._progress = 0.0
        self._anim_phase = 0.0
        self._waveform_data = [0.0] * 64
        self._visible = False
        self._hide_timer = None
        self._boot_progress = 0.0

        self._app = None
        self._window = None
        self._draw_area = None
        self._tick_source = None

    # ══════════════════════════════════════════════════════
    # PUBLIC API — Called from Jarvis engine threads
    # ══════════════════════════════════════════════════════

    def show(self, state: str, text: str = "", sub: str = "", duration: float = 4.0):
        """Thread-safe: Show HUD with given state for `duration` seconds."""
        GLib.idle_add(self._show_internal, state, text, sub, duration)

    def update_waveform(self, audio_levels: list):
        """Thread-safe: Feed real-time audio amplitude data (0.0-1.0)."""
        self._waveform_data = audio_levels[:64]

    def set_boot_progress(self, fraction: float):
        """Thread-safe: Update boot sequence progress (0.0-1.0)."""
        self._boot_progress = min(1.0, max(0.0, fraction))

    def hide(self):
        """Thread-safe: Immediately hide the HUD."""
        GLib.idle_add(self._hide_internal)

    # ── Convenience wrappers ──
    def listening(self):
        self.show(HUDState.LISTENING, "Listening...", "Say a command")

    def thinking(self, text=""):
        self.show(HUDState.THINKING, "Processing...", text, duration=10.0)

    def executing(self, text=""):
        self.show(HUDState.EXECUTING, "Executing", text, duration=8.0)

    def success(self, text=""):
        self.show(HUDState.SUCCESS, "Done", text, duration=3.0)

    def warning(self, text=""):
        self.show(HUDState.WARNING, "Warning", text, duration=5.0)

    def speaking(self, text=""):
        self.show(HUDState.SPEAKING, "Speaking...", text, duration=15.0)

    def boot(self):
        self.show(HUDState.BOOT, "JARVIS OS", "Initializing neural pathways...", duration=30.0)

    # ══════════════════════════════════════════════════════
    # GTK APPLICATION LIFECYCLE
    # ══════════════════════════════════════════════════════

    def run(self):
        """Blocks — run in a dedicated thread. Call run_background() instead."""
        self._app = Gtk.Application(application_id="ai.jarvis.hud")
        self._app.connect("activate", self._on_activate)
        self._app.run(None)

    def run_background(self):
        """Launch HUD in a background thread. Non-blocking."""
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        time.sleep(0.5)  # Wait for GTK to initialize
        return t

    def _on_activate(self, app):
        self._window = Gtk.ApplicationWindow(application=app)
        self._window.set_title("Jarvis HUD")
        self._window.set_default_size(500, 200)

        # ── Make transparent ──
        self._window.add_css_class("jarvis-hud-window")

        # ── Layer Shell: become a compositor overlay ──
        if HAS_LAYER_SHELL:
            Gtk4LayerShell.init_for_window(self._window)
            Gtk4LayerShell.set_layer(self._window, Gtk4LayerShell.Layer.OVERLAY)
            Gtk4LayerShell.set_anchor(self._window, Gtk4LayerShell.Edge.TOP, True)
            Gtk4LayerShell.set_anchor(self._window, Gtk4LayerShell.Edge.RIGHT, True)
            Gtk4LayerShell.set_margin(self._window, Gtk4LayerShell.Edge.TOP, 20)
            Gtk4LayerShell.set_margin(self._window, Gtk4LayerShell.Edge.RIGHT, 20)
            Gtk4LayerShell.set_keyboard_mode(self._window, Gtk4LayerShell.KeyboardMode.NONE)
            # Pass through all input — HUD is visual only
            Gtk4LayerShell.set_exclusive_zone(self._window, -1)

        # ── Cairo drawing area ──
        self._draw_area = Gtk.DrawingArea()
        self._draw_area.set_content_width(480)
        self._draw_area.set_content_height(180)
        self._draw_area.set_draw_func(self._on_draw)
        self._window.set_child(self._draw_area)

        # ── Load CSS for transparency ──
        css = Gtk.CssProvider()
        css.load_from_string("""
            .jarvis-hud-window {
                background-color: transparent;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # ── Animation tick (60fps target) ──
        self._tick_source = GLib.timeout_add(16, self._tick)

        # Start hidden
        self._window.set_visible(False)

    # ══════════════════════════════════════════════════════
    # ANIMATION LOOP
    # ══════════════════════════════════════════════════════

    def _tick(self):
        """Called every ~16ms (60fps). Advances animation phase."""
        self._anim_phase += 0.04
        if self._draw_area and self._visible:
            self._draw_area.queue_draw()
        return True  # Keep ticking

    def _show_internal(self, state, text, sub, duration):
        self._state = state
        self._status_text = text
        self._sub_text = sub
        self._visible = True
        if self._window:
            self._window.set_visible(True)

        # Auto-hide timer
        if self._hide_timer:
            GLib.source_remove(self._hide_timer)
        if state != HUDState.BOOT:
            self._hide_timer = GLib.timeout_add(int(duration * 1000), self._hide_internal)

    def _hide_internal(self):
        self._visible = False
        self._state = HUDState.IDLE
        if self._window:
            self._window.set_visible(False)
        self._hide_timer = None
        return False

    # ══════════════════════════════════════════════════════
    # CAIRO RENDERING — The Iron Man HUD
    # ══════════════════════════════════════════════════════

    def _on_draw(self, area, cr, width, height):
        """Master draw function. Dispatches to state-specific renderers."""
        if not self._visible:
            return

        # Clear with full transparency
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        if self._state == HUDState.BOOT:
            self._draw_boot(cr, width, height)
        elif self._state == HUDState.LISTENING:
            self._draw_listening(cr, width, height)
        elif self._state == HUDState.THINKING:
            self._draw_thinking(cr, width, height)
        elif self._state == HUDState.EXECUTING:
            self._draw_executing(cr, width, height)
        elif self._state == HUDState.SUCCESS:
            self._draw_result(cr, width, height, self.COLORS["success_green"], "✓")
        elif self._state == HUDState.WARNING:
            self._draw_result(cr, width, height, self.COLORS["warning_amber"], "⚠")
        elif self._state == HUDState.SPEAKING:
            self._draw_speaking(cr, width, height)

    # ── Glass Panel Background ──
    def _draw_glass_panel(self, cr, x, y, w, h, alpha=0.75):
        """Draws a rounded glassmorphism panel."""
        r = 16  # Corner radius
        cr.new_sub_path()
        cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()

        # Glass fill
        bg = self.COLORS["glass_bg"]
        cr.set_source_rgba(bg[0], bg[1], bg[2], alpha)
        cr.fill_preserve()

        # Border glow
        color = self._state_color()
        cr.set_source_rgba(color[0], color[1], color[2], 0.4)
        cr.set_line_width(1.5)
        cr.stroke()

    def _state_color(self):
        """Returns the primary color for the current state."""
        return {
            HUDState.LISTENING:  self.COLORS["arc_blue"],
            HUDState.THINKING:   self.COLORS["arc_blue"],
            HUDState.EXECUTING:  self.COLORS["arc_glow"],
            HUDState.SUCCESS:    self.COLORS["success_green"],
            HUDState.WARNING:    self.COLORS["warning_amber"],
            HUDState.SPEAKING:   self.COLORS["arc_blue"],
            HUDState.BOOT:       self.COLORS["arc_blue"],
        }.get(self._state, self.COLORS["arc_blue"])

    # ── LISTENING: Pulsing arc reactor ring ──
    def _draw_listening(self, cr, w, h):
        self._draw_glass_panel(cr, 0, 0, w, h)

        # Pulsing circle
        cx, cy = 40, h / 2
        pulse = 0.5 + 0.5 * math.sin(self._anim_phase * 3)
        radius = 12 + pulse * 4

        color = self.COLORS["arc_blue"]
        # Outer glow
        cr.set_source_rgba(color[0], color[1], color[2], 0.15 + pulse * 0.15)
        cr.arc(cx, cy, radius + 8, 0, 2 * math.pi)
        cr.fill()
        # Core
        cr.set_source_rgba(color[0], color[1], color[2], 0.6 + pulse * 0.4)
        cr.arc(cx, cy, radius, 0, 2 * math.pi)
        cr.fill()
        # Center bright spot
        cr.set_source_rgba(1, 1, 1, 0.8)
        cr.arc(cx, cy, 3, 0, 2 * math.pi)
        cr.fill()

        # Text
        self._draw_text(cr, 70, h / 2 - 12, self._status_text, 15, self.COLORS["text_white"])
        self._draw_text(cr, 70, h / 2 + 10, self._sub_text, 11, self.COLORS["text_dim"])

    # ── THINKING: Spinning arc segments ──
    def _draw_thinking(self, cr, w, h):
        self._draw_glass_panel(cr, 0, 0, w, h)

        cx, cy = 40, h / 2
        color = self.COLORS["arc_blue"]

        # Spinning arc segments
        for i in range(3):
            angle_offset = self._anim_phase * 2 + i * (2 * math.pi / 3)
            cr.set_source_rgba(color[0], color[1], color[2], 0.3 + i * 0.2)
            cr.set_line_width(2.5 - i * 0.5)
            cr.arc(cx, cy, 14 + i * 4, angle_offset, angle_offset + math.pi * 0.6)
            cr.stroke()

        # Center dot
        cr.set_source_rgba(color[0], color[1], color[2], 0.9)
        cr.arc(cx, cy, 3, 0, 2 * math.pi)
        cr.fill()

        # Text
        dots = "." * (int(self._anim_phase * 2) % 4)
        self._draw_text(cr, 70, h / 2 - 12, f"Thinking{dots}", 15, self.COLORS["text_white"])
        self._draw_text(cr, 70, h / 2 + 10, self._sub_text, 11, self.COLORS["text_dim"])

    # ── EXECUTING: Progress bar with energy flow ──
    def _draw_executing(self, cr, w, h):
        self._draw_glass_panel(cr, 0, 0, w, h)

        color = self.COLORS["arc_glow"]

        # Animated progress bar
        bar_x = 20
        bar_y = h - 35
        bar_w = w - 40
        bar_h = 4

        # Track
        cr.set_source_rgba(0.2, 0.2, 0.3, 0.5)
        self._rounded_rect(cr, bar_x, bar_y, bar_w, bar_h, 2)
        cr.fill()

        # Energy flow (sweeping highlight)
        flow_pos = (self._anim_phase * 0.3) % 1.0
        flow_w = bar_w * 0.3
        flow_x = bar_x + flow_pos * (bar_w - flow_w)

        pat = cairo.LinearGradient(flow_x, 0, flow_x + flow_w, 0)
        pat.add_color_stop_rgba(0.0, color[0], color[1], color[2], 0.0)
        pat.add_color_stop_rgba(0.5, color[0], color[1], color[2], 0.8)
        pat.add_color_stop_rgba(1.0, color[0], color[1], color[2], 0.0)
        cr.set_source(pat)
        self._rounded_rect(cr, bar_x, bar_y, bar_w, bar_h, 2)
        cr.fill()

        # Icon: lightning bolt
        self._draw_text(cr, 20, h / 2 - 18, "⚡", 20, color)

        # Text
        self._draw_text(cr, 55, h / 2 - 15, self._status_text, 15, self.COLORS["text_white"])
        self._draw_text(cr, 55, h / 2 + 8, self._sub_text, 11, self.COLORS["text_dim"])

    # ── SUCCESS / WARNING: Checkmark or warning icon ──
    def _draw_result(self, cr, w, h, color, icon):
        self._draw_glass_panel(cr, 0, 0, w, h)

        # Expanding ring animation
        expand = min(1.0, self._anim_phase * 0.5)
        cx, cy = 40, h / 2

        cr.set_source_rgba(color[0], color[1], color[2], 0.3 * (1 - expand))
        cr.arc(cx, cy, 10 + expand * 20, 0, 2 * math.pi)
        cr.fill()

        cr.set_source_rgba(color[0], color[1], color[2], 0.9)
        cr.arc(cx, cy, 10, 0, 2 * math.pi)
        cr.fill()

        self._draw_text(cr, 70, h / 2 - 12, self._status_text, 15, color)
        self._draw_text(cr, 70, h / 2 + 10, self._sub_text, 11, self.COLORS["text_dim"])

    # ── SPEAKING: Real-time waveform visualization ──
    def _draw_speaking(self, cr, w, h):
        self._draw_glass_panel(cr, 0, 0, w, h)

        color = self.COLORS["arc_blue"]
        bar_count = min(len(self._waveform_data), 48)
        bar_width = 4
        gap = 3
        total_w = bar_count * (bar_width + gap)
        start_x = (w - total_w) / 2
        center_y = h / 2 + 10

        for i in range(bar_count):
            # Simulated waveform if no real data
            if all(v == 0 for v in self._waveform_data):
                amp = 0.2 + 0.6 * abs(math.sin(self._anim_phase * 3 + i * 0.3))
            else:
                amp = max(0.05, self._waveform_data[i])

            bar_h = amp * 40
            x = start_x + i * (bar_width + gap)

            # Gradient per bar
            alpha = 0.4 + amp * 0.6
            cr.set_source_rgba(color[0], color[1], color[2], alpha)
            self._rounded_rect(cr, x, center_y - bar_h / 2, bar_width, bar_h, 1.5)
            cr.fill()

        # Text above waveform
        self._draw_text(cr, w / 2, 18, self._status_text, 13, self.COLORS["text_white"], center=True)

    # ── BOOT: Arc reactor power-up sequence ──
    def _draw_boot(self, cr, w, h):
        # Full panel
        self._draw_glass_panel(cr, 0, 0, w, h, alpha=0.85)

        cx, cy = w / 2, h / 2 - 10
        color = self.COLORS["arc_blue"]
        phase = self._anim_phase

        # Outer rotating ring
        cr.set_line_width(2)
        for i in range(6):
            angle = phase * 1.5 + i * (math.pi / 3)
            seg_len = math.pi * 0.35
            alpha = 0.2 + 0.3 * math.sin(phase + i)
            cr.set_source_rgba(color[0], color[1], color[2], alpha)
            cr.arc(cx, cy, 45, angle, angle + seg_len)
            cr.stroke()

        # Middle ring (counter-rotating)
        for i in range(4):
            angle = -phase * 2 + i * (math.pi / 2)
            cr.set_source_rgba(color[0], color[1], color[2], 0.5)
            cr.arc(cx, cy, 30, angle, angle + math.pi * 0.3)
            cr.stroke()

        # Inner core glow
        core_pulse = 0.5 + 0.5 * math.sin(phase * 4)
        cr.set_source_rgba(color[0], color[1], color[2], 0.2 + core_pulse * 0.3)
        cr.arc(cx, cy, 18, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.6 + core_pulse * 0.4)
        cr.arc(cx, cy, 5, 0, 2 * math.pi)
        cr.fill()

        # Boot text
        self._draw_text(cr, cx, h - 35, self._status_text, 16, self.COLORS["text_white"], center=True, bold=True)
        self._draw_text(cr, cx, h - 15, self._sub_text, 10, self.COLORS["text_dim"], center=True)

        # Progress bar at very bottom
        bar_x = 30
        bar_y = h - 8
        bar_w = w - 60
        cr.set_source_rgba(0.15, 0.15, 0.2, 0.5)
        self._rounded_rect(cr, bar_x, bar_y, bar_w, 3, 1.5)
        cr.fill()
        if self._boot_progress > 0:
            cr.set_source_rgba(color[0], color[1], color[2], 0.9)
            self._rounded_rect(cr, bar_x, bar_y, bar_w * self._boot_progress, 3, 1.5)
            cr.fill()

    # ══════════════════════════════════════════════════════
    # CAIRO HELPERS
    # ══════════════════════════════════════════════════════

    def _draw_text(self, cr, x, y, text, size, color, center=False, bold=False):
        if not text:
            return
        cr.select_font_face("monospace",
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(size)

        if center:
            extents = cr.text_extents(text)
            x = x - extents.width / 2

        cr.set_source_rgba(color[0], color[1], color[2], 1.0)
        cr.move_to(x, y + size * 0.35)
        cr.show_text(text)

    def _rounded_rect(self, cr, x, y, w, h, r):
        cr.new_sub_path()
        cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()


# ══════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    import time

    hud = JarvisHUD()
    t = hud.run_background()

    time.sleep(1)
    hud.boot()
    for i in range(20):
        hud.set_boot_progress(i / 20.0)
        time.sleep(0.15)

    hud.hide()
    time.sleep(0.5)

    hud.listening()
    time.sleep(3)

    hud.thinking("Analyzing your request")
    time.sleep(3)

    hud.executing("Running: firefox https://youtube.com")
    time.sleep(3)

    hud.success("YouTube opened successfully")
    time.sleep(3)

    hud.speaking("Playing lofi hip hop beats")
    time.sleep(5)

    hud.warning("Battery below 20%")
    time.sleep(3)

    hud.hide()
    print("[HUD Test] Complete.")
