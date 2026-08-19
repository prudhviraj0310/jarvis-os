/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ConnectionFromClient.h"
#include "JournalManager.h"

namespace JournalService {

ConnectionFromClient::ConnectionFromClient(NonnullOwnPtr<Core::LocalSocket> socket, int client_id)
    : IPC::ConnectionFromClient<JournalClientEndpoint, JournalServerEndpoint>(*this, move(socket), client_id)
{
}

void ConnectionFromClient::die()
{
}

Messages::JournalServer::AppendEntryResponse ConnectionFromClient::append_entry(String const& actor, String const& cap, String const& args, String const& res)
{
    auto entry = JournalManager::the().append_entry(actor, cap, args, res);
    return { true, entry.sequence_number, entry.block_hash };
}

Messages::JournalServer::GetLatestBlockResponse ConnectionFromClient::get_latest_block()
{
    auto const& latest = JournalManager::the().latest_entry();
    return { latest.sequence_number, latest.block_hash };
}

Messages::JournalServer::GetJournalCountResponse ConnectionFromClient::get_journal_count()
{
    return { JournalManager::the().entry_count() };
}

}
