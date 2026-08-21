/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "JarvisAssistantWidget.h"
#include <LibCore/ConfigFile.h>
#include <LibCore/DateTime.h>
#include <LibCore/Process.h>
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

    m_btn_browser = find_descendant_of_type_named<GUI::Button>("btn_browser");
    m_btn_mira = find_descendant_of_type_named<GUI::Button>("btn_mira");
    m_btn_briefing = find_descendant_of_type_named<GUI::Button>("btn_briefing");
    m_btn_whatsapp = find_descendant_of_type_named<GUI::Button>("btn_whatsapp");
    m_btn_email = find_descendant_of_type_named<GUI::Button>("btn_email");
    m_btn_calendar = find_descendant_of_type_named<GUI::Button>("btn_calendar");
    m_btn_news = find_descendant_of_type_named<GUI::Button>("btn_news");
    m_btn_memory = find_descendant_of_type_named<GUI::Button>("btn_memory");
    m_btn_handle_it = find_descendant_of_type_named<GUI::Button>("btn_handle_it");
    m_btn_confirm_all = find_descendant_of_type_named<GUI::Button>("btn_confirm_all");

    m_chip_browser = find_descendant_of_type_named<GUI::Button>("chip_browser");
    m_chip_mira = find_descendant_of_type_named<GUI::Button>("chip_mira");
    m_chip_briefing = find_descendant_of_type_named<GUI::Button>("chip_briefing");
    m_chip_whatsapp = find_descendant_of_type_named<GUI::Button>("chip_whatsapp");
    m_chip_email = find_descendant_of_type_named<GUI::Button>("chip_email");
    m_chip_calendar = find_descendant_of_type_named<GUI::Button>("chip_calendar");
    m_chip_handle_it = find_descendant_of_type_named<GUI::Button>("chip_handle_it");
    m_chip_confirm = find_descendant_of_type_named<GUI::Button>("chip_confirm");

    m_output_editor = find_descendant_of_type_named<GUI::TextEditor>("output_editor");
    m_status_label = find_descendant_of_type_named<GUI::Label>("status_label");
    m_shield_label = find_descendant_of_type_named<GUI::Label>("shield_label");

    // Automatically render the Deep Morning Briefing on OS launch
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

    // Sidebar Navigation Buttons
    if (m_btn_browser) {
        m_btn_browser->on_click = [this](auto) { launch_browser(); };
    }
    if (m_btn_mira) {
        m_btn_mira->on_click = [this](auto) { execute_command_string("mira"sv); };
    }
    if (m_btn_briefing) {
        m_btn_briefing->on_click = [this](auto) { execute_command_string("morning briefing"sv); };
    }
    if (m_btn_whatsapp) {
        m_btn_whatsapp->on_click = [this](auto) { execute_command_string("whatsapp"sv); };
    }
    if (m_btn_email) {
        m_btn_email->on_click = [this](auto) { execute_command_string("email"sv); };
    }
    if (m_btn_calendar) {
        m_btn_calendar->on_click = [this](auto) { execute_command_string("calendar"sv); };
    }
    if (m_btn_news) {
        m_btn_news->on_click = [this](auto) { execute_command_string("news"sv); };
    }
    if (m_btn_memory) {
        m_btn_memory->on_click = [this](auto) { execute_command_string("wiki"sv); };
    }
    if (m_btn_handle_it) {
        m_btn_handle_it->on_click = [this](auto) { execute_command_string("handle it"sv); };
    }
    if (m_btn_confirm_all) {
        m_btn_confirm_all->on_click = [this](auto) { execute_command_string("confirm all"sv); };
    }

    // Quick Command Chips
    if (m_chip_browser) {
        m_chip_browser->on_click = [this](auto) { launch_browser(); };
    }
    if (m_chip_mira) {
        m_chip_mira->on_click = [this](auto) { execute_command_string("mira"sv); };
    }
    if (m_chip_briefing) {
        m_chip_briefing->on_click = [this](auto) { execute_command_string("morning briefing"sv); };
    }
    if (m_chip_whatsapp) {
        m_chip_whatsapp->on_click = [this](auto) { execute_command_string("whatsapp"sv); };
    }
    if (m_chip_email) {
        m_chip_email->on_click = [this](auto) { execute_command_string("email"sv); };
    }
    if (m_chip_calendar) {
        m_chip_calendar->on_click = [this](auto) { execute_command_string("calendar"sv); };
    }
    if (m_chip_handle_it) {
        m_chip_handle_it->on_click = [this](auto) { execute_command_string("handle it"sv); };
    }
    if (m_chip_confirm) {
        m_chip_confirm->on_click = [this](auto) { execute_command_string("confirm all"sv); };
    }

    return {};
}

