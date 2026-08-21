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

enum class ProvenanceLevel {
    Observed,
    Derived,
    Inferred,
    Unknown
};

struct MemoryItem {
    ByteString key;
    ByteString content;
    ProvenanceLevel provenance { ProvenanceLevel::Observed };
    double confidence { 1.0 };
    ByteString source_channel;
    ByteString timestamp;

    ByteString provenance_string() const;
    JsonObject to_json() const;
};

class PersonalMemory {
public:
    static PersonalMemory& the();

    PersonalMemory();

    Vector<MemoryItem> const& memories() const { return m_memories; }
    void add_memory(MemoryItem item);
    Vector<MemoryItem> query(ByteString const& topic) const;

    JsonArray to_json() const;

private:
    Vector<MemoryItem> m_memories;
};

}
