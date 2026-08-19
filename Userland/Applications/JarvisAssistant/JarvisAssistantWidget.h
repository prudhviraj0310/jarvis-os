/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <LibGUI/Widget.h>
#include <LibGUI/TextBox.h>
#include <LibGUI/Button.h>
#include <LibGUI/TextEditor.h>
#include <LibGUI/Label.h>
#include <LibJarvis/ConnectionToServer.h>
#include "ArcReactorWidget.h"

namespace JarvisAssistant {

class JarvisAssistantWidget final : public GUI::Widget {
    C_OBJECT(JarvisAssistantWidget)
public:
    virtual ~JarvisAssistantWidget() override = default;

    static ErrorOr<NonnullRefPtr<JarvisAssistantWidget>> try_create();
    ErrorOr<void> initialize();

private:
    JarvisAssistantWidget() = default;

    void execute_command_string(StringView command_str);
    void trigger_voice_interaction();

    RefPtr<ArcReactorWidget> m_arc_reactor;
    RefPtr<GUI::TextBox> m_capability_input;
    RefPtr<GUI::Button> m_execute_button;
    RefPtr<GUI::Button> m_voice_button;
    RefPtr<GUI::Button> m_btn_diag;
    RefPtr<GUI::Button> m_btn_shield;
    RefPtr<GUI::Button> m_btn_lockdown;
    RefPtr<GUI::Button> m_btn_journal;
    RefPtr<GUI::TextEditor> m_output_editor;
    RefPtr<GUI::Label> m_status_label;
    RefPtr<GUI::Label> m_shield_label;
    RefPtr<GUI::Label> m_ipc_label;
    RefPtr<Jarvis::ConnectionToServer> m_connection;
};

}
