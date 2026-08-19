/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ConnectionFromClient.h"
#include "CapabilityDispatcher.h"
#include "PolicyGate.h"

namespace JarvisService {

ConnectionFromClient::ConnectionFromClient(NonnullOwnPtr<Core::LocalSocket> socket, int client_id)
    : IPC::ConnectionFromClient<JarvisClientEndpoint, JarvisServerEndpoint>(*this, move(socket), client_id)
{
}

void ConnectionFromClient::die()
{
}

Messages::JarvisServer::RequestCapabilityResponse ConnectionFromClient::request_capability(String const& name, String const& args, String const& req_id)
{
    auto tier = PolicyGate::the().evaluate_capability(name.bytes_as_string_view());
    bool accepted = (tier != PolicyTier::Denied);
    auto response = CapabilityDispatcher::the().dispatch(name, args, req_id);
    return { accepted, response };
}

Messages::JarvisServer::GetSystemHealthResponse ConnectionFromClient::get_system_health()
{
    return { CapabilityDispatcher::the().get_system_health() };
}

Messages::JarvisServer::QueryPolicyResponse ConnectionFromClient::query_policy(String const& name)
{
    auto tier = PolicyGate::the().evaluate_capability(name.bytes_as_string_view());
    bool allowed = (tier != PolicyTier::Denied);
    auto tier_str = PolicyGate::the().policy_tier_to_string(tier);
    return { allowed, tier_str };
}

}
