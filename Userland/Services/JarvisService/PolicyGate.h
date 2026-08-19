/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/String.h>
#include <AK/HashMap.h>

namespace JarvisService {

enum class PolicyTier {
    Allowed,
    ConfirmRequired,
    RestrictedRoot,
    Denied
};

class PolicyGate {
public:
    static PolicyGate& the();

    PolicyTier evaluate_capability(StringView capability_name) const;
    String policy_tier_to_string(PolicyTier tier) const;

private:
    PolicyGate();
    HashMap<String, PolicyTier> m_rules;
};

}
