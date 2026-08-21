/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "FilesConnector.h"
#include <LibCore/DateTime.h>

namespace JarvisService {

JsonObject RecentFile::to_json() const
{
    JsonObject obj;
    obj.set("path", path);
    obj.set("description", description);
    obj.set("last_modified", last_modified);
    obj.set("file_type", file_type);
    return obj;
}

NonnullRefPtr<FilesConnector> FilesConnector::create()
{
    return adopt_ref(*new FilesConnector());
}

FilesConnector::FilesConnector()
{
    sync();
}

void FilesConnector::sync()
{
    m_recent_files.clear();
    m_recent_files.append({
        .path = "/home/anon/Capstone/OperatingSystemArchitecture.md",
        .description = "JARVIS OS Kernel & Capability Architecture Documentation",
        .last_modified = "Today, 08:00 AM",
        .file_type = "Markdown Document"
    });

    m_recent_files.append({
        .path = "/home/anon/Database/Assignment_Normalized_Schema.sql",
        .description = "Distributed Database SQL Schema (Due Tomorrow)",
        .last_modified = "Yesterday, 11:20 PM",
        .file_type = "SQL Script"
    });

    m_recent_files.append({
        .path = "/var/log/jarvis_journal.log",
        .description = "Cryptographic SHA-256 Capability Audit Ledger",
        .last_modified = "Active Stream",
        .file_type = "Cryptographic Log"
    });
}

JsonObject FilesConnector::to_json() const
{
    JsonObject obj;
    obj.set("name", name());
    obj.set("provider", provider_type());
    obj.set("status", status_string());
    obj.set("authenticated", is_authenticated());
    obj.set("last_sync", last_sync_time());

    JsonArray arr;
    for (auto const& f : m_recent_files)
        arr.must_append(f.to_json());
    obj.set("recent_files", arr);
    return obj;
}

}
