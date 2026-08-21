/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/Vector.h>
#include <AK/JsonArray.h>

namespace JarvisService {

enum class EmailPriority {
    Important,
    LowPriority,
    Spam
};

struct EmailMessage {
    ByteString sender;
    ByteString subject;
    ByteString snippet;
    ByteString timestamp;
    EmailPriority priority { EmailPriority::Important };
    bool is_unread { true };
    bool requires_response { false };
    ByteString deadline;
    ByteString summary;

    ByteString priority_string() const;
    JsonObject to_json() const;
};

class EmailConnector final : public PersonalConnector {
public:
    static NonnullRefPtr<EmailConnector> create();

    virtual ~EmailConnector() override = default;

    virtual ByteString name() const override { return "Email"; }
    virtual ByteString provider_type() const override { return "IMAP_Gmail"; }
    virtual ConnectorStatus status() const override { return m_status; }
    virtual bool is_authenticated() const override { return m_authenticated; }
    virtual ByteString last_sync_time() const override { return m_last_sync; }

    virtual void sync() override;
    virtual void revoke() override;
    virtual JsonObject to_json() const override;

    Vector<EmailMessage> const& emails() const { return m_emails; }
    Vector<EmailMessage> important_unread() const;

    ByteString draft_email(ByteString const& to, ByteString const& subject, ByteString const& context);
    bool send_email(ByteString const& to, ByteString const& subject, ByteString const& body);

private:
    EmailConnector();

    ConnectorStatus m_status { ConnectorStatus::Connected };
    bool m_authenticated { true };
    ByteString m_last_sync { "Just now" };
    Vector<EmailMessage> m_emails;
};

}
