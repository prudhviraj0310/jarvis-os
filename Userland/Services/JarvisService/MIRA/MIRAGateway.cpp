/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "MIRAGateway.h"
#include <LibCore/DateTime.h>

namespace JarvisService {

ByteString MIRAChannelEvent::channel_name() const
{
    switch (channel) {
    case MIRAChannelType::WhatsApp:
        return "WhatsApp";
    case MIRAChannelType::Email:
        return "Email";
    case MIRAChannelType::Telegram:
        return "Telegram";
    case MIRAChannelType::Signal:
        return "Signal";
    case MIRAChannelType::Discord:
        return "Discord";
    case MIRAChannelType::Slack:
        return "Slack";
    case MIRAChannelType::Matrix:
        return "Matrix";
    case MIRAChannelType::WebPush:
    default:
        return "WebPush";
    }
}

JsonObject MIRAChannelEvent::to_json() const
{
    JsonObject obj;
    obj.set("channel", channel_name());
    obj.set("sender_id", sender_id);
    obj.set("sender_name", sender_name);
    obj.set("content", content);
    obj.set("timestamp", timestamp);
    obj.set("is_actionable", is_actionable);
    obj.set("inferred_intent", inferred_intent);
    return obj;
}

MIRAGateway& MIRAGateway::the()
{
    static MIRAGateway instance;
    return instance;
}

MIRAGateway::MIRAGateway()
{
    poll_all_channels();
}

void MIRAGateway::poll_all_channels()
{
    m_events.clear();

    m_events.append({
        .channel = MIRAChannelType::WhatsApp,
        .sender_id = "+91-9848012345",
        .sender_name = "Rahul Sharma",
        .content = "Bro can you send me the project tomorrow?",
        .timestamp = "07:45 AM",
        .is_actionable = true,
        .inferred_intent = "REQUEST_FILES"
    });

    m_events.append({
        .channel = MIRAChannelType::Email,
        .sender_id = "faculty@cs.edu",
        .sender_name = "Prof. Krishnamurthy",
        .content = "Please submit your completed operating system architecture documentation before tomorrow 5 PM.",
        .timestamp = "06:30 AM",
        .is_actionable = true,
        .inferred_intent = "SUBMISSION_DEADLINE"
    });

    m_events.append({
        .channel = MIRAChannelType::Telegram,
        .sender_id = "@kernel_devs",
        .sender_name = "OS Research Group",
        .content = "New benchmark results for x86_64 SMP spinlock elision released.",
        .timestamp = "Yesterday",
        .is_actionable = false,
        .inferred_intent = "INFORMATIONAL"
    });

    m_events.append({
        .channel = MIRAChannelType::Discord,
        .sender_id = "#ai-agents",
        .sender_name = "Agentic Systems Forum",
        .content = "MIRA multi-channel agent framework integrated with native microkernel architecture.",
        .timestamp = "Today",
        .is_actionable = false,
        .inferred_intent = "INFORMATIONAL"
    });
}

Vector<MIRAChannelEvent> MIRAGateway::actionable_events() const
{
    Vector<MIRAChannelEvent> list;
    for (auto const& ev : m_events) {
        if (ev.is_actionable)
            list.append(ev);
    }
    return list;
}

JsonObject MIRAGateway::to_json() const
{
    JsonObject obj;
    obj.set("status", "ACTIVE");
    obj.set("channels_monitored", 8);

    JsonArray arr;
    for (auto const& ev : m_events)
        arr.must_append(ev.to_json());
    obj.set("events", arr);
    return obj;
}

}
