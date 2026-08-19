/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/String.h>
#include <LibIPC/ConnectionToServer.h>
#include <Userland/Services/JarvisService/JarvisClientEndpoint.h>
#include <Userland/Services/JarvisService/JarvisServerEndpoint.h>

namespace Jarvis {

class ConnectionToServer final
    : public IPC::ConnectionToServer<JarvisClientEndpoint, JarvisServerEndpoint>
    , public JarvisClientEndpoint {
    IPC_CLIENT_CONNECTION(ConnectionToServer, "/tmp/portal/jarvis"sv)
public:
    virtual ~ConnectionToServer() override = default;

    ErrorOr<String> request_capability_sync(String const& name, String const& args, String const& req_id);
    ErrorOr<String> get_system_health_sync();
    ErrorOr<String> query_policy_sync(String const& name);

    virtual void die() override;

private:
    ConnectionToServer(NonnullOwnPtr<Core::LocalSocket>);

    virtual void world_state_changed(String const& event_type, String const& state_json) override;
};

}
