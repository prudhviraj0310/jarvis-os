/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <LibGUI/Widget.h>
#include <LibCore/Timer.h>
#include <LibGfx/Color.h>

namespace JarvisAssistant {

class ArcReactorWidget final : public GUI::Widget {
    C_OBJECT(ArcReactorWidget)
public:
    virtual ~ArcReactorWidget() override = default;

    void set_active_voice_mode(bool active);
    void set_threat_status(StringView status);

protected:
    virtual void paint_event(GUI::PaintEvent&) override;
    virtual void mousedown_event(GUI::MouseEvent&) override;

private:
    ArcReactorWidget();

    RefPtr<Core::Timer> m_anim_timer;
    float m_rotation_angle { 0.0f };
    float m_waveform_phase { 0.0f };
    bool m_voice_mode_active { false };
    ByteString m_status_text { "ONLINE" };
    Color m_primary_color { 0, 229, 255 }; // Cyan
    Color m_accent_color { 255, 183, 3 };  // Gold/Amber
};

}
