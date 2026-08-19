/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "JournalManager.h"
#include <AK/JsonObject.h>
#include <LibCore/DateTime.h>
#include <LibCore/File.h>
#include <LibCrypto/Hash/SHA2.h>

namespace JournalService {

JournalManager& JournalManager::the()
{
    static JournalManager instance;
    return instance;
}

JournalManager::JournalManager()
{
    m_genesis_entry.sequence_number = 0;
    m_genesis_entry.actor = "SYSTEM"_string;
    m_genesis_entry.capability_name = "GENESIS"_string;
    m_genesis_entry.previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"_string;
    m_genesis_entry.block_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"_string;
}

JournalEntry JournalManager::append_entry(String const& actor, String const& capability, String const& args, String const& result)
{
    JournalEntry entry;
    entry.sequence_number = m_entries.size() + 1;
    entry.actor = actor;
    entry.capability_name = capability;
    entry.arguments_json = args;
    entry.result_json = result;
    entry.previous_hash = latest_entry().block_hash;

    auto time_str = Core::DateTime::now().to_byte_string();
    entry.timestamp = String::from_byte_string(time_str).release_value_but_fixme_should_propagate_errors();

    StringBuilder hash_input;
    hash_input.append(String::formatted("{}", entry.sequence_number).release_value_but_fixme_should_propagate_errors());
    hash_input.append(entry.timestamp);
    hash_input.append(entry.actor);
    hash_input.append(entry.capability_name);
    hash_input.append(entry.arguments_json);
    hash_input.append(entry.result_json);
    hash_input.append(entry.previous_hash);

    Crypto::Hash::SHA256 sha;
    auto input_str = hash_input.to_byte_string();
    sha.update(input_str.bytes());
    auto digest = sha.digest();
    StringBuilder hex_builder;
    for (size_t i = 0; i < sizeof(digest.data); ++i) {
        hex_builder.appendff("{:02x}", digest.data[i]);
    }
    entry.block_hash = String::from_byte_string(hex_builder.to_byte_string()).release_value_but_fixme_should_propagate_errors();

    m_entries.append(entry);
    persist_entry(entry);

    return entry;
}

void JournalManager::persist_entry(JournalEntry const& entry)
{
    JsonObject obj;
    obj.set("sequence", static_cast<double>(entry.sequence_number));
    obj.set("timestamp", entry.timestamp.to_byte_string());
    obj.set("actor", entry.actor.to_byte_string());
    obj.set("capability", entry.capability_name.to_byte_string());
    obj.set("arguments", entry.arguments_json.to_byte_string());
    obj.set("result", entry.result_json.to_byte_string());
    obj.set("previous_hash", entry.previous_hash.to_byte_string());
    obj.set("block_hash", entry.block_hash.to_byte_string());

    auto file_or_error = Core::File::open("/var/log/jarvis_journal.log"sv, Core::File::OpenMode::Write | Core::File::OpenMode::Append);
    if (!file_or_error.is_error()) {
        auto& file = file_or_error.value();
        auto line = String::formatted("{}\n", obj.to_byte_string()).release_value_but_fixme_should_propagate_errors();
        (void)file->write_until_depleted(line.bytes());
    }
}

}
