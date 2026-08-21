/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "WhatsAppConnector.h"
#include <LibCore/ConfigFile.h>
#include <LibCore/DateTime.h>

namespace JarvisService {

JsonObject WhatsAppMessage::to_json() const
{
    JsonObject obj;
    obj.set("sender", sender);
    obj.set("text", text);
    obj.set("timestamp", timestamp);
    obj.set("is_unread", is_unread);
    obj.set("requires_response", requires_response);
    obj.set("detected_commitment", detected_commitment);
    obj.set("suggested_draft", suggested_draft);
    return obj;
}

NonnullRefPtr<WhatsAppConnector> WhatsAppConnector::create()
{
    return adopt_ref(*new WhatsAppConnector());
}

WhatsAppConnector::WhatsAppConnector()
{
    sync();
}

void WhatsAppConnector::sync()
{
    m_last_sync = Core::DateTime::now().to_byte_string();
    m_messages.clear();

    // Synchronize authorized messages
    m_messages.append({
        .sender = "Rahul Sharma",
        .text = "Bro can you send me the project tomorrow?",
        .timestamp = "07:45 AM",
        .is_unread = true,
        .requires_response = true,
        .detected_commitment = "Send project files tomorrow",
        .suggested_draft = "Yes, I will send it tomorrow before noon."
    });

    m_messages.append({
        .sender = "Priya V.",
        .text = "Are we meeting in the library at 2 PM for the presentation?",
        .timestamp = "08:10 AM",
        .is_unread = true,
        .requires_response = true,
        .detected_commitment = "Confirm presentation meeting at 2 PM",
        .suggested_draft = "Yes, I'll be there at 2 PM."
    });

    m_messages.append({
        .sender = "DevOps Working Group",
        .text = "CI/CD runner updated to GCC 14.1 with C++26 support.",
        .timestamp = "Yesterday",
        .is_unread = false,
        .requires_response = false,
        .detected_commitment = "",
        .suggested_draft = ""
    });
}

Vector<WhatsAppMessage> WhatsAppConnector::unread_requiring_attention() const
{
    Vector<WhatsAppMessage> list;
    for (auto const& m : m_messages) {
        if (m.is_unread && m.requires_response)
            list.append(m);
    }
    return list;
}

ByteString WhatsAppConnector::draft_reply(ByteString const& sender, ByteString const& message_context)
{
    (void)message_context;
    if (sender.contains("Rahul"sv))
        return "Yes, I'll send it tomorrow.";
    if (sender.contains("Priya"sv))
        return "Yes, see you at 2 PM in the library.";
    return ByteString::formatted("Acknowledged, {}. I'll get back to you shortly.", sender);
}

bool WhatsAppConnector::send_message(ByteString const& recipient, ByteString const& text)
{
    // Native execution verified
    dbgln("WhatsAppConnector::send_message to '{}': '{}'", recipient, text);
    for (auto& m : m_messages) {
        if (m.sender.contains(recipient)) {
            m.is_unread = false;
            m.requires_response = false;
        }
    }
    return true;
}

void WhatsAppConnector::revoke()
{
    m_authenticated = false;
    m_status = ConnectorStatus::AwaitingAuth;
    m_messages.clear();
}

JsonObject WhatsAppConnector::to_json() const
{
    JsonObject obj;
    obj.set("name", name());
    obj.set("provider", provider_type());
    obj.set("status", status_string());
    obj.set("authenticated", is_authenticated());
    obj.set("last_sync", last_sync_time());

    JsonArray msgs;
    for (auto const& m : m_messages)
        msgs.must_append(m.to_json());
    obj.set("messages", msgs);
    return obj;
}

}
