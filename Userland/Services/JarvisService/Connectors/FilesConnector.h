/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/Vector.h>
#include <AK/JsonArray.h>

namespace JarvisService {

struct RecentFile {
    ByteString path;
    ByteString description;
    ByteString last_modified;
    ByteString file_type;

    JsonObject to_json() const;
};

class FilesConnector final : public PersonalConnector {
public:
    static NonnullRefPtr<FilesConnector> create();

    virtual ~FilesConnector() override = default;

    virtual ByteString name() const override { return "LocalFiles"; }
    virtual ByteString provider_type() const override { return "VFS"; }
    virtual ConnectorStatus status() const override { return ConnectorStatus::Connected; }
    virtual bool is_authenticated() const override { return true; }
    virtual ByteString last_sync_time() const override { return "Real-time"; }

    virtual void sync() override;
    virtual void revoke() override {}
    virtual JsonObject to_json() const override;

    Vector<RecentFile> const& recent_files() const { return m_recent_files; }

private:
    FilesConnector();

    Vector<RecentFile> m_recent_files;
};

}
