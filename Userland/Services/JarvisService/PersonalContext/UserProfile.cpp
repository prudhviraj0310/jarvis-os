/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "UserProfile.h"
#include <LibCore/ConfigFile.h>

namespace JarvisService {

UserProfile& UserProfile::the()
{
    static UserProfile instance;
    return instance;
}

UserProfile::UserProfile()
{
    reload();
}

void UserProfile::reload()
{
    auto config_or_error = Core::ConfigFile::open("/etc/jarvis/config.ini"sv);
    if (!config_or_error.is_error()) {
        auto config = config_or_error.value();
        m_permission_granted = config->read_bool_entry("User"sv, "PermissionGranted"sv, true);
        m_name = config->read_entry("User"sv, "Name"sv, "Prudhvi Raj");
        m_email = config->read_entry("User"sv, "Email"sv, "prudhvinaik2005@gmail.com");
        m_course_name = config->read_entry("Attendance"sv, "CourseName"sv, "Computer Science & Engineering");
        auto att_str = config->read_entry("Attendance"sv, "CurrentPercentage"sv, "87.5");
        auto tgt_str = config->read_entry("Attendance"sv, "TargetPercentage"sv, "85.0");
        m_attendance_percentage = att_str.replace("%"sv, ""sv, ReplaceMode::All).to_number<double>().value_or(87.5);
        m_target_percentage = tgt_str.replace("%"sv, ""sv, ReplaceMode::All).to_number<double>().value_or(85.0);
    }
}

}
