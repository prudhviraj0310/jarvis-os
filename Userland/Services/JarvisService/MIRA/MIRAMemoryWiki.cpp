/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "MIRAMemoryWiki.h"

namespace JarvisService {

JsonObject WikiArticle::to_json() const
{
    JsonObject obj;
    obj.set("title", title);
    obj.set("category", category);
    obj.set("content", content);
    obj.set("last_updated", last_updated);

    JsonArray links;
    for (auto const& e : linked_entities)
        links.must_append(e);
    obj.set("linked_entities", links);
    return obj;
}

MIRAMemoryWiki& MIRAMemoryWiki::the()
{
    static MIRAMemoryWiki instance;
    return instance;
}

MIRAMemoryWiki::MIRAMemoryWiki()
{
    m_articles.append({
        .title = "Capstone Project: JARVIS OS",
        .category = "Projects",
        .content = "Sovereign 64-bit operating system with native C++ kernel, preemptive multitasking, CapabilityRegistry, and SHA-256 cryptographic JournalService.",
        .last_updated = "Today",
        .linked_entities = { "Prof. Krishnamurthy", "Rahul Sharma", "JournalService" }
    });

    m_articles.append({
        .title = "Academic Standing & Attendance",
        .category = "Education",
        .content = "Enrolled in Computer Science & Engineering. Current overall attendance is verified at 87.5% with all midterm clearances confirmed.",
        .last_updated = "Yesterday",
        .linked_entities = { "Academic Dean", "Database Course", "Distributed Systems" }
    });

    m_articles.append({
        .title = "Machine Sovereignty Invariant",
        .category = "Security Architecture",
        .content = "The core principle dictating that Model Output does not equal Machine Evidence. Consequential actions require explicit native capability verification and journal audit.",
        .last_updated = "Active",
        .linked_entities = { "PolicyGate", "JournalService", "CapabilityDispatcher" }
    });
}

Optional<WikiArticle> MIRAMemoryWiki::find_article(ByteString const& title) const
{
    auto lower = title.to_lowercase();
    for (auto const& art : m_articles) {
        if (art.title.to_lowercase().contains(lower))
            return art;
    }
    return {};
}

void MIRAMemoryWiki::record_reflection(ByteString const& topic, ByteString const& reflection)
{
    m_articles.append({
        .title = ByteString::formatted("Reflection: {}", topic),
        .category = "Self-Reflection",
        .content = reflection,
        .last_updated = "Just now",
        .linked_entities = {}
    });
}

JsonObject MIRAMemoryWiki::to_json() const
{
    JsonObject obj;
    obj.set("status", "INDEXED");
    obj.set("article_count", static_cast<int>(m_articles.size()));

    JsonArray arr;
    for (auto const& art : m_articles)
        arr.must_append(art.to_json());
    obj.set("wiki_articles", arr);
    return obj;
}

}
