/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "EmailConnector.h"
#include <AK/StringBuilder.h>
#include <LibCore/ConfigFile.h>
#include <LibCore/DateTime.h>

namespace JarvisService {

ByteString EmailMessage::priority_string() const
{
    switch (priority) {
    case EmailPriority::Important:
        return "IMPORTANT";
    case EmailPriority::LowPriority:
        return "LOW_PRIORITY";
    case EmailPriority::Spam:
    default:
        return "SPAM";
    }
}

JsonObject EmailMessage::to_json() const
{
    JsonObject obj;
    obj.set("sender", sender);
    obj.set("subject", subject);
    obj.set("snippet", snippet);
    obj.set("timestamp", timestamp);
    obj.set("priority", priority_string());
    obj.set("is_unread", is_unread);
    obj.set("requires_response", requires_response);
    obj.set("deadline", deadline);
    obj.set("summary", summary);
    return obj;
}

NonnullRefPtr<EmailConnector> EmailConnector::create()
{
    return adopt_ref(*new EmailConnector());
}

EmailConnector::EmailConnector()
{
    sync();
}

void EmailConnector::sync()
{
    m_last_sync = Core::DateTime::now().to_byte_string();
    m_emails.clear();

    // 1. Important emails
    m_emails.append({
        .sender = "Prof. Krishnamurthy <faculty@cs.edu>",
        .subject = "Final Capstone Deliverables & Evaluation Schedule",
        .snippet = "Please submit your completed operating system architecture documentation before tomorrow 5 PM.",
        .timestamp = "06:30 AM",
        .priority = EmailPriority::Important,
        .is_unread = true,
        .requires_response = true,
        .deadline = "Tomorrow, 5:00 PM",
        .summary = "Capstone documentation submission deadline tomorrow 5 PM."
    });

    m_emails.append({
        .sender = "Academic Dean <academic@cs.edu>",
        .subject = "Mid-Term Attendance Summary & Hall Ticket Clearance",
        .snippet = "Your current overall attendance is verified at 87.5%. Examination eligibility is confirmed.",
        .timestamp = "Yesterday",
        .priority = EmailPriority::Important,
        .is_unread = true,
        .requires_response = false,
        .deadline = "",
        .summary = "Attendance verified at 87.5%. Exam eligibility confirmed."
    });

    m_emails.append({
        .sender = "GitHub Security <notifications@github.com>",
        .subject = "[Security] Push protection active for prudhviraj0310/jarvis-os",
        .snippet = "All secret scanning checks passed successfully for repository prudhviraj0310/jarvis-os.",
        .timestamp = "Yesterday",
        .priority = EmailPriority::Important,
        .is_unread = false,
        .requires_response = false,
        .deadline = "",
        .summary = "GitHub security verification passed."
    });

    // 2. Low priority emails
    m_emails.append({
        .sender = "ACM TechNews <technews@acm.org>",
        .subject = "Weekly Briefing: Advances in Microkernel Verification and LLM Architectures",
        .snippet = "Explore the latest breakthroughs in verified operating systems and high-throughput compilers.",
        .timestamp = "Yesterday",
        .priority = EmailPriority::LowPriority,
        .is_unread = true,
        .requires_response = false,
        .deadline = "",
        .summary = "Weekly research bulletin."
    });
}

Vector<EmailMessage> EmailConnector::important_unread() const
{
    Vector<EmailMessage> list;
    for (auto const& e : m_emails) {
        if (e.is_unread && e.priority == EmailPriority::Important)
            list.append(e);
    }
    return list;
}

ByteString EmailConnector::draft_email(ByteString const& to, ByteString const& subject, ByteString const& context)
{
    (void)subject;
    (void)context;
    StringBuilder sb;
    sb.appendff("Dear {},\n\n", to.contains("Krishnamurthy"sv) ? "Prof. Krishnamurthy" : to);
    sb.append("I have updated the architectural documentation and submitted the latest kernel and capability ledger verification logs as requested.\n\n"sv);
    sb.append("Best regards,\nPrudhvi Raj"sv);
    return sb.to_byte_string();
}

bool EmailConnector::send_email(ByteString const& to, ByteString const& subject, ByteString const& body)
{
    dbgln("EmailConnector::send_email to='{}', subject='{}', body_len={}", to, subject, body.length());
    for (auto& e : m_emails) {
        if (e.sender.contains(to)) {
            e.is_unread = false;
            e.requires_response = false;
        }
    }
    return true;
}

void EmailConnector::revoke()
{
    m_authenticated = false;
    m_status = ConnectorStatus::AwaitingAuth;
    m_emails.clear();
}

JsonObject EmailConnector::to_json() const
{
    JsonObject obj;
    obj.set("name", name());
    obj.set("provider", provider_type());
    obj.set("status", status_string());
    obj.set("authenticated", is_authenticated());
    obj.set("last_sync", last_sync_time());

    JsonArray ems;
    for (auto const& e : m_emails)
        ems.must_append(e.to_json());
    obj.set("emails", ems);
    return obj;
}

}
