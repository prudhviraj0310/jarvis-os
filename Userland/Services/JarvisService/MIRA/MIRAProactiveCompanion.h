/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/Vector.h>
#include <AK/JsonObject.h>
#include <AK/JsonArray.h>

namespace JarvisService {

struct ProactiveCheckIn {
    ByteString trigger_type; // "DEADLINE_APPROACHING", "UNANSWERED_MESSAGE", "CALENDAR_PREP"
    ByteString message;
    ByteString recommended_action;
    int urgency { 5 }; // 1 to 10

    JsonObject to_json() const;
};

class MIRAProactiveCompanion {
public:
    static MIRAProactiveCompanion& the();

    MIRAProactiveCompanion();

    Vector<ProactiveCheckIn> const& check_ins() const { return m_check_ins; }
    void refresh_check_ins();

    JsonObject to_json() const;

private:
    Vector<ProactiveCheckIn> m_check_ins;
};

}
