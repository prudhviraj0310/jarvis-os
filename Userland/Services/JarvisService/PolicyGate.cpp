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
    // Read & Informational capabilities
    m_rules.set("system.morning_briefing"_string, PolicyTier::Allowed);
    m_rules.set("system.whatsapp"_string, PolicyTier::Allowed);
    m_rules.set("system.email"_string, PolicyTier::Allowed);
    m_rules.set("system.calendar"_string, PolicyTier::Allowed);
    m_rules.set("system.news"_string, PolicyTier::Allowed);
    m_rules.set("system.percentage"_string, PolicyTier::Allowed);
    m_rules.set("system.processes"_string, PolicyTier::Allowed);
    m_rules.set("system.memory"_string, PolicyTier::Allowed);
    m_rules.set("security.shield_status"_string, PolicyTier::Allowed);

    m_rules.set("whatsapp.read"_string, PolicyTier::Allowed);
    m_rules.set("whatsapp.draft"_string, PolicyTier::Allowed);
    m_rules.set("email.read"_string, PolicyTier::Allowed);
    m_rules.set("email.summarize"_string, PolicyTier::Allowed);
    m_rules.set("email.draft"_string, PolicyTier::Allowed);
    m_rules.set("calendar.list"_string, PolicyTier::Allowed);
    m_rules.set("news.briefing"_string, PolicyTier::Allowed);
    m_rules.set("memory.inspect"_string, PolicyTier::Allowed);
    m_rules.set("automation.status"_string, PolicyTier::Allowed);
    m_rules.set("action.handle_it"_string, PolicyTier::Allowed);
    m_rules.set("filesystem.read"_string, PolicyTier::Allowed);
    m_rules.set("kernel.dmesg"_string, PolicyTier::Allowed);

    // MIRA Subsystem capabilities
    m_rules.set("mira.dashboard"_string, PolicyTier::Allowed);
    m_rules.set("mira.gateway"_string, PolicyTier::Allowed);
    m_rules.set("mira.wiki"_string, PolicyTier::Allowed);
    m_rules.set("mira.companion"_string, PolicyTier::Allowed);
    m_rules.set("mira.mcp"_string, PolicyTier::Allowed);

    // Consequential actions (Require explicit human confirmation!)
    m_rules.set("whatsapp.send"_string, PolicyTier::ConfirmRequired);
    m_rules.set("email.send"_string, PolicyTier::ConfirmRequired);
    m_rules.set("calendar.add_event"_string, PolicyTier::ConfirmRequired);
    m_rules.set("action.confirm_and_execute"_string, PolicyTier::ConfirmRequired);
    m_rules.set("filesystem.write"_string, PolicyTier::ConfirmRequired);
    m_rules.set("terminal.execute"_string, PolicyTier::ConfirmRequired);
    m_rules.set("security.lockdown"_string, PolicyTier::ConfirmRequired);
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
