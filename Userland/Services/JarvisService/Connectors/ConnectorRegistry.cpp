/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ConnectorRegistry.h"

namespace JarvisService {

ConnectorRegistry& ConnectorRegistry::the()
{
    static ConnectorRegistry instance;
    return instance;
}

ConnectorRegistry::ConnectorRegistry()
{
}

void ConnectorRegistry::register_connector(NonnullRefPtr<PersonalConnector> connector)
{
    m_connectors.set(connector->name(), connector);
}

RefPtr<PersonalConnector> ConnectorRegistry::get_connector(ByteString const& name)
{
    auto it = m_connectors.find(name);
    if (it == m_connectors.end())
        return nullptr;
    return it->value;
}

void ConnectorRegistry::sync_all()
{
    for (auto& item : m_connectors) {
        item.value->sync();
    }
}

JsonArray ConnectorRegistry::to_json() const
{
    JsonArray arr;
    for (auto const& item : m_connectors) {
        arr.must_append(item.value->to_json());
    }
    return arr;
}

}
