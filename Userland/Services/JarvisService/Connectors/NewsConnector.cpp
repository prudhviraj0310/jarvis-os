/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "NewsConnector.h"
#include <LibCore/DateTime.h>

namespace JarvisService {

JsonObject NewsStory::to_json() const
{
    JsonObject obj;
    obj.set("category", category);
    obj.set("headline", headline);
    obj.set("summary", summary);
    obj.set("source", source);
    obj.set("importance", importance);
    return obj;
}

NonnullRefPtr<NewsConnector> NewsConnector::create()
{
    return adopt_ref(*new NewsConnector());
}

NewsConnector::NewsConnector()
{
    sync();
}

void NewsConnector::sync()
{
    m_last_sync = Core::DateTime::now().to_byte_string();
    m_stories.clear();

    m_stories.append({
        .category = "AI",
        .headline = "Autonomous Agentic Operating Systems Pioneer Real-Time Machine Verification",
        .summary = "New kernel architectures decouple reasoning models from machine authority using cryptographic ledgers.",
        .source = "HackerNews / arXiv",
        .importance = 10
    });

    m_stories.append({
        .category = "Technology",
        .headline = "C++26 Standardization Finalizes Reflection and Hardware Acceleration Contracts",
        .summary = "ISO C++ Committee introduces core memory safety profiles and zero-overhead reflection pipelines.",
        .source = "ISO C++ Bulletin",
        .importance = 9
    });

    m_stories.append({
        .category = "India",
        .headline = "National Quantum Mission Advances Indigenous QPU Fabrication & Cryptography Hubs",
        .summary = "Premier academic institutions commission 64-qubit quantum testbeds and post-quantum encryption protocols.",
        .source = "PIB India / TechWire",
        .importance = 8
    });

    m_stories.append({
        .category = "Global",
        .headline = "Global Semiconductor Foundries Accelerate 1.8nm GAA Transistor Deployment",
        .summary = "Next-generation process nodes achieve 30% higher energy efficiency for edge AI compute clusters.",
        .source = "Reuters Technology",
        .importance = 8
    });

    m_stories.append({
        .category = "Finance",
        .headline = "Tech Indices Rally as Enterprise Autonomous AI Adoption Surpasses Projections",
        .summary = "Cloud infrastructure spending rises 24% year-over-year driven by sovereign enterprise deployments.",
        .source = "Financial Times",
        .importance = 7
    });
}

Vector<NewsStory> NewsConnector::stories_by_category(ByteString const& category) const
{
    Vector<NewsStory> list;
    auto lower = category.to_lowercase();
    for (auto const& s : m_stories) {
        if (s.category.to_lowercase() == lower)
            list.append(s);
    }
    return list;
}

void NewsConnector::revoke()
{
    m_stories.clear();
}

JsonObject NewsConnector::to_json() const
{
    JsonObject obj;
    obj.set("name", name());
    obj.set("provider", provider_type());
    obj.set("status", status_string());
    obj.set("authenticated", is_authenticated());
    obj.set("last_sync", last_sync_time());

    JsonArray arr;
    for (auto const& s : m_stories)
        arr.must_append(s.to_json());
    obj.set("stories", arr);
    return obj;
}

}
