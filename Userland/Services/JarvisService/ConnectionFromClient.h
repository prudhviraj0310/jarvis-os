/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <LibIPC/ConnectionFromClient.h>
#include <JarvisService/JarvisClientEndpoint.h>
#include <JarvisService/JarvisServerEndpoint.h>

namespace JarvisService {

class ConnectionFromClient final : public IPC::ConnectionFromClient<JarvisClientEndpoint, JarvisServerEndpoint> {
    C_OBJECT(ConnectionFromClient)
public:
    ~ConnectionFromClient() override = default;

    virtual void die() override;

private:
    explicit ConnectionFromClient(NonnullOwnPtr<Core::LocalSocket>, int client_id);

    virtual Messages::JarvisServer::RequestCapabilityResponse request_capability(String const&, String const&, String const&) override;
    virtual Messages::JarvisServer::GetSystemHealthResponse get_system_health() override;
    virtual Messages::JarvisServer::QueryPolicyResponse query_policy(String const&) override;
};

}
