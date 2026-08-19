/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "JarvisAssistantWidget.h"
#include <LibCore/DateTime.h>
#include <AK/JsonObject.h>
#include <AK/JsonValue.h>

namespace JarvisAssistant {

ErrorOr<void> JarvisAssistantWidget::initialize()
{
    m_arc_reactor = find_descendant_of_type_named<ArcReactorWidget>("arc_reactor_widget");
    m_capability_input = find_descendant_of_type_named<GUI::TextBox>("capability_input");
    m_execute_button = find_descendant_of_type_named<GUI::Button>("execute_button");
    m_voice_button = find_descendant_of_type_named<GUI::Button>("voice_button");
    m_btn_diag = find_descendant_of_type_named<GUI::Button>("btn_diag");
    m_btn_shield = find_descendant_of_type_named<GUI::Button>("btn_shield");
    m_btn_lockdown = find_descendant_of_type_named<GUI::Button>("btn_lockdown");
    m_btn_journal = find_descendant_of_type_named<GUI::Button>("btn_journal");
    m_output_editor = find_descendant_of_type_named<GUI::TextEditor>("output_editor");
    m_status_label = find_descendant_of_type_named<GUI::Label>("status_label");
    m_shield_label = find_descendant_of_type_named<GUI::Label>("shield_label");
    m_ipc_label = find_descendant_of_type_named<GUI::Label>("ipc_label");

    if (m_output_editor) {
        m_output_editor->set_text("[JARVIS OS Holographic Tactical Matrix Online]\nKernel: JARVIS OS 1.0 (Foundation x86_64)\nNeural Interface & Ultimate Shield Subsystem: ACTIVE\nIPC Portal: /tmp/portal/jarvis (Operational)\nReady for voice and tactical command dispatch.\n"sv);
    }

    if (m_execute_button) {
        m_execute_button->on_click = [this](auto) {
            if (m_capability_input) {
                auto text = m_capability_input->text();
                if (!text.is_empty()) {
                    execute_command_string(text);
                    m_capability_input->set_text(""sv);
                }
            }
        };
    }

    if (m_voice_button) {
        m_voice_button->on_click = [this](auto) {
            trigger_voice_interaction();
        };
    }

    if (m_capability_input) {
        m_capability_input->on_return_pressed = [this]() {
            auto text = m_capability_input->text();
            if (!text.is_empty()) {
                execute_command_string(text);
                m_capability_input->set_text(""sv);
            }
        };
    }

    if (m_btn_diag) {
        m_btn_diag->on_click = [this](auto) {
            execute_command_string("voice.diagnostics"sv);
        };
    }

    if (m_btn_shield) {
        m_btn_shield->on_click = [this](auto) {
            execute_command_string("voice.shield"sv);
        };
    }

    if (m_btn_lockdown) {
        m_btn_lockdown->on_click = [this](auto) {
            execute_command_string("voice.lockdown"sv);
        };
    }

    if (m_btn_journal) {
        m_btn_journal->on_click = [this](auto) {
            execute_command_string("security.shield_status"sv);
        };
    }

    return {};
}

void JarvisAssistantWidget::trigger_voice_interaction()
{
    if (m_arc_reactor)
        m_arc_reactor->set_active_voice_mode(true);

    if (m_output_editor) {
        StringBuilder sb;
        sb.append(m_output_editor->text());
        sb.append("\n[VOICE COMMAND ENGAGED] Listening on audio frequency matrix...\n"sv);
        m_output_editor->set_text(sb.to_byte_string());
    }

    execute_command_string("voice.status"sv);
}

void JarvisAssistantWidget::execute_command_string(StringView command_str)
{
    if (!m_output_editor)
        return;

    StringBuilder log_builder;
    log_builder.append(m_output_editor->text());
    log_builder.appendff("\n>>> [COGNITIVE DISPATCH]: {}\n", command_str);

    if (!m_connection) {
        auto conn_or_error = Jarvis::ConnectionToServer::try_create();
        if (!conn_or_error.is_error())
            m_connection = conn_or_error.release_value();
    }

    if (m_connection) {
        auto cap_str = String::from_utf8(command_str).release_value_but_fixme_should_propagate_errors();
        auto result_or_error = m_connection->request_capability_sync(cap_str, "{}"_string, "req-voice-001"_string);

        if (result_or_error.is_error()) {
            log_builder.appendff("ERROR: IPC capability dispatch failure\n");
        } else {
            auto result_json = result_or_error.value();
            log_builder.appendff("JARVIS: {}\n", result_json);

            if (result_json.contains("LOCKDOWN"sv)) {
                if (m_arc_reactor)
                    m_arc_reactor->set_threat_status("LOCKDOWN"sv);
                if (m_shield_label)
                    m_shield_label->set_text("ULTIMATE SHIELD: DEFCON-1 LOCKDOWN"_string);
            } else {
                if (m_arc_reactor)
                    m_arc_reactor->set_threat_status("ONLINE"sv);
                if (m_shield_label)
                    m_shield_label->set_text("ULTIMATE SHIELD: ACTIVE | Threat Matrix: NOMINAL"_string);
            }
        }
    } else {
        log_builder.appendff("JARVIS: Subsystem acknowledged command: {}\n", command_str);
    }

    m_output_editor->set_text(log_builder.to_byte_string());
}

}
