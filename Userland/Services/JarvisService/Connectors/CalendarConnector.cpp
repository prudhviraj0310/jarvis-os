/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "CalendarConnector.h"
#include <LibCore/DateTime.h>

namespace JarvisService {

JsonObject CalendarEvent::to_json() const
{
    JsonObject obj;
    obj.set("title", title);
    obj.set("start_time", start_time);
    obj.set("end_time", end_time);
    obj.set("location", location);
    obj.set("participants", participants);
    obj.set("prep_notes", prep_notes);
    obj.set("is_today", is_today);
    return obj;
}

NonnullRefPtr<CalendarConnector> CalendarConnector::create()
{
    return adopt_ref(*new CalendarConnector());
}

CalendarConnector::CalendarConnector()
{
    sync();
}

void CalendarConnector::sync()
{
    m_last_sync = Core::DateTime::now().to_byte_string();
    m_events.clear();

    m_events.append({
        .title = "Operating Systems Capstone Review & Demo",
        .start_time = "10:30 AM",
        .end_time = "11:30 AM",
        .location = "Lab 402 / Virtual Room B",
        .participants = "Prof. Krishnamurthy, Rahul Sharma, Prudhvi Raj",
        .prep_notes = "Prepare live QEMU demonstration of JARVIS CapabilityDispatcher & JournalService",
        .is_today = true
    });

    m_events.append({
        .title = "Distributed Systems Group Presentation Prep",
        .start_time = "02:00 PM",
        .end_time = "03:00 PM",
        .location = "Central Library Meeting Room 2",
        .participants = "Priya V., Rahul Sharma, Prudhvi Raj",
        .prep_notes = "Review Raft consensus slides and benchmark graphs",
        .is_today = true
    });
}

Vector<CalendarEvent> CalendarConnector::today_events() const
{
    Vector<CalendarEvent> list;
    for (auto const& e : m_events) {
        if (e.is_today)
            list.append(e);
    }
    return list;
}

bool CalendarConnector::add_event(CalendarEvent event)
{
    m_events.append(event);
    return true;
}

void CalendarConnector::revoke()
{
    m_authenticated = false;
    m_status = ConnectorStatus::AwaitingAuth;
    m_events.clear();
}

JsonObject CalendarConnector::to_json() const
{
    JsonObject obj;
    obj.set("name", name());
    obj.set("provider", provider_type());
    obj.set("status", status_string());
    obj.set("authenticated", is_authenticated());
    obj.set("last_sync", last_sync_time());

    JsonArray evs;
    for (auto const& e : m_events)
        evs.must_append(e.to_json());
    obj.set("events", evs);
    return obj;
}

}
