/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/Vector.h>
#include <AK/JsonObject.h>
#include <AK/JsonArray.h>

namespace JarvisService {

enum class ActionType {
    DraftReply,
    SendReply,
    DraftEmail,
    SendEmail,
    CreateCalendarEvent,
    NotifyUser
};

struct ProposedAction {
    ByteString id;
    ActionType type;
    ByteString title;
    ByteString description;
    ByteString target_recipient;
    ByteString payload;
    bool requires_confirmation { true };
    bool is_executed { false };

    ByteString type_string() const;
    JsonObject to_json() const;
};

class AutomationEngine {
public:
    static AutomationEngine& the();

    AutomationEngine();

    void trigger_system_boot();
    void trigger_email_received(ByteString const& sender, ByteString const& subject);
    void trigger_whatsapp_received(ByteString const& sender, ByteString const& text);

    Vector<ProposedAction> const& pending_actions() const { return m_pending_actions; }
    Optional<ProposedAction> get_action(ByteString const& id) const;
    bool mark_action_executed(ByteString const& id);

    JsonArray to_json() const;

private:
    Vector<ProposedAction> m_pending_actions;
};

}
