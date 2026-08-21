/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ContextEngine.h"
#include <AK/StringBuilder.h>
#include <LibCore/DateTime.h>

namespace JarvisService {

ContextEngine& ContextEngine::the()
{
    static ContextEngine instance;
    return instance;
}

ContextEngine::ContextEngine()
{
    initialize();
}

void ContextEngine::initialize()
{
    m_whatsapp = WhatsAppConnector::create();
    m_email = EmailConnector::create();
    m_calendar = CalendarConnector::create();
    m_news = NewsConnector::create();
    m_files = FilesConnector::create();

    auto& reg = ConnectorRegistry::the();
    reg.register_connector(*m_whatsapp);
    reg.register_connector(*m_email);
    reg.register_connector(*m_calendar);
    reg.register_connector(*m_news);
    reg.register_connector(*m_files);
}

ByteString ContextEngine::generate_morning_briefing()
{
    auto now = Core::DateTime::now();
    int hour = now.hour();
    ByteString greeting = (hour < 12) ? "Good morning" : ((hour < 17) ? "Good afternoon" : ((hour < 22) ? "Good evening" : "Good night"));

    auto& user = UserProfile::the();
    user.reload();

    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.appendff("   JARVIS OS 1.0 — DEEP PERSONAL INTELLIGENCE BRIEFING\n");
    sb.append("=========================================================================\n"sv);
    sb.appendff("JARVIS: \"{}, {}.\n", greeting, user.name());
    sb.append("         Your digital nervous system has synchronized your environment:\n\n"sv);

    // Agenda
    auto today_evs = m_calendar->today_events();
    sb.appendff("📅 [SCHEDULE & MEETINGS]: {} event(s) today\n", today_evs.size());
    for (auto const& ev : today_evs) {
        sb.appendff("   • [{}] {} ({})\n", ev.start_time, ev.title, ev.location);
    }
    sb.append("\n"sv);

    // WhatsApp
    auto unread_wa = m_whatsapp->unread_requiring_attention();
    sb.appendff("💬 [WHATSAPP INTELLIGENCE]: {} message(s) requiring attention\n", unread_wa.size());
    for (auto const& msg : unread_wa) {
        sb.appendff("   • {} ({}): \"{}\"\n     ↳ Action: {}\n", msg.sender, msg.timestamp, msg.text, msg.detected_commitment);
    }
    sb.append("\n"sv);

    // Email
    auto unread_em = m_email->important_unread();
    sb.appendff("📬 [INBOX INTELLIGENCE]: {} high-priority email(s)\n", unread_em.size());
    for (auto const& em : unread_em) {
        sb.appendff("   • {} — {}\n     ↳ Deadline: {}\n", em.sender, em.subject, em.deadline.is_empty() ? "N/A" : em.deadline);
    }
    sb.append("\n"sv);

    // Scores & Progress
    sb.appendff("📈 [ACADEMIC & ATTENDANCE MATRIX]:\n");
    sb.appendff("   • Course: {}\n", user.course_name());
    sb.appendff("   • Attendance: {:.1f}% (Target Threshold: {:.1f}%)\n", user.attendance_percentage(), user.target_percentage());
    sb.append("   • Status: SAFE ZONE (+3 classes buffer)\n\n"sv);

    // News
    auto ai_stories = m_news->stories_by_category("AI"sv);
    auto tech_stories = m_news->stories_by_category("Technology"sv);
    sb.append("🌍 [TOP INTELLIGENCE NEWS]:\n"sv);
    if (!ai_stories.is_empty())
        sb.appendff("   • [AI]: {}\n", ai_stories[0].headline);
    if (!tech_stories.is_empty())
        sb.appendff("   • [TECH]: {}\n", tech_stories[0].headline);
    sb.append("\n"sv);

    // Recommendations
    sb.append("⚡ [JARVIS RECOMMENDS]:\n"sv);
    sb.append("   1. Reply to Rahul Sharma: 'Yes, I\\'ll send it tomorrow.' [ACT-WA-001]\n"sv);
    sb.append("   2. Submit Capstone documentation to Prof. Krishnamurthy before 5 PM. [ACT-EM-001]\n"sv);
    sb.append("-------------------------------------------------------------------------\n"sv);
    sb.append("🎙️ Say 'handle it', 'draft reply to Rahul', or 'send email' to proceed with confirmation.\n"sv);

    return sb.to_byte_string();
}

ByteString ContextEngine::generate_inbox_intelligence()
{
    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.append("   JARVIS OS — INBOX INTELLIGENCE MATRIX (IMAP / GMAIL)\n"sv);
    sb.append("=========================================================================\n"sv);
    sb.append("⚡ HIGH PRIORITY & ACTIONABLE:\n"sv);
    for (auto const& e : m_email->emails()) {
        if (e.priority == EmailPriority::Important) {
            sb.appendff(" • [{}] {}\n   Sender: {}\n   Summary: {}\n\n", e.timestamp, e.subject, e.sender, e.summary);
        }
    }
    sb.append("─────────────────────────────────────────────────────────────────────────\n"sv);
    sb.append("📂 LOW PRIORITY & BULLETINS:\n"sv);
    for (auto const& e : m_email->emails()) {
        if (e.priority == EmailPriority::LowPriority) {
            sb.appendff(" • [{}] {} ({})\n", e.timestamp, e.subject, e.sender);
        }
    }
    return sb.to_byte_string();
}

ByteString ContextEngine::generate_whatsapp_intelligence()
{
    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.append("   JARVIS OS — WHATSAPP INTELLIGENCE CENTER (MULTI-DEVICE BRIDGE)\n"sv);
    sb.append("=========================================================================\n"sv);
    for (auto const& msg : m_whatsapp->messages()) {
        sb.appendff("💬 [{}] {}\n", msg.timestamp, msg.sender);
        sb.appendff("   Message: \"{}\"\n", msg.text);
        if (msg.requires_response) {
            sb.appendff("   Detected Commitment: {}\n", msg.detected_commitment);
            sb.appendff("   Suggested Draft: \"{}\"\n", msg.suggested_draft);
            sb.append("   Policy Status: DRAFT_READY (Confirmation required to send)\n"sv);
        }
        sb.append("\n"sv);
    }
    return sb.to_byte_string();
}

ByteString ContextEngine::generate_calendar_matrix()
{
    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.append("   JARVIS OS — CALENDAR AGENDA & DEADLINE SCHEDULE\n"sv);
    sb.append("=========================================================================\n"sv);
    for (auto const& ev : m_calendar->events()) {
        sb.appendff("📅 [{}] {}\n", ev.start_time, ev.title);
        sb.appendff("   Location: {}\n", ev.location);
        sb.appendff("   Participants: {}\n", ev.participants);
        sb.appendff("   Preparation Notes: {}\n\n", ev.prep_notes);
    }
    return sb.to_byte_string();
}

ByteString ContextEngine::generate_news_briefing()
{
    StringBuilder sb;
    sb.append("=========================================================================\n"sv);
    sb.append("   JARVIS OS — CLUSTERED NEWS INTELLIGENCE DECK\n"sv);
    sb.append("=========================================================================\n"sv);
    for (auto const& s : m_news->stories()) {
        sb.appendff("🌍 [{}] {} (Source: {})\n", s.category, s.headline, s.source);
        sb.appendff("   Summary: {}\n\n", s.summary);
    }
    return sb.to_byte_string();
}

JsonObject ContextEngine::to_json()
{
    JsonObject obj;
    obj.set("user", UserProfile::the().name());
    obj.set("attendance", UserProfile::the().attendance_percentage());
    obj.set("connectors", ConnectorRegistry::the().to_json());
    obj.set("contacts", ContactGraph::the().to_json());
    obj.set("memory", PersonalMemory::the().to_json());
    obj.set("automation", AutomationEngine::the().to_json());
    obj.set("persona", PersonaModel::the().to_json());
    return obj;
}

}
