/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "MIRAModelRouter.h"

namespace JarvisService {

JsonObject RoutingDecision::to_json() const
{
    JsonObject obj;
    obj.set("tier", tier == ModelRouteTier::FastEdge ? "FAST_EDGE" : (tier == ModelRouteTier::DeepReasoning ? "DEEP_REASONING" : "LOCAL_OFFLINE"));
    obj.set("model_name", model_name);
    obj.set("latency_ms", estimated_latency_ms);
    obj.set("confidence", reasoning_confidence);
    obj.set("justification", justification);
    return obj;
}

MIRAModelRouter& MIRAModelRouter::the()
{
    static MIRAModelRouter instance;
    return instance;
}

MIRAModelRouter::MIRAModelRouter()
{
}

RoutingDecision MIRAModelRouter::route_intent(ByteString const& prompt)
{
    auto lower = prompt.to_lowercase();

    if (lower.contains("plan"sv) || lower.contains("analyze"sv) || lower.contains("handle it"sv) || lower.contains("briefing"sv)) {
        return {
            .tier = ModelRouteTier::DeepReasoning,
            .model_name = "MIRA-DeepReasoner-v2",
            .estimated_latency_ms = 45,
            .reasoning_confidence = 0.96,
            .justification = "Complex multi-channel intent synthesis & dependency resolution"
        };
    }

    return {
        .tier = ModelRouteTier::FastEdge,
        .model_name = "MIRA-FastEdge-v1",
        .estimated_latency_ms = 8,
        .reasoning_confidence = 0.99,
        .justification = "Standard cognitive status and single-step query"
    };
}

JsonObject MIRAModelRouter::to_json() const
{
    JsonObject obj;
    obj.set("status", "ONLINE");
    obj.set("active_engine", "MIRA Dual-Tier AutoRouter");
    obj.set("fast_tier_latency", "<10ms");
    obj.set("deep_tier_latency", "<50ms");
    obj.set("offline_fallback", "READY");
    return obj;
}

}
