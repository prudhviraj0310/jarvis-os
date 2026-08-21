/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/String.h>

namespace JarvisService {

class UserProfile {
public:
    static UserProfile& the();

    UserProfile();

    ByteString name() const { return m_name; }
    ByteString email() const { return m_email; }
    ByteString course_name() const { return m_course_name; }
    double attendance_percentage() const { return m_attendance_percentage; }
    double target_percentage() const { return m_target_percentage; }
    bool permission_granted() const { return m_permission_granted; }

    void reload();

private:
    ByteString m_name { "Prudhvi Raj" };
    ByteString m_email { "prudhvinaik2005@gmail.com" };
    ByteString m_course_name { "Computer Science & Engineering" };
    double m_attendance_percentage { 87.5 };
    double m_target_percentage { 85.0 };
    bool m_permission_granted { true };
};

}
