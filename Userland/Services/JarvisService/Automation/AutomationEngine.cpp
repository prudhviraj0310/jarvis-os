/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "AutomationEngine.h"

namespace JarvisService {

ByteString ProposedAction::type_string() const
{
    switch (type) {
    case ActionType::DraftReply:
        return "DRAFT_REPLY";
    case ActionType::SendReply:
        return "SEND_REPLY";
    case ActionType::DraftEmail:
        return "DRAFT_EMAIL";
    case ActionType::SendEmail:
        return "SEND_EMAIL";
    case ActionType::CreateCalendarEvent:
        return "CREATE_CALENDAR_EVENT";
    case ActionType::NotifyUser:
    default:
        return "NOTIFY_USER";
    }
}

JsonObject ProposedAction::to_json() const
{
    JsonObject obj;
    obj.set("id", id);
    obj.set("type", type_string());
    obj.set("title", title);
    obj.set("description", description);
    obj.set("target_recipient", target_recipient);
    obj.set("payload", payload);
    obj.set("requires_confirmation", requires_confirmation);
    obj.set("is_executed", is_executed);
    return obj;
}

AutomationEngine& AutomationEngine::the()
{
    static AutomationEngine instance;
    return instance;
}

AutomationEngine::AutomationEngine()
{
    trigger_system_boot();
}

void AutomationEngine::trigger_system_boot()
{
    m_pending_actions.clear();

    // 1. WhatsApp recommended reply
    m_pending_actions.append({
        .id = "ACT-WA-001",
        .type = ActionType::SendReply,
        .title = "Reply to Rahul Sharma regarding Capstone Project",
        .description = "Rahul asked: 'Bro can you send me the project tomorrow?'",
        .target_recipient = "Rahul Sharma",
        .payload = "Yes, I'll send it tomorrow.",
        .requires_confirmation = true,
        .is_executed = false
    });

    // 2. Email recommended draft
    m_pending_actions.append({
        .id = "ACT-EM-001",
        .type = ActionType::SendEmail,
        .title = "Acknowledge Capstone Submission to Prof. Krishnamurthy",
        .description = "Deliverables submission deadline is tomorrow at 5:00 PM.",
        .target_recipient = "Prof. Krishnamurthy <faculty@cs.edu>",
        .payload = "Dear Prof. Krishnamurthy,\n\nI have updated the architectural documentation and submitted the latest kernel verification logs.\n\nBest regards,\nPrudhvi Raj",
        .requires_confirmation = true,
        .is_executed = false
    });

    // 3. Calendar Preparation
    m_pending_actions.append({
        .id = "ACT-CAL-001",
        .type = ActionType::NotifyUser,
        .title = "Prepare for Capstone Review & Demo at 10:30 AM",
        .description = "Demonstrate live QEMU capability execution and JournalService ledger.",
        .target_recipient = "Prudhvi Raj",
        .payload = "Review slides and ensure QEMU test pass.",
        .requires_confirmation = false,
        .is_executed = false
    });
}

void AutomationEngine::trigger_email_received(ByteString const& sender, ByteString const& subject)
{
    (void)sender;
    (void)subject;
}

void AutomationEngine::trigger_whatsapp_received(ByteString const& sender, ByteString const& text)
{
    (void)sender;
    (void)text;
}

Optional<ProposedAction> AutomationEngine::get_action(ByteString const& id) const
{
    for (auto const& a : m_pending_actions) {
        if (a.id == id)
            return a;
    }
    return {};
}

bool AutomationEngine::mark_action_executed(ByteString const& id)
{
    for (auto& a : m_pending_actions) {
        if (a.id == id) {
            a.is_executed = true;
            return true;
        }
    }
    return false;
}

JsonArray AutomationEngine::to_json() const
{
    JsonArray arr;
    for (auto const& a : m_pending_actions)
        arr.must_append(a.to_json());
    return arr;
}

}