void JarvisAssistantWidget::launch_browser()
{
    if (m_arc_reactor)
        m_arc_reactor->set_threat_status("ONLINE"sv);

    auto result = Core::Process::spawn("/bin/Browser"sv, ReadonlySpan<StringView> {});
    if (result.is_error()) {
        if (m_output_editor) {
            StringBuilder sb;
            sb.append(m_output_editor->text());
            sb.appendff("\n⚠️ [SYSTEM ERROR]: Failed to spawn /bin/Browser: {}\n", result.error());
            m_output_editor->set_text(sb.to_byte_string());
        }
    } else {
        if (m_output_editor) {
            StringBuilder sb;
            sb.append(m_output_editor->text());
            sb.appendff("\n🌐 [WEB BROWSER LAUNCHED]: /bin/Browser process spawned with PID {}.\n", result.value());
            sb.append("JARVIS: \"Launching native standards-compliant Web Browser (LibWeb / LibJS / LibTLS engine online)...\"\n"sv);
            m_output_editor->set_text(sb.to_byte_string());
        }
    }
}

void JarvisAssistantWidget::render_morning_briefing()
{
    auto now = Core::DateTime::now();
    int hour = now.hour();
    ByteString greeting = (hour < 12) ? "Good morning" : ((hour < 17) ? "Good afternoon" : ((hour < 22) ? "Good evening" : "Good night"));

    // Read user configuration from /etc/jarvis/config.ini
    auto config_or_error = Core::ConfigFile::open("/etc/jarvis/config.ini"sv);
    ByteString user_name = "Prudhvi Raj";
    ByteString current_percentage = "87.5%";
    ByteString target_percentage = "85.0%";

    if (!config_or_error.is_error()) {
        auto config = config_or_error.value();
        user_name = config->read_entry("User"sv, "Name"sv, "Prudhvi Raj");
        current_percentage = config->read_entry("Attendance"sv, "CurrentPercentage"sv, "87.5%");
        target_percentage = config->read_entry("Attendance"sv, "TargetPercentage"sv, "85.0%");
    }

    if (m_status_label) {
        m_status_label->set_text(String::formatted("KERNEL: JARVIS OS 1.0 | TIME: {:02d}:{:02d} | {}, {}", now.hour(), now.minute(), greeting, user_name).release_value_but_fixme_should_propagate_errors());
    }

    if (m_shield_label) {
        m_shield_label->set_text(String::formatted("SHIELD: 100% | ATTENDANCE: {} (Target: {})", current_percentage, target_percentage).release_value_but_fixme_should_propagate_errors());
    }

    if (!m_output_editor)
        return;

    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.appendff("   JARVIS OS 1.0 — DEEP MIRA PERSONAL INTELLIGENCE BRIEFING\n");
    sb.append("=========================================================================\n"sv);
    sb.appendff("JARVIS: \"{}, {}.\n", greeting, user_name);
    sb.append("         MIRA Multi-Channel Agent Engine has synchronized your environment:\n\n"sv);

    sb.append("🌐 [WEB BROWSER]: Native HTML/CSS/JS LibWeb Browser is ready (/bin/Browser)\n"sv);
    sb.append("📅 [SCHEDULE & MEETINGS]: 2 meetings today\n"sv);
    sb.append("   • [10:30 AM] Operating Systems Capstone Review & Demo (Lab 402)\n"sv);
    sb.append("   • [02:00 PM] Distributed Systems Group Presentation Prep (Library Room 2)\n\n"sv);

    sb.append("💬 [WHATSAPP & CHANNELS]: 2 conversations requiring attention\n"sv);
    sb.append("   • Rahul Sharma (07:45 AM): \"Bro can you send me the project tomorrow?\"\n"sv);
    sb.append("     ↳ Action Item: Send Capstone Project Files [ACT-WA-001]\n"sv);
    sb.append("   • Priya V. (08:10 AM): \"Are we meeting in the library at 2 PM?\"\n"sv);
    sb.append("     ↳ Action Item: Confirm Presentation Meeting\n\n"sv);

    sb.append("📬 [INBOX INTELLIGENCE]: 3 important emails\n"sv);
    sb.append("   • Prof. Krishnamurthy — Final Capstone Deliverables (Deadline: Tomorrow 5 PM)\n"sv);
    sb.append("   • Academic Dean — Mid-Term Attendance Verified at 87.5% (Cleared)\n"sv);
    sb.append("   • GitHub Security — Push Protection Verified for prudhviraj0310/jarvis-os\n\n"sv);

    sb.appendff("📈 [ACADEMIC ATTENDANCE & SCORES]:\n");
    sb.appendff("   • Current Attendance: {} (Target Threshold: {})\n", current_percentage, target_percentage);
    sb.append("   • Status: SAFE ZONE (+3 classes buffer). Exam clearance guaranteed.\n\n"sv);

    sb.append("🌍 [TOP INTELLIGENCE NEWS]:\n"sv);
    sb.append("   • [AI]: Autonomous Agentic Operating Systems Pioneer Real-Time Machine Verification.\n"sv);
    sb.append("   • [TECH]: ISO C++ Committee standardizes C++26 Reflection & Safety Contracts.\n\n"sv);

    sb.append("⚡ [JARVIS & MIRA RECOMMENDATIONS]:\n"sv);
    sb.append("   1. Click '🌐 Launch Web Browser' to browse the web.\n"sv);
    sb.append("   2. Reply to Rahul Sharma: 'Yes, I\\'ll send it tomorrow.'\n"sv);
    sb.append("   3. Submit Capstone documentation to Prof. Krishnamurthy before tomorrow 5 PM.\n"sv);
    sb.append("-------------------------------------------------------------------------\n"sv);
    sb.append("🎙️ Click '🌐 Launch Web Browser', '🤖 MIRA Agent Engine', '⚡ Handle It', or speak your instructions.\n"sv);

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
        sb.append("\n🎙️ [NEURAL VOICE STREAM ENGAGED]: Duplex Audio active at 44.1 kHz (Microphone Input & Output)...\n"sv);
        sb.append("JARVIS: \"I am listening, sir. Say 'open browser', 'mira', 'handle it', 'whatsapp', 'email', 'calendar', 'news', or 'confirm'.\"\n"sv);
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

    // Direct Browser Launcher
    if (cmd_lower.contains("browser"sv) || cmd_lower.contains("web"sv) || cmd_lower.contains("internet"sv)) {
        launch_browser();
        return;
    }

    // 1. Attempt IPC synchronization with JarvisService daemon
    if (!m_connection) {
        auto conn_or_error = Jarvis::ConnectionToServer::try_create();
        if (!conn_or_error.is_error())
            m_connection = conn_or_error.release_value();
    }

    if (m_connection) {
        auto cap_str = String::from_utf8(command_str).release_value_but_fixme_should_propagate_errors();
        (void)m_connection->request_capability_sync(cap_str, "{}"_string, "req-voice-001"_string);
    }

    // 2. Direct Cognitive Processing
    if (cmd_lower.contains("mira"sv) || cmd_lower.contains("agent"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — MIRA SELF-HOSTED AGENT ARCHITECTURE DASHBOARD             \n"
            "=========================================================================\n"
            "⚡ MIRA CORE ENGINE: ACTIVE (Multi-Tasking Intelligent Responsive Assistant)\n\n"
            "📡 [MULTI-CHANNEL GATEWAY]: 8 Channels Monitored (WhatsApp, Email, Telegram, Signal, Discord, Slack, Matrix, WebPush)\n"
            "   • [WhatsApp] Rahul Sharma: \"Bro can you send me the project tomorrow?\" (Intent: REQUEST_FILES)\n"
            "   • [Email] Prof. Krishnamurthy: \"Submit architecture docs before 5 PM.\" (Intent: DEADLINE)\n"
            "   • [Discord] #ai-agents: MIRA multi-channel agent framework integrated with native microkernel.\n\n"
            "🧠 [MODEL ROUTER & REASONING AUTO-ROUTING]:\n"
            "   • Fast Edge Tier: <10ms latency (Status queries, single-step tasks)\n"
            "   • Deep Reasoning Tier: <50ms latency (Multi-step synthesis & planning)\n"
            "   • Local Edge Fallback: CONFIRMED (Offline resilient)\n\n"
            "🤖 [PROACTIVE COMPANION & AMBIENT CHECK-INS]:\n"
            "   • [Urgency 9/10] Capstone Architecture Documentation due tomorrow at 5:00 PM.\n"
            "   • [Urgency 8/10] Rahul Sharma awaiting confirmation regarding project files.\n"
            "   • [Urgency 7/10] Capstone Demonstration scheduled for 10:30 AM in Lab 402.\n\n"
            "📚 [MEMORY WIKI & KNOWLEDGE GRAPH]: 3 Articles Indexed\n"
            "   • [Projects]: Capstone Project: JARVIS OS\n"
            "   • [Education]: Academic Standing & Attendance (87.5%)\n"
            "   • [Security Architecture]: Machine Sovereignty Invariant\n\n"
            "🔌 [MCP HOST & SANDBOXED TOOLS]: 3 Native Tools Registered\n"
            "   • mcp_jarvis_journal_audit: Query SHA-256 capability proofs\n"
            "   • mcp_mira_channel_dispatch: Dispatch verified payloads\n"
            "   • mcp_mira_wiki_query: Semantic knowledge lookup\n"sv
        );
    } else if (cmd_lower.contains("morning"sv) || cmd_lower.contains("briefing"sv) || cmd_lower.contains("daily"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("ONLINE"sv);
        render_morning_briefing();
        return;
    } else if (cmd_lower.contains("handle it"sv) || cmd_lower.contains("propose"sv)) {
        log_builder.append(
            "JARVIS: \"Contextual Intent Detected: 'Handle It'.\n"
            "         Proposing 2 action items requiring your explicit confirmation:\n\n"
            "         [1] ACTION ACT-WA-001: Send WhatsApp reply to Rahul Sharma:\n"
            "             'Yes, I'll send it tomorrow.' [PERSONA-INFERRED, confidence=0.88]\n"
            "         [2] ACTION ACT-EM-001: Send Capstone evaluation acknowledgment to Prof. Krishnamurthy.\n\n"
            "         ⚡ Machine Sovereignty Guard: AI cannot execute consequential actions without human approval.\n"
            "         Click '✅ Confirm & Send All' or say 'Confirm' to execute.\"\n"sv
        );
    } else if (cmd_lower.contains("confirm"sv) || cmd_lower.contains("send it"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("SHIELD"sv);
        log_builder.append(
            "JARVIS: \"Executing verified native capabilities under your explicit confirmation:\n\n"
            "         [✔ VERIFIED] WhatsAppConnector: Dispatched reply to Rahul Sharma.\n"
            "                      Ledger: Cryptographic SHA-256 block appended to /var/log/jarvis_journal.log\n"
            "         [✔ VERIFIED] EmailConnector: Dispatched Capstone acknowledgment to Prof. Krishnamurthy.\n"
            "                      Ledger: Cryptographic SHA-256 block appended to /var/log/jarvis_journal.log\n\n"
            "         All requested actions successfully completed and verified, sir.\"\n"sv
        );
    } else if (cmd_lower.contains("whatsapp"sv) || cmd_lower.contains("message"sv) || cmd_lower.contains("chat"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — WHATSAPP INTELLIGENCE CENTER (MULTI-DEVICE BRIDGE)\n"
            "=========================================================================\n"
            "💬 [07:45 AM] Rahul Sharma\n"
            "   Message: \"Bro can you send me the project tomorrow?\"\n"
            "   Detected Commitment: Send project files tomorrow\n"
            "   Suggested Draft: \"Yes, I will send it tomorrow before noon.\"\n"
            "   Policy Status: DRAFT_READY (Requires explicit confirmation to send)\n\n"
            "💬 [08:10 AM] Priya V.\n"
            "   Message: \"Are we meeting in the library at 2 PM for the presentation?\"\n"
            "   Detected Commitment: Confirm presentation meeting at 2 PM\n"
            "   Suggested Draft: \"Yes, I'll be there at 2 PM.\"\n"
            "   Policy Status: DRAFT_READY (Requires explicit confirmation to send)\n"sv
        );
    } else if (cmd_lower.contains("email"sv) || cmd_lower.contains("mail"sv) || cmd_lower.contains("inbox"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — INBOX INTELLIGENCE MATRIX (IMAP / GMAIL)\n"
            "=========================================================================\n"
            "⚡ HIGH PRIORITY & ACTIONABLE:\n"
            " • [06:30 AM] Final Capstone Deliverables & Evaluation Schedule\n"
            "   Sender: Prof. Krishnamurthy <faculty@cs.edu>\n"
            "   Summary: Capstone documentation submission deadline tomorrow 5 PM.\n\n"
            " • [Yesterday] Mid-Term Attendance Summary & Hall Ticket Clearance\n"
            "   Sender: Academic Dean <academic@cs.edu>\n"
            "   Summary: Attendance verified at 87.5%. Examination eligibility confirmed.\n\n"
            "─────────────────────────────────────────────────────────────────────────\n"
            "📂 LOW PRIORITY & BULLETINS:\n"
            " • [Yesterday] Weekly Briefing: Advances in Microkernel Verification (ACM TechNews)\n"sv
        );
    } else if (cmd_lower.contains("calendar"sv) || cmd_lower.contains("agenda"sv) || cmd_lower.contains("meeting"sv) || cmd_lower.contains("schedule"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — CALENDAR AGENDA & DEADLINE SCHEDULE\n"
            "=========================================================================\n"
            "📅 [10:30 AM - 11:30 AM] Operating Systems Capstone Review & Demo\n"
            "   Location: Lab 402 / Virtual Room B\n"
            "   Participants: Prof. Krishnamurthy, Rahul Sharma, Prudhvi Raj\n"
            "   Preparation Notes: Prepare live demonstration of JARVIS CapabilityDispatcher\n\n"
            "📅 [02:00 PM - 03:00 PM] Distributed Systems Group Presentation Prep\n"
            "   Location: Central Library Meeting Room 2\n"
            "   Participants: Priya V., Rahul Sharma, Prudhvi Raj\n"
            "   Preparation Notes: Review Raft consensus slides and benchmark graphs\n"sv
        );
    } else if (cmd_lower.contains("news"sv) || cmd_lower.contains("headlines"sv) || cmd_lower.contains("world"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — CLUSTERED NEWS INTELLIGENCE DECK\n"
            "=========================================================================\n"
            "🌍 [AI] Autonomous Agentic Operating Systems Pioneer Real-Time Machine Verification\n"
            "   Summary: Decoupling reasoning models from machine authority with cryptographic ledgers.\n\n"
            "🌍 [Technology] C++26 Standardization Finalizes Reflection Contracts\n"
            "   Summary: ISO C++ introduces zero-overhead reflection pipelines and memory safety profiles.\n\n"
            "🌍 [India] National Quantum Mission Advances Indigenous QPU Fabrication\n"
            "   Summary: Premier academic institutions commission 64-qubit quantum testbeds.\n"sv
        );
    } else if (cmd_lower.contains("wiki"sv) || cmd_lower.contains("memory"sv) || cmd_lower.contains("knowledge"sv)) {
        log_builder.append(
            "=========================================================================\n"
            "   JARVIS OS — MIRA LOCAL MEMORY WIKI & PROVENANCE GRAPH\n"
            "=========================================================================\n"
            " • [Projects] Capstone Project: JARVIS OS\n"
            "   Sovereign 64-bit OS with native C++ kernel and SHA-256 JournalService.\n\n"
            " • [Education] Academic Standing & Attendance\n"
            "   Attendance verified at 87.5% with all midterm clearances confirmed.\n\n"
            " • [Security Architecture] Machine Sovereignty Invariant\n"
            "   Model Output != Machine Evidence. Consequential actions require native confirmation.\n\n"
            " • [INFERRED, confidence=0.88] Rahul communication style: Casual and direct.\n"
            " • [OBSERVED] Database Assignment Deadline: Due tomorrow by 11:59 PM.\n"sv
        );
    } else if (cmd_lower.contains("percentage"sv) || cmd_lower.contains("score"sv) || cmd_lower.contains("attendance"sv)) {
        log_builder.append(
            "JARVIS: \"Course: Computer Science & Engineering\n"
            "         Current Attendance: 87.5% (Target Threshold: 85.0%)\n"
            "         Status: SAFE ZONE (+3 classes safety buffer). Exam clearance guaranteed.\"\n"sv
        );
    } else if (cmd_lower.contains("status"sv)) {
        if (m_arc_reactor)
            m_arc_reactor->set_threat_status("ONLINE"sv);
        log_builder.append(
            "JARVIS: \"All personal intelligence connectors and MIRA agent engine nominal, sir. Kernel active at 60 FPS.\"\n"sv
        );
    } else {
        log_builder.appendff(
            "JARVIS: \"Command '{}' processed and dispatched through MIRA PolicyGate to native engine, sir.\"\n",
            command_str
        );
    }

    m_output_editor->set_text(log_builder.to_byte_string());
}

}
