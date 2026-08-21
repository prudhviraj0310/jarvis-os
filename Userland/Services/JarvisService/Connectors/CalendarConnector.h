/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "PersonalConnector.h"
#include <AK/Vector.h>
#include <AK/JsonArray.h>

namespace JarvisService {

struct CalendarEvent {
    ByteString title;
    ByteString start_time;
    ByteString end_time;
    ByteString location;
    ByteString participants;
    ByteString prep_notes;
    bool is_today { true };

    JsonObject to_json() const;
};

class CalendarConnector final : public PersonalConnector {
public:
    static NonnullRefPtr<CalendarConnector> create();

    virtual ~CalendarConnector() override = default;

    virtual ByteString name() const override { return "Calendar"; }
    virtual ByteString provider_type() const override { return "LocalCal"; }
    virtual ConnectorStatus status() const override { return m_status; }
    virtual bool is_authenticated() const override { return m_authenticated; }
    virtual ByteString last_sync_time() const override { return m_last_sync; }

    virtual void sync() override;
    virtual void revoke() override;
    virtual JsonObject to_json() const override;

    Vector<CalendarEvent> const& events() const { return m_events; }
    Vector<CalendarEvent> today_events() const;

    bool add_event(CalendarEvent event);

private:
    CalendarConnector();

    ConnectorStatus m_status { ConnectorStatus::Connected };
    bool m_authenticated { true };
    ByteString m_last_sync { "Just now" };
    Vector<CalendarEvent> m_events;
};

}
