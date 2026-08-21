/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "MIRAGateway.h"
#include "MIRAMemoryWiki.h"
#include "MIRAModelRouter.h"
#include "MIRAProactiveCompanion.h"
#include "MIRAMCPHost.h"
#include <AK/ByteString.h>
#include <AK/JsonObject.h>

namespace JarvisService {

class MIRAEngine {
public:
    static MIRAEngine& the();

    MIRAEngine();

    ByteString generate_mira_dashboard();
    JsonObject to_json();
};

}
