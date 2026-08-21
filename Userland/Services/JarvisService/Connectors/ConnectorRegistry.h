/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/HashMap.h>
#include <AK/JsonArray.h>
#include <AK/NonnullRefPtr.h>

namespace JarvisService {

class ConnectorRegistry {
public:
    static ConnectorRegistry& the();

    ConnectorRegistry();

    void register_connector(NonnullRefPtr<PersonalConnector> connector);
    RefPtr<PersonalConnector> get_connector(ByteString const& name);
    void sync_all();

    JsonArray to_json() const;

private:
    HashMap<ByteString, NonnullRefPtr<PersonalConnector>> m_connectors;
};

}
