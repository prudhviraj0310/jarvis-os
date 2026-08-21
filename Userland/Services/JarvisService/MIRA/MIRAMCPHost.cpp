/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "MIRAMCPHost.h"

namespace JarvisService {

JsonObject MCPToolDefinition::to_json() const
{
    JsonObject obj;
    obj.set("name", name);
    obj.set("description", description);
    obj.set("input_schema", input_schema);
    obj.set("is_sandboxed", is_sandboxed);
    return obj;
}

MIRAMCPHost& MIRAMCPHost::the()
{
    static MIRAMCPHost instance;
    return instance;
}

MIRAMCPHost::MIRAMCPHost()
{
    m_tools.append({
        .name = "mcp_jarvis_journal_audit",
        .description = "Query cryptographic SHA-256 block ledger for capability proofs",
        .input_schema = "{\"type\":\"object\",\"properties\":{\"filter\":{\"type\":\"string\"}}}",
        .is_sandboxed = true
    });

    m_tools.append({
        .name = "mcp_mira_channel_dispatch",
        .description = "Dispatch verified message payload across registered MIRA channels",
        .input_schema = "{\"type\":\"object\",\"properties\":{\"channel\":{\"type\":\"string\"},\"payload\":{\"type\":\"string\"}}}",
        .is_sandboxed = true
    });

    m_tools.append({
        .name = "mcp_mira_wiki_query",
        .description = "Semantic lookup in local MIRA Knowledge Base and Wiki",
        .input_schema = "{\"type\":\"object\",\"properties\":{\"topic\":{\"type\":\"string\"}}}",
        .is_sandboxed = true
    });
}

JsonObject MIRAMCPHost::to_json() const
{
    JsonObject obj;
    obj.set("status", "LISTENING");
    obj.set("protocol_version", "MCP 2024-11-05");
    obj.set("tool_count", static_cast<int>(m_tools.size()));

    JsonArray arr;
    for (auto const& t : m_tools)
        arr.must_append(t.to_json());
    obj.set("tools", arr);
    return obj;
}

}
