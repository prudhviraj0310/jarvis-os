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

enum class MIRAChannelType {
    WhatsApp,
    Email,
    Telegram,
    Signal,
    Discord,
    Slack,
    Matrix,
    WebPush
};

struct MIRAChannelEvent {
    MIRAChannelType channel;
    ByteString sender_id;
    ByteString sender_name;
    ByteString content;
    ByteString timestamp;
    bool is_actionable { false };
    ByteString inferred_intent;

    ByteString channel_name() const;
    JsonObject to_json() const;
};

class MIRAGateway {
public:
    static MIRAGateway& the();

    MIRAGateway();

    void poll_all_channels();
    Vector<MIRAChannelEvent> const& active_events() const { return m_events; }
    Vector<MIRAChannelEvent> actionable_events() const;

    JsonObject to_json() const;

private:
    Vector<MIRAChannelEvent> m_events;
};

}
