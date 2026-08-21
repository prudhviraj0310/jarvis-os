/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "PersonalMemory.h"

namespace JarvisService {

ByteString MemoryItem::provenance_string() const
{
    switch (provenance) {
    case ProvenanceLevel::Observed:
        return "[OBSERVED]";
    case ProvenanceLevel::Derived:
        return "[DERIVED]";
    case ProvenanceLevel::Inferred:
        return ByteString::formatted("[INFERRED, confidence={:.2f}]", confidence);
    case ProvenanceLevel::Unknown:
    default:
        return "[UNKNOWN]";
    }
}

JsonObject MemoryItem::to_json() const
{
    JsonObject obj;
    obj.set("key", key);
    obj.set("content", content);
    obj.set("provenance", provenance_string());
    obj.set("confidence", confidence);
    obj.set("source_channel", source_channel);
    obj.set("timestamp", timestamp);
    return obj;
}

PersonalMemory& PersonalMemory::the()
{
    static PersonalMemory instance;
    return instance;
}

PersonalMemory::PersonalMemory()
{
    m_memories.append({
        .key = "Rahul communication style",
        .content = "User usually replies to Rahul casually and directly.",
        .provenance = ProvenanceLevel::Inferred,
        .confidence = 0.88,
        .source_channel = "WhatsApp",
        .timestamp = "Recent"
    });

    m_memories.append({
        .key = "Faculty communication style",
        .content = "Communication with faculty (Prof. Krishnamurthy) is strictly formal.",
        .provenance = ProvenanceLevel::Observed,
        .confidence = 1.0,
        .source_channel = "Email",
        .timestamp = "Recent"
    });

    m_memories.append({
        .key = "Database Assignment Deadline",
        .content = "Database assignment is due tomorrow by 11:59 PM.",
        .provenance = ProvenanceLevel::Observed,
        .confidence = 1.0,
        .source_channel = "Email / Classroom",
        .timestamp = "Today"
    });

    m_memories.append({
        .key = "Capstone Project Review",
        .content = "Project review scheduled with faculty next Monday.",
        .provenance = ProvenanceLevel::Derived,
        .confidence = 0.95,
        .source_channel = "Calendar",
        .timestamp = "Today"
    });
}

void PersonalMemory::add_memory(MemoryItem item)
{
    m_memories.append(item);
}

Vector<MemoryItem> PersonalMemory::query(ByteString const& topic) const
{
    Vector<MemoryItem> results;
    auto lower = topic.to_lowercase();
    for (auto const& item : m_memories) {
        if (item.key.to_lowercase().contains(lower) || item.content.to_lowercase().contains(lower))
            results.append(item);
    }
    return results;
}

JsonArray PersonalMemory::to_json() const
{
    JsonArray arr;
    for (auto const& item : m_memories) {
        arr.must_append(item.to_json());
    }
    return arr;
}

}
