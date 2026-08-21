/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "MIRAProactiveCompanion.h"

namespace JarvisService {

JsonObject ProactiveCheckIn::to_json() const
{
    JsonObject obj;
    obj.set("trigger_type", trigger_type);
    obj.set("message", message);
    obj.set("recommended_action", recommended_action);
    obj.set("urgency", urgency);
    return obj;
}

MIRAProactiveCompanion& MIRAProactiveCompanion::the()
{
    static MIRAProactiveCompanion instance;
    return instance;
}

MIRAProactiveCompanion::MIRAProactiveCompanion()
{
    refresh_check_ins();
}

void MIRAProactiveCompanion::refresh_check_ins()
{
    m_check_ins.clear();

    m_check_ins.append({
        .trigger_type = "DEADLINE_APPROACHING",
        .message = "Capstone Architecture Documentation due tomorrow at 5:00 PM.",
        .recommended_action = "Review final draft and execute email acknowledgment.",
        .urgency = 9
    });

    m_check_ins.append({
        .trigger_type = "UNANSWERED_MESSAGE",
        .message = "Rahul Sharma is awaiting your confirmation regarding project code.",
        .recommended_action = "Send drafted reply: 'Yes, I\\'ll send it tomorrow.'",
        .urgency = 8
    });

    m_check_ins.append({
        .trigger_type = "CALENDAR_PREP",
        .message = "Capstone Demonstration starts at 10:30 AM in Lab 402.",
        .recommended_action = "Pre-warm QEMU virtual machine environment.",
        .urgency = 7
    });
}

JsonObject MIRAProactiveCompanion::to_json() const
{
    JsonObject obj;
    obj.set("status", "ACTIVE");
    obj.set("check_in_count", static_cast<int>(m_check_ins.size()));

    JsonArray arr;
    for (auto const& c : m_check_ins)
        arr.must_append(c.to_json());
    obj.set("check_ins", arr);
    return obj;
}

}
