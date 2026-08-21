/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include <AK/ByteString.h>
#include <AK/JsonObject.h>

namespace JarvisService {

class PersonaModel {
public:
    static PersonaModel& the();

    PersonaModel();

    ByteString generate_draft_for_peer(ByteString const& recipient, ByteString const& commitment);
    ByteString generate_draft_for_faculty(ByteString const& recipient, ByteString const& task);

    JsonObject to_json() const;

private:
    ByteString m_peer_tone { "Casual, concise, direct" };
    ByteString m_faculty_tone { "Formal, respectful, structured" };
    double m_persona_confidence { 0.85 };
};

}
