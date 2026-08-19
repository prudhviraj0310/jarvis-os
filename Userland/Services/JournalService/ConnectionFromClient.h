/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <LibIPC/ConnectionFromClient.h>
#include <JournalService/JournalClientEndpoint.h>
#include <JournalService/JournalServerEndpoint.h>

namespace JournalService {

class ConnectionFromClient final : public IPC::ConnectionFromClient<JournalClientEndpoint, JournalServerEndpoint> {
    C_OBJECT(ConnectionFromClient)
public:
    ~ConnectionFromClient() override = default;

    virtual void die() override;

private:
    explicit ConnectionFromClient(NonnullOwnPtr<Core::LocalSocket>, int client_id);

    virtual Messages::JournalServer::AppendEntryResponse append_entry(String const&, String const&, String const&, String const&) override;
    virtual Messages::JournalServer::GetLatestBlockResponse get_latest_block() override;
    virtual Messages::JournalServer::GetJournalCountResponse get_journal_count() override;
};

}
