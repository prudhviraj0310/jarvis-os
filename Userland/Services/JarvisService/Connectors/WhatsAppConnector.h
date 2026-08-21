/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/Vector.h>
#include <AK/JsonArray.h>

namespace JarvisService {

struct WhatsAppMessage {
    ByteString sender;
    ByteString text;
    ByteString timestamp;
    bool is_unread { true };
    bool requires_response { false };
    ByteString detected_commitment;
    ByteString suggested_draft;

    JsonObject to_json() const;
};

class WhatsAppConnector final : public PersonalConnector {
public:
    static NonnullRefPtr<WhatsAppConnector> create();

    virtual ~WhatsAppConnector() override = default;

    virtual ByteString name() const override { return "WhatsApp"; }
    virtual ByteString provider_type() const override { return "MultiDeviceBridge"; }
    virtual ConnectorStatus status() const override { return m_status; }
    virtual bool is_authenticated() const override { return m_authenticated; }
    virtual ByteString last_sync_time() const override { return m_last_sync; }

    virtual void sync() override;
    virtual void revoke() override;
    virtual JsonObject to_json() const override;

    Vector<WhatsAppMessage> const& messages() const { return m_messages; }
    Vector<WhatsAppMessage> unread_requiring_attention() const;

    ByteString draft_reply(ByteString const& sender, ByteString const& message_context);
    bool send_message(ByteString const& recipient, ByteString const& text);

private:
    WhatsAppConnector();

    ConnectorStatus m_status { ConnectorStatus::Connected };
    bool m_authenticated { true };
    ByteString m_last_sync { "Just now" };
    Vector<WhatsAppMessage> m_messages;
};

}
