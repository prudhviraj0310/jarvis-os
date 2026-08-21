/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "PersonaModel.h"
#include <AK/StringBuilder.h>

namespace JarvisService {

PersonaModel& PersonaModel::the()
{
    static PersonaModel instance;
    return instance;
}

PersonaModel::PersonaModel()
{
}

ByteString PersonaModel::generate_draft_for_peer(ByteString const& recipient, ByteString const& commitment)
{
    (void)recipient;
    if (commitment.contains("project"sv))
        return "Yes bro, I'll send the project files tomorrow.";
    if (commitment.contains("presentation"sv) || commitment.contains("meeting"sv))
        return "Yes, see you at 2 PM in the library.";
    return ByteString::formatted("Yes, will do! ({})", commitment);
}

ByteString PersonaModel::generate_draft_for_faculty(ByteString const& recipient, ByteString const& task)
{
    (void)recipient;
    (void)task;
    StringBuilder sb;
    sb.append("Respected Sir,\n\n"sv);
    sb.append("I have completed the requested architecture deliverables and verified the cryptographic capability logs.\n\n"sv);
    sb.append("Sincerely,\nPrudhvi Raj"sv);
    return sb.to_byte_string();
}

JsonObject PersonaModel::to_json() const
{
    JsonObject obj;
    obj.set("peer_tone", m_peer_tone);
    obj.set("faculty_tone", m_faculty_tone);
    obj.set("confidence", m_persona_confidence);
    obj.set("provenance", "[PERSONA-INFERRED, confidence=0.85]");
    return obj;
}

}
