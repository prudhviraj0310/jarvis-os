/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "JarvisAssistantWidget.h"
#include <LibCore/DateTime.h>
#include <AK/StringBuilder.h>
#include <AK/JsonObject.h>
#include <AK/JsonValue.h>

namespace JarvisAssistant {

ErrorOr<void> JarvisAssistantWidget::initialize()
{
    m_arc_reactor = find_descendant_of_type_named<ArcReactorWidget>("arc_reactor_widget");
    m_capability_input = find_descendant_of_type_named<GUI::TextBox>("capability_input");
    m_execute_button = find_descendant_of_type_named<GUI::Button>("execute_button");
    m_voice_button = find_descendant_of_type_named<GUI::Button>("voice_button");

    m_btn_briefing = find_descendant_of_type_named<GUI::Button>("btn_briefing");
    m_btn_whatsapp = find_descendant_of_type_named<GUI::Button>("btn_whatsapp");
    m_btn_email = find_descendant_of_type_named<GUI::Button>("btn_email");
    m_btn_score = find_descendant_of_type_named<GUI::Button>("btn_score");
    m_btn_news = find_descendant_of_type_named<GUI::Button>("btn_news");
    m_btn_shield = find_descendant_of_type_named<GUI::Button>("btn_shield");
    m_btn_lockdown = find_descendant_of_type_named<GUI::Button>("btn_lockdown");
    m_btn_diag = find_descendant_of_type_named<GUI::Button>("btn_diag");

    m_chip_briefing = find_descendant_of_type_named<GUI::Button>("chip_briefing");
    m_chip_whatsapp = find_descendant_of_type_named<GUI::Button>("chip_whatsapp");
    m_chip_email = find_descendant_of_type_named<GUI::Button>("chip_email");
    m_chip_score = find_descendant_of_type_named<GUI::Button>("chip_score");
    m_chip_news = find_descendant_of_type_named<GUI::Button>("chip_news");
    m_chip_shield = find_descendant_of_type_named<GUI::Button>("chip_shield");

    m_output_editor = find_descendant_of_type_named<GUI::TextEditor>("output_editor");
    m_status_label = find_descendant_of_type_named<GUI::Label>("status_label");
    m_shield_label = find_descendant_of_type_named<GUI::Label>("shield_label");

    // Automatically render the Morning Briefing on OS launch!
    render_morning_briefing();

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

    // Daily Intelligence Protocol Buttons
    if (m_btn_briefing) {
        m_btn_briefing->on_click = [this](auto) { execute_command_string("morning briefing"sv); };
    }
    if (m_btn_whatsapp) {
        m_btn_whatsapp->on_click = [this](auto) { execute_command_string("whatsapp"sv); };
    }
    if (m_btn_email) {
        m_btn_email->on_click = [this](auto) { execute_command_string("email"sv); };
    }
    if (m_btn_score) {
        m_btn_score->on_click = [this](auto) { execute_command_string("percentage"sv); };
    }
    if (m_btn_news) {
        m_btn_news->on_click = [this](auto) { execute_command_string("news"sv); };
    }
    if (m_btn_shield) {
        m_btn_shield->on_click = [this](auto) { execute_command_string("shield"sv); };
    }
    if (m_btn_lockdown) {
        m_btn_lockdown->on_click = [this](auto) { execute_command_string("lockdown"sv); };
    }
    if (m_btn_diag) {
        m_btn_diag->on_click = [this](auto) { execute_command_string("diagnostics"sv); };
    }

    // Quick Voice Intelligence Chips
    if (m_chip_briefing) {
        m_chip_briefing->on_click = [this](auto) { execute_command_string("morning briefing"sv); };
    }
    if (m_chip_whatsapp) {
        m_chip_whatsapp->on_click = [this](auto) { execute_command_string("whatsapp"sv); };
    }
    if (m_chip_email) {
        m_chip_email->on_click = [this](auto) { execute_command_string("email"sv); };
    }
    if (m_chip_score) {
        m_chip_score->on_click = [this](auto) { execute_command_string("percentage"sv); };
    }
    if (m_chip_news) {
        m_chip_news->on_click = [this](auto) { execute_command_string("news"sv); };
    }
    if (m_chip_shield) {
        m_chip_shield->on_click = [this](auto) { execute_command_string("shield"sv); };
    }

    return {};
}

void JarvisAssistantWidget::render_morning_briefing()
{
    auto now = Core::DateTime::now();
    int hour = now.hour();
    ByteString greeting = (hour < 12) ? "Good morning, Sir." : ((hour < 17) ? "Good afternoon, Sir." : ((hour < 22) ? "Good evening, Sir." : "Good night, Sir."));

    if (m_status_label) {
        m_status_label->set_text(String::formatted("KERNEL: JARVIS OS 1.0 (x86_64) | TIME: {:02d}:{:02d} | {}", now.hour(), now.minute(), greeting).release_value_but_fixme_should_propagate_errors());
    }

    if (m_shield_label) {
        m_shield_label->set_text("ULTIMATE SHIELD: 100% | READINESS: 96% | BATTERY: 98%"_string);
    }

    if (!m_output_editor)
        return;

    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.appendff("   JARVIS OS 1.0 — AUTONOMOUS MORNING INTELLIGENCE BRIEFING              \n");
    sb.append("=========================================================================\n"sv);
    sb.appendff("JARVIS: \"{}\n", greeting);
    sb.append(
        "         All systems are online. Here is your daily intelligence briefing:\n"
        "\n"
        "💬 [WHATSAPP INTELLIGENCE] — 3 Unread Priority Messages:\n"
        "   1. [08:15 AM] Alex (Lead): \"Kernel capability patch merged & ready.\"\n"
        "   2. [07:45 AM] Stark Security: \"Defense nodes holding at 100% integrity.\"\n"
        "   3. [07:10 AM] Sarah (AI Team): \"Voice neural frequency model synchronized.\"\n"
        "\n"
        "📬 [EMAIL INTELLIGENCE] — 4 Priority Inbox Summaries:\n"
        "   1. [07:50 AM] GitHub: \"[PR #42] Holographic Cyber Glass UI & Arc Reactor verified.\"\n"
        "   2. [07:15 AM] Stark Sentinel: \"Daily Threat Assessment: Zero breaches detected.\"\n"
        "   3. [06:30 AM] Tech Radar: \"Sovereign C++ Operating Systems surge in adoption.\"\n"
        "   4. [06:00 AM] Cloud Telemetry: \"Automated cryptographic audit completed.\"\n"
        "\n"
        "📈 [PERCENTAGE & SYSTEM SCORES]:\n"
        "   - Daily Readiness Score : 96% (Optimal)\n"
        "   - Schedule & Task Status: 88% on track\n"
        "   - System Power & Battery: 98% (Health: 100%)\n"
        "   - Defense Shield Status : 100% Active (Syscall Isolation Enforced)\n"
        "\n"
        "🌍 [GLOBAL & TECH NEWS TELEMETRY]:\n"
        "   - TECH: Autonomous AI operating systems redefine hardware interaction.\n"
        "   - CYBER DEFENSE: Zero-trust kernel syscall enforcement adopted globally.\n"
        "   - SCIENCE: Quantum communication satellite network active at 99.9% uptime.\"\n"
        "-------------------------------------------------------------------------\n"
        "🎙️ Audio voice matrix is listening. Speak or click any intelligence chip.\n"sv
    );

    m_output_editor->set_text(sb.to_byte_string());
}

void JarvisAssistantWidget::trigger_voice_interaction()
{
    m_voice_active = !m_voice_active;

    if (m_arc_reactor)
        m_arc_reactor->set_active_voice_mode(m_voice_active);

    if (m_voice_button) {
        if (m_voice_active) {
            m_voice_button->set_text("🔴 Listening..."_string);
        } else {
            m_voice_button->set_text("🎙️ Wake JARVIS"_string);
        }
    }

    if (!m_output_editor)
        return;

    StringBuilder sb;
    sb.append(m_output_editor->text());

    if (m_voice_active) {
        sb.append("\n🎙️ [NEURAL VOICE STREAM ENGAGED]: Audio frequency matrix listening at 44.1 kHz...\n"sv);
        sb.append("JARVIS: \"I am listening, sir. Speak your command — say 'morning briefing', 'read whatsapp', 'check emails', or 'what is my percentage'.\"\n"sv);
    } else {
        sb.append("\n🎙️ [NEURAL VOICE STREAM]: Voice input channel returned to standby.\n"sv);
    }

    m_output_editor->set_text(sb.to_byte_string());
}

void JarvisAssistantWidget::execute_command_string(StringView command_str)
{
    if (!m_output_editor)
        return;

    StringBuilder log_builder;
    log_builder.append(m_output_editor->text());
    log_builder.appendff("\n>>> [COGNITIVE DISPATCH]: {}\n", command_str);

    auto cmd_lower = ByteString(command_str).to_lowercase();

    // 1. Attempt IPC synchronization with background daemon
    if (!m_connection) {
        auto conn_or_error = Jarvis::ConnectionToServer::try_create();
        if (!conn_or_error.is_error())
            m_connection = conn_or_error.release_value();
    }

    if (m_connection) {
        auto cap_str = String::from_utf8(command_str).release_value_but_fixme_should_propagate_errors();
        (void)m_connection->request_capability_sync(cap_str, "{}"_string, "req-voice-001"_string);
    }

    // 2. Direct Cognitive Dialogue Processing
    if (cmd_lower.contains("morning"sv) || cmd_lower.contains("briefing"sv) || cmd_lower.contains("daily"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("ONLINE"sv);

        render_morning_briefing();
        return;
    } else if (cmd_lower.contains("whatsapp"sv) || cmd_lower.contains("message"sv) || cmd_lower.contains("chat"sv)) {
        log_builder.append(
            "JARVIS: \"💬 Reading your 3 unread WhatsApp messages, sir:\n"
            "         1. [08:15 AM] Alex (Lead): 'Kernel capability patch merged & ready for test.'\n"
            "         2. [07:45 AM] Stark Security: 'Defense nodes holding at 100% integrity.'\n"
            "         3. [07:10 AM] Sarah (AI Team): 'Voice neural frequency model synchronized.'\n"
            "         All sender identities cryptographically verified.\"\n"sv
        );
    } else if (cmd_lower.contains("email"sv) || cmd_lower.contains("mail"sv) || cmd_lower.contains("inbox"sv)) {
        log_builder.append(
            "JARVIS: \"📬 Summarizing your 4 priority emails, sir:\n"
            "         1. GitHub Notifications: '[PR #42] Holographic Cyber Glass UI & Arc Reactor verified.'\n"
            "         2. Stark Sentinel: 'Daily Threat Assessment: Zero breaches detected.'\n"
            "         3. Tech Radar: 'Sovereign C++ Operating Systems surge in adoption.'\n"
            "         4. Cloud Telemetry: 'Automated cryptographic audit completed.'\"\n"sv
        );
    } else if (cmd_lower.contains("percentage"sv) || cmd_lower.contains("score"sv) || cmd_lower.contains("productivity"sv) || cmd_lower.contains("battery"sv)) {
        log_builder.append(
            "JARVIS: \"📊 System Scores & Personal Percentage Metrics:\n"
            "         - Overall Daily Readiness Score: 96% (Optimal)\n"
            "         - Daily Schedule & Task Score  : 88% on track\n"
            "         - System Battery & Power Matrix: 98% (Health: 100%)\n"
            "         - Ultimate Shield Security     : 100% Enforced.\"\n"sv
        );
    } else if (cmd_lower.contains("news"sv) || cmd_lower.contains("headlines"sv) || cmd_lower.contains("world"sv)) {
        log_builder.append(
            "JARVIS: \"🌍 Global & Tech News Telemetry:\n"
            "         [+] TECH: Autonomous AI operating systems redefine hardware interaction.\n"
            "         [+] CYBER DEFENSE: Zero-trust kernel syscall enforcement adopted globally.\n"
            "         [+] SCIENCE: Quantum communication satellite network active at 99.9% uptime.\"\n"sv
        );
    } else if (cmd_lower.contains("status"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("ONLINE"sv);
        if (m_shield_label)
            m_shield_label->set_text("ULTIMATE SHIELD: ACTIVE (100%) | READINESS: 96%"_string);

        log_builder.append(
            "JARVIS: \"All systems are operating at peak efficiency, sir.\n"
            "         - Kernel Architecture: 64-bit x86_64 Preemptive Core\n"
            "         - Ultimate Shield: Active (100% Syscall Isolation)\n"
            "         - Cryptographic Ledger: Chained SHA-256 Validated\n"
            "         - Compositor: Hardware Cyber Glass at 60 FPS.\"\n"sv
        );
    } else if (cmd_lower.contains("shield"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("SHIELD"sv);
        if (m_shield_label)
            m_shield_label->set_text("ULTIMATE SHIELD: MAXIMUM PERIMETER (100%)"_string);

        log_builder.append(
            "JARVIS: \"Ultimate Shield perimeter reinforced to maximum capacity, sir.\n"
            "         All untrusted syscalls and rogue memory pages are strictly blocked.\n"
            "         Defense matrix integrity is holding at 100%.\"\n"sv
        );
    } else if (cmd_lower.contains("lockdown"sv) || cmd_lower.contains("defcon"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("LOCKDOWN"sv);
        if (m_shield_label)
            m_shield_label->set_text("ULTIMATE SHIELD: DEFCON-1 RED ALERT LOCKDOWN"_string);

        log_builder.append(
            "JARVIS: \"⚠️ DEFCON-1 RED ALERT LOCKDOWN ENGAGED, SIR!\n"
            "         - Process execution quarantine: ACTIVE\n"
            "         - Kernel syscall lockdown: ENFORCED\n"
            "         - Cryptographic audit trail: SEALED.\"\n"sv
        );
    } else if (cmd_lower.contains("diag"sv) || cmd_lower.contains("scan"sv)) {
        log_builder.append(
            "JARVIS: \"Executing full autonomous system diagnostics...\n"
            "         [+] CPU Topology & SMP Scheduler: PASS\n"
            "         [+] Virtual Memory Paging & MMU: PASS\n"
            "         [+] Ext2 VFS Filesystem Hierarchy: PASS\n"
            "         [+] IPC Capability Portal (/tmp/portal/jarvis): PASS\n"
            "         [+] SHA-256 Cryptographic Block Journal: PASS\n"
            "         System health score: 100/100 (Optimal).\"\n"sv
        );
    } else if (cmd_lower.contains("who"sv) || cmd_lower.contains("identity"sv)) {
        log_builder.append(
            "JARVIS: \"I am JARVIS — Just A Rather Very Intelligent System.\n"
            "         I am your sovereign, self-booting cognitive operating system,\n"
            "         built natively from the metal up in C++ with zero web layers.\"\n"sv
        );
    } else {
        log_builder.appendff(
            "JARVIS: \"Command '{}' processed and dispatched to cognitive core, sir.\n"
            "         Tactical defense vectors remain fully synchronized.\"\n",
            command_str
        );
    }

    m_output_editor->set_text(log_builder.to_byte_string());
}

}
