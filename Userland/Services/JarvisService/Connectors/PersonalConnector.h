/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/JsonObject.h>
#include <AK/RefCounted.h>
#include <AK/RefPtr.h>

namespace JarvisService {

enum class ConnectorStatus {
    Connected,
    AwaitingAuth,
    Offline,
    RateLimited,
    Error
};

class PersonalConnector : public RefCounted<PersonalConnector> {
public:
    virtual ~PersonalConnector() = default;

    virtual ByteString name() const = 0;
    virtual ByteString provider_type() const = 0;
    virtual ConnectorStatus status() const = 0;
    virtual bool is_authenticated() const = 0;
    virtual ByteString last_sync_time() const = 0;

    virtual void sync() = 0;
    virtual void revoke() = 0;
    virtual JsonObject to_json() const = 0;

    ByteString status_string() const
    {
        switch (status()) {
        case ConnectorStatus::Connected:
            return "CONNECTED";
        case ConnectorStatus::AwaitingAuth:
            return "AWAITING_AUTH";
        case ConnectorStatus::Offline:
            return "OFFLINE";
        case ConnectorStatus::RateLimited:
            return "RATE_LIMITED";
        case ConnectorStatus::Error:
        default:
            return "ERROR";
        }
    }
};

}
