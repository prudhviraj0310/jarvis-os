#!/usr/bin/env python3
"""
JARVIS OS — Cinematic Boot Sequence
====================================
A fullscreen GTK4 + Cairo animation that plays when the system boots.
Shows an arc reactor powering up, system diagnostics scrolling, and 
transitions into the desktop.

This runs BEFORE Hyprland loads the desktop — it's the first thing users see.

Requires: gtk4, python-gobject, cairo
"""

import gi
import math
import time
import threading
import random

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, GLib

import cairo


class BootSequence:
    """
    Fullscreen cinematic boot animation.
    Phases:
      0. Black screen
      1. Arc reactor glow appears (center)
      2. Concentric rings spin up
      3. System diagnostic text scrolls
      4. "JARVIS OS" title fades in
      5. Dissolve to desktop
    """

    # ── Diagnostic messages (scroll like Iron Man's HUD) ──
    DIAGNOSTICS = [
        "Initializing neural substrate...",
        "Loading cognitive architecture... [32 modules]",
        "Emotion Engine ................... ONLINE",
        "Thought Engine ................... ONLINE",
        "Energy Model ..................... ONLINE",
        "Memory Palace .................... ONLINE",
        "Behavioral Prediction ............ ONLINE",
        "Reflection Engine ................ ONLINE",
        "Code Evolution Guard ............. ARMED",
        "Identity Core .................... LOADED",
        "Voice Stream ..................... READY",
        "Vision Pipeline .................. STANDBY",
        "LLM Backend (Ollama) ............. CONNECTING",
        "Autonomous Engine ................ ACTIVE",
        "Multi-Agent Society .............. 4 AGENTS",
        "Execution Policy ................. ENFORCED",
        "Screen Awareness ................. BINDING",
        "Input Control Layer .............. LOCKED",
        "Browser Proxy .................... AVAILABLE",
        "External World Adapter ........... ENABLED",
        "",
        "All systems nominal.",
        "Welcome back, sir.",
    ]

    def __init__(self, on_complete=None):
        self._phase = 0.0
        self._diagnostics_shown = 0
        self._diag_buffer = []
        self._start_time = 0
        self._on_complete = on_complete
        self._app = None
        self._window = None
        self._completed = False

    def run(self):
        """Blocks the calling thread. Run in a thread for non-blocking."""
        self._app = Gtk.Application(application_id="ai.jarvis.boot")
        self._app.connect("activate", self._on_activate)
        self._app.run(None)

    def _on_activate(self, app):
        self._window = Gtk.ApplicationWindow(application=app)
        self._window.set_title("Jarvis Boot")
        self._window.fullscreened = True
        self._window.set_fullscreen_mode = True

        # Force fullscreen
        self._window.fullscreen()

        # Add CSS for black background
        css = Gtk.CssProvider()
        css.load_from_string("window { background-color: #000000; }")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Drawing area
        draw = Gtk.DrawingArea()
        draw.set_draw_func(self._on_draw)
        self._window.set_child(draw)

        self._window.present()
        self._start_time = time.time()

        # Tick at 60fps
        GLib.timeout_add(16, self._tick, draw)

    def _tick(self, draw):
        elapsed = time.time() - self._start_time
        self._phase = elapsed

        # Total animation: ~8 seconds
        if elapsed > 8.5 and not self._completed:
            self._completed = True
            # Fade out and close
            GLib.timeout_add(500, self._finish)

        draw.queue_draw()
        return not self._completed

    def _finish(self):
        if self._on_complete:
            self._on_complete()
        if self._app:
            self._app.quit()
        return False

    def _on_draw(self, area, cr, width, height):
        phase = self._phase
        cx, cy = width / 2, height / 2

        # Black background
        cr.set_source_rgb(0, 0, 0)
        cr.paint()

        # ── Phase 0-1.5s: Arc reactor glow appears ──
        if phase > 0.3:
            intensity = min(1.0, (phase - 0.3) / 1.5)
            self._draw_arc_reactor(cr, cx, cy, phase, intensity)

        # ── Phase 1.5s+: Diagnostic text scrolls ──
        if phase > 1.5:
            self._draw_diagnostics(cr, width, height, phase)

        # ── Phase 3s+: Title appears ──
        if phase > 3.0:
            title_alpha = min(1.0, (phase - 3.0) / 1.5)
            self._draw_title(cr, cx, cy - 130, title_alpha)

        # ── Phase 7s+: Fade to white ──
        if phase > 7.0:
            fade = min(1.0, (phase - 7.0) / 1.5)
            cr.set_source_rgba(0.04, 0.05, 0.08, fade)
            cr.paint()

    def _draw_arc_reactor(self, cr, cx, cy, phase, intensity):
        """The core arc reactor animation — concentric spinning rings."""
        blue = (0.20, 0.78, 1.00)

        # Outer ambient glow
        glow_r = 120 * intensity
        pat = cairo.RadialGradient(cx, cy, 0, cx, cy, glow_r)
        pat.add_color_stop_rgba(0.0, blue[0], blue[1], blue[2], 0.12 * intensity)
        pat.add_color_stop_rgba(0.6, blue[0], blue[1], blue[2], 0.04 * intensity)
        pat.add_color_stop_rgba(1.0, 0, 0, 0, 0)
        cr.set_source(pat)
        cr.paint()

        # Ring 3 (outer) — 8 segments, slow rotation
        cr.set_line_width(2)
        for i in range(8):
            angle = phase * 0.5 + i * (math.pi / 4)
            alpha = 0.15 + 0.15 * math.sin(phase * 2 + i)
            cr.set_source_rgba(blue[0], blue[1], blue[2], alpha * intensity)
            cr.arc(cx, cy, 80 * intensity, angle, angle + math.pi * 0.15)
            cr.stroke()

        # Ring 2 (middle) — 6 segments, counter-rotating
        cr.set_line_width(2.5)
        for i in range(6):
            angle = -phase * 0.8 + i * (math.pi / 3)
            alpha = 0.3 + 0.2 * math.sin(phase * 3 + i)
            cr.set_source_rgba(blue[0], blue[1], blue[2], alpha * intensity)
            cr.arc(cx, cy, 50 * intensity, angle, angle + math.pi * 0.25)
            cr.stroke()

        # Ring 1 (inner) — 4 segments, fast
        cr.set_line_width(3)
        for i in range(4):
            angle = phase * 1.5 + i * (math.pi / 2)
            cr.set_source_rgba(blue[0], blue[1], blue[2], 0.6 * intensity)
            cr.arc(cx, cy, 25 * intensity, angle, angle + math.pi * 0.3)
            cr.stroke()

        # Core bright spot
        core_pulse = 0.7 + 0.3 * math.sin(phase * 5)
        cr.set_source_rgba(blue[0], blue[1], blue[2], 0.3 * core_pulse * intensity)
        cr.arc(cx, cy, 15 * intensity, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.9 * core_pulse * intensity)
        cr.arc(cx, cy, 4 * intensity, 0, 2 * math.pi)
        cr.fill()

    def _draw_diagnostics(self, cr, w, h, phase):
        """Scrolling diagnostic text — appears line by line."""
        # How many lines to show
        elapsed_since_start = phase - 1.5
        lines_to_show = int(elapsed_since_start / 0.18)  # New line every 180ms
        lines_to_show = min(lines_to_show, len(self.DIAGNOSTICS))

        cr.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)

        x_start = w * 0.62
        y_start = h * 0.3
        line_height = 17

        for i in range(lines_to_show):
            line = self.DIAGNOSTICS[i]
            y = y_start + i * line_height

            # Fade in each line
            line_age = elapsed_since_start - i * 0.18
            alpha = min(0.85, line_age * 3)

            # Color: ONLINE = green, otherwise blue
            if "ONLINE" in line or "ACTIVE" in line or "READY" in line or "ARMED" in line:
                cr.set_source_rgba(0.18, 0.90, 0.45, alpha)
            elif "nominal" in line or "Welcome" in line:
                cr.set_source_rgba(0.20, 0.78, 1.00, alpha)
            elif "ENFORCED" in line or "LOCKED" in line:
                cr.set_source_rgba(1.0, 0.75, 0.2, alpha)
            else:
                cr.set_source_rgba(0.6, 0.65, 0.7, alpha)

            cr.move_to(x_start, y)
            cr.show_text(line)

    def _draw_title(self, cr, cx, y, alpha):
        """JARVIS OS title with glow."""
        blue = (0.20, 0.78, 1.00)

        # Glow behind text
        cr.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(36)
        text = "JARVIS OS"
        extents = cr.text_extents(text)
        tx = cx - extents.width / 2

        cr.set_source_rgba(blue[0], blue[1], blue[2], 0.15 * alpha)
        cr.move_to(tx - 1, y + 1)
        cr.show_text(text)

        cr.set_source_rgba(blue[0], blue[1], blue[2], alpha)
        cr.move_to(tx, y)
        cr.show_text(text)

        # Subtitle
        cr.set_font_size(12)
        sub = "AI-Native Operating System"
        sub_ext = cr.text_extents(sub)
        cr.set_source_rgba(0.5, 0.55, 0.65, alpha * 0.8)
        cr.move_to(cx - sub_ext.width / 2, y + 30)
        cr.show_text(sub)


# ══════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    def on_boot_done():
        print("[Boot Sequence] Animation complete. Transitioning to desktop.")

    boot = BootSequence(on_complete=on_boot_done)
    boot.run()
