/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include <LibJarvis/ConnectionToServer.h>

namespace Jarvis {

ConnectionToServer::ConnectionToServer(NonnullOwnPtr<Core::LocalSocket> socket)
    : IPC::ConnectionToServer<JarvisClientEndpoint, JarvisServerEndpoint>(*this, move(socket))
{
}

void ConnectionToServer::die()
{
}

void ConnectionToServer::world_state_changed(String const&, String const&)
{
}

ErrorOr<String> ConnectionToServer::request_capability_sync(String const& name, String const& args, String const& req_id)
{
    auto result = send_sync_but_allow_failure<Messages::JarvisServer::RequestCapability>(name, args, req_id);
    if (!result)
        return Error::from_string_literal("IPC communication failure with JarvisService");
    return result->take_response_json();
}

ErrorOr<String> ConnectionToServer::get_system_health_sync()
{
    auto result = send_sync_but_allow_failure<Messages::JarvisServer::GetSystemHealth>();
    if (!result)
        return Error::from_string_literal("IPC communication failure with JarvisService");
    return result->take_health_json();
}

ErrorOr<String> ConnectionToServer::query_policy_sync(String const& name)
{
    auto result = send_sync_but_allow_failure<Messages::JarvisServer::QueryPolicy>(name);
    if (!result)
        return Error::from_string_literal("IPC communication failure with JarvisService");
    return String::formatted("Capability: {}, Allowed: {}, Tier: {}", name, result->is_allowed(), result->policy_level());
}

}
