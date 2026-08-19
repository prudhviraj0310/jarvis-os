/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "PolicyGate.h"

namespace JarvisService {

PolicyGate& PolicyGate::the()
{
    static PolicyGate instance;
    return instance;
}

PolicyGate::PolicyGate()
{
    m_rules.set("filesystem.read"_string, PolicyTier::Allowed);
    m_rules.set("filesystem.write"_string, PolicyTier::ConfirmRequired);
    m_rules.set("system.processes"_string, PolicyTier::Allowed);
    m_rules.set("system.memory"_string, PolicyTier::Allowed);
    m_rules.set("terminal.execute"_string, PolicyTier::ConfirmRequired);
    m_rules.set("kernel.dmesg"_string, PolicyTier::Allowed);
}

PolicyTier PolicyGate::evaluate_capability(StringView capability_name) const
{
    auto it = m_rules.find(capability_name);
    if (it == m_rules.end())
        return PolicyTier::Denied;
    return it->value;
}

String PolicyGate::policy_tier_to_string(PolicyTier tier) const
{
    switch (tier) {
    case PolicyTier::Allowed:
        return "ALLOWED"_string;
    case PolicyTier::ConfirmRequired:
        return "CONFIRM_REQUIRED"_string;
    case PolicyTier::RestrictedRoot:
        return "RESTRICTED_ROOT"_string;
    case PolicyTier::Denied:
    default:
        return "DENIED"_string;
    }
}

}
