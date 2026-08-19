/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ArcReactorWidget.h"
#include <LibGUI/Painter.h>
#include <LibGfx/Font/Font.h>
#include <LibGfx/Font/FontDatabase.h>
#include <math.h>

REGISTER_WIDGET(JarvisAssistant, ArcReactorWidget)

namespace JarvisAssistant {

ArcReactorWidget::ArcReactorWidget()
{
    m_anim_timer = Core::Timer::create_repeating(33, [this]() {
        m_rotation_angle += 0.04f;
        if (m_rotation_angle > 6.28318f)
            m_rotation_angle -= 6.28318f;

        m_waveform_phase += 0.12f;
        if (m_waveform_phase > 6.28318f)
            m_waveform_phase -= 6.28318f;

        update();
    });
    m_anim_timer->start();
}

void ArcReactorWidget::set_active_voice_mode(bool active)
{
    m_voice_mode_active = active;
    if (active) {
        m_primary_color = Color(0, 255, 220);
    } else {
        m_primary_color = Color(0, 229, 255);
    }
    update();
}

void ArcReactorWidget::set_threat_status(StringView status)
{
    m_status_text = status;
    if (status.contains("LOCKDOWN"sv)) {
        m_primary_color = Color(255, 45, 85);
    } else if (status.contains("ELEVATED"sv)) {
        m_primary_color = Color(255, 183, 3);
    } else {
        m_primary_color = Color(0, 229, 255);
    }
    update();
}

void ArcReactorWidget::mousedown_event(GUI::MouseEvent&)
{
    m_voice_mode_active = !m_voice_mode_active;
    update();
}

static void draw_polygon_ring(GUI::Painter& painter, Gfx::IntPoint center, int radius, Color color, int segments)
{
    float step = 6.28318f / segments;
    for (int i = 0; i < segments; ++i) {
        float a1 = i * step;
        float a2 = (i + 1) * step;

        Gfx::IntPoint p1(center.x() + static_cast<int>(radius * cosf(a1)), center.y() + static_cast<int>(radius * sinf(a1)));
        Gfx::IntPoint p2(center.x() + static_cast<int>(radius * cosf(a2)), center.y() + static_cast<int>(radius * sinf(a2)));

        painter.draw_line(p1, p2, color, 2);
    }
}

void ArcReactorWidget::paint_event(GUI::PaintEvent&)
{
    GUI::Painter painter(*this);
    auto rect = this->rect();

    // 1. Deep Obsidian Slate Background
    painter.fill_rect(rect, Color(5, 8, 15));

    // 2. Tactical Corner HUD Brackets
    int bracket_len = 18;
    Color bracket_col = m_primary_color;
    // Top-Left
    painter.draw_line(rect.top_left(), rect.top_left().translated(bracket_len, 0), bracket_col, 2);
    painter.draw_line(rect.top_left(), rect.top_left().translated(0, bracket_len), bracket_col, 2);
    // Top-Right
    painter.draw_line(rect.top_right().translated(-1, 0), rect.top_right().translated(-bracket_len, 0), bracket_col, 2);
    painter.draw_line(rect.top_right().translated(-1, 0), rect.top_right().translated(-1, bracket_len), bracket_col, 2);
    // Bottom-Left
    painter.draw_line(rect.bottom_left().translated(0, -1), rect.bottom_left().translated(bracket_len, -1), bracket_col, 2);
    painter.draw_line(rect.bottom_left().translated(0, -1), rect.bottom_left().translated(0, -bracket_len), bracket_col, 2);
    // Bottom-Right
    painter.draw_line(rect.bottom_right().translated(-1, -1), rect.bottom_right().translated(-bracket_len, -1), bracket_col, 2);
    painter.draw_line(rect.bottom_right().translated(-1, -1), rect.bottom_right().translated(-1, -bracket_len), bracket_col, 2);

    auto center = rect.center();
    int min_dim = min(rect.width(), rect.height());
    int max_radius = (min_dim / 2) - 16;
    if (max_radius < 25)
        return;

    // 3. Multi-layer Concentric Outer Rings (Polygon Ring Math - No Scale Assertion)
    draw_polygon_ring(painter, center, max_radius, m_primary_color, 48);

    int mid_radius = max_radius * 4 / 5;
    draw_polygon_ring(painter, center, mid_radius, Color(0, 140, 190), 36);

    int inner_radius = max_radius / 2;
    draw_polygon_ring(painter, center, inner_radius, m_primary_color, 24);

    // 4. Counter-rotating Energy Spokes
    int num_spokes = 16;
    for (int i = 0; i < num_spokes; ++i) {
        float angle = m_rotation_angle + (i * 6.28318f / num_spokes);
        float cos_a = cosf(angle);
        float sin_a = sinf(angle);

        Gfx::IntPoint p1(center.x() + static_cast<int>((inner_radius + 4) * cos_a), center.y() + static_cast<int>((inner_radius + 4) * sin_a));
        Gfx::IntPoint p2(center.x() + static_cast<int>((mid_radius - 4) * cos_a), center.y() + static_cast<int>((mid_radius - 4) * sin_a));

        Color spoke_col = (i % 2 == 0) ? m_primary_color : Color(0, 160, 210);
        painter.draw_line(p1, p2, spoke_col, 2);
    }

    // 5. Dynamic Audio / Voice Frequency Waveform across Center
    int wave_width = max_radius * 2 - 24;
    int start_x = center.x() - (wave_width / 2);
    int wave_amp = m_voice_mode_active ? 18 : 6;

    for (int x = 0; x < wave_width - 2; x += 2) {
        float norm_x = static_cast<float>(x) / wave_width;
        float window = sinf(norm_x * 3.14159f);
        float wave_val = sinf((norm_x * 12.0f) + m_waveform_phase) * wave_amp * window;

        Gfx::IntPoint wp1(start_x + x, center.y() + static_cast<int>(wave_val));
        Gfx::IntPoint wp2(start_x + x + 2, center.y() + static_cast<int>(wave_val));

        Color wave_col = m_voice_mode_active ? Color(0, 255, 230) : Color(0, 200, 240);
        painter.draw_line(wp1, wp2, wave_col, 2);
    }

    // 6. Glowing Center Core Matrix
    auto& font = Gfx::FontDatabase::default_font();
    Gfx::IntRect text_rect(center.x() - inner_radius, center.y() - 10, inner_radius * 2, 20);
    painter.draw_text(text_rect, m_status_text, font, Gfx::TextAlignment::Center, m_primary_color);
}

}
