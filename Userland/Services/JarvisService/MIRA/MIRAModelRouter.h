/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/JsonObject.h>

namespace JarvisService {

enum class ModelRouteTier {
    FastEdge,
    DeepReasoning,
    LocalOffline
};

struct RoutingDecision {
    ModelRouteTier tier;
    ByteString model_name;
    int estimated_latency_ms;
    double reasoning_confidence;
    ByteString justification;

    JsonObject to_json() const;
};

class MIRAModelRouter {
public:
    static MIRAModelRouter& the();

    MIRAModelRouter();

    RoutingDecision route_intent(ByteString const& prompt);
    JsonObject to_json() const;

private:
    bool m_online_providers_available { true };
};

}
