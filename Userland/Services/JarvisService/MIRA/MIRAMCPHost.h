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

struct MCPToolDefinition {
    ByteString name;
    ByteString description;
    ByteString input_schema;
    bool is_sandboxed { true };

    JsonObject to_json() const;
};

class MIRAMCPHost {
public:
    static MIRAMCPHost& the();

    MIRAMCPHost();

    Vector<MCPToolDefinition> const& registered_tools() const { return m_tools; }
    JsonObject to_json() const;

private:
    Vector<MCPToolDefinition> m_tools;
};

}
