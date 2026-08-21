/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/Vector.h>
#include <AK/JsonArray.h>

namespace JarvisService {

struct NewsStory {
    ByteString category; // "AI", "Technology", "India", "Global", "Finance"
    ByteString headline;
    ByteString summary;
    ByteString source;
    int importance { 8 }; // 1 to 10

    JsonObject to_json() const;
};

class NewsConnector final : public PersonalConnector {
public:
    static NonnullRefPtr<NewsConnector> create();

    virtual ~NewsConnector() override = default;

    virtual ByteString name() const override { return "News"; }
    virtual ByteString provider_type() const override { return "ClusteredRSS"; }
    virtual ConnectorStatus status() const override { return m_status; }
    virtual bool is_authenticated() const override { return true; }
    virtual ByteString last_sync_time() const override { return m_last_sync; }

    virtual void sync() override;
    virtual void revoke() override;
    virtual JsonObject to_json() const override;

    Vector<NewsStory> const& stories() const { return m_stories; }
    Vector<NewsStory> stories_by_category(ByteString const& category) const;

private:
    NewsConnector();

    ConnectorStatus m_status { ConnectorStatus::Connected };
    ByteString m_last_sync { "Just now" };
    Vector<NewsStory> m_stories;
};

}
