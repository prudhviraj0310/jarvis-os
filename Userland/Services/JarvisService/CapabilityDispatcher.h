/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/String.h>

namespace JarvisService {

class CapabilityDispatcher {
public:
    static CapabilityDispatcher& the();

    String dispatch(String const& capability_name, String const& arguments_json, String const& request_id);
    String get_system_health();
    String process_voice_command(String const& voice_text, String const& request_id);

private:
    CapabilityDispatcher() = default;
    int m_threat_level { 0 }; // 0: NOMINAL, 1: ELEVATED, 2: LOCKDOWN
};

}
