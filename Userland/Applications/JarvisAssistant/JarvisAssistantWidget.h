/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "ArcReactorWidget.h"
#include <LibGUI/Widget.h>
#include <LibGUI/Button.h>
#include <LibGUI/TextBox.h>
#include <LibGUI/TextEditor.h>
#include <LibGUI/Label.h>
#include <LibJarvis/ConnectionToServer.h>

namespace JarvisAssistant {

class JarvisAssistantWidget final : public GUI::Widget {
    C_OBJECT(JarvisAssistantWidget)
public:
    virtual ~JarvisAssistantWidget() override = default;
    static ErrorOr<NonnullRefPtr<JarvisAssistantWidget>> try_create();

    ErrorOr<void> initialize();

    void execute_command_string(StringView command);
    void trigger_voice_interaction();
    void render_morning_briefing();

private:
    JarvisAssistantWidget() = default;

    RefPtr<ArcReactorWidget> m_arc_reactor;
    RefPtr<GUI::TextBox> m_capability_input;
    RefPtr<GUI::Button> m_execute_button;
    RefPtr<GUI::Button> m_voice_button;

    RefPtr<GUI::Button> m_btn_briefing;
    RefPtr<GUI::Button> m_btn_whatsapp;
    RefPtr<GUI::Button> m_btn_email;
    RefPtr<GUI::Button> m_btn_score;
    RefPtr<GUI::Button> m_btn_news;
    RefPtr<GUI::Button> m_btn_shield;
    RefPtr<GUI::Button> m_btn_lockdown;
    RefPtr<GUI::Button> m_btn_diag;

    RefPtr<GUI::Button> m_chip_briefing;
    RefPtr<GUI::Button> m_chip_whatsapp;
    RefPtr<GUI::Button> m_chip_email;
    RefPtr<GUI::Button> m_chip_score;
    RefPtr<GUI::Button> m_chip_news;
    RefPtr<GUI::Button> m_chip_shield;

    RefPtr<GUI::TextEditor> m_output_editor;
    RefPtr<GUI::Label> m_status_label;
    RefPtr<GUI::Label> m_shield_label;

    RefPtr<Jarvis::ConnectionToServer> m_connection;
    bool m_voice_active { false };
};

}
