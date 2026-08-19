/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/String.h>
#include <AK/Vector.h>

namespace JournalService {

struct JournalEntry {
    u64 sequence_number { 0 };
    String timestamp {};
    String actor {};
    String capability_name {};
    String arguments_json {};
    String result_json {};
    String previous_hash {};
    String block_hash {};
};

class JournalManager {
public:
    static JournalManager& the();

    JournalEntry append_entry(String const& actor, String const& capability, String const& args, String const& result);
    JournalEntry const& latest_entry() const { return m_entries.is_empty() ? m_genesis_entry : m_entries.last(); }
    u64 entry_count() const { return m_entries.size(); }

private:
    JournalManager();
    void persist_entry(JournalEntry const& entry);

    JournalEntry m_genesis_entry;
    Vector<JournalEntry> m_entries;
};

}
