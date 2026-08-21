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

struct Contact {
    ByteString name;
    ByteString relationship;
    ByteString organization;
    ByteString communication_style;
    int importance_score { 5 }; // 1 to 10
    ByteString last_interaction;
    ByteString preferred_channel { "WhatsApp" };
    ByteString notes;

    JsonObject to_json() const;
};

class ContactGraph {
public:
    static ContactGraph& the();

    ContactGraph();

    Vector<Contact> const& contacts() const { return m_contacts; }
    Optional<Contact> find_contact(ByteString const& name) const;
    void add_or_update_contact(Contact contact);

    JsonArray to_json() const;

private:
    Vector<Contact> m_contacts;
};

}
