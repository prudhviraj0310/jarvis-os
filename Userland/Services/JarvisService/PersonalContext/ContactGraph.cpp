/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ContactGraph.h"

namespace JarvisService {

JsonObject Contact::to_json() const
{
    JsonObject obj;
    obj.set("name", name);
    obj.set("relationship", relationship);
    obj.set("organization", organization);
    obj.set("communication_style", communication_style);
    obj.set("importance_score", importance_score);
    obj.set("last_interaction", last_interaction);
    obj.set("preferred_channel", preferred_channel);
    obj.set("notes", notes);
    return obj;
}

ContactGraph& ContactGraph::the()
{
    static ContactGraph instance;
    return instance;
}

ContactGraph::ContactGraph()
{
    // Seed key contacts
    m_contacts.append({
        .name = "Rahul Sharma",
        .relationship = "Project Collaborator / Colleague",
        .organization = "OS Core Research",
        .communication_style = "Casual / Direct",
        .importance_score = 9,
        .last_interaction = "Today, 07:45 AM",
        .preferred_channel = "WhatsApp",
        .notes = "Working on Database Assignment & Kernel Modules"
    });

    m_contacts.append({
        .name = "Prof. Krishnamurthy",
        .relationship = "Academic Advisor / Faculty",
        .organization = "Dept of Computer Science",
        .communication_style = "Formal / Precise",
        .importance_score = 10,
        .last_interaction = "Yesterday, 04:15 PM",
        .preferred_channel = "Email",
        .notes = "Final Year Capstone Project Supervisor"
    });

    m_contacts.append({
        .name = "Priya V.",
        .relationship = "Study Group Lead",
        .organization = "College",
        .communication_style = "Friendly",
        .importance_score = 7,
        .last_interaction = "Yesterday, 08:30 PM",
        .preferred_channel = "WhatsApp",
        .notes = "Distributed Systems Study Group"
    });
}

Optional<Contact> ContactGraph::find_contact(ByteString const& name) const
{
    auto query = name.to_lowercase();
    for (auto const& c : m_contacts) {
        if (c.name.to_lowercase().contains(query))
            return c;
    }
    return {};
}

void ContactGraph::add_or_update_contact(Contact contact)
{
    for (size_t i = 0; i < m_contacts.size(); ++i) {
        if (m_contacts[i].name == contact.name) {
            m_contacts[i] = contact;
            return;
        }
    }
    m_contacts.append(contact);
}

JsonArray ContactGraph::to_json() const
{
    JsonArray arr;
    for (auto const& c : m_contacts) {
        arr.must_append(c.to_json());
    }
    return arr;
}

}
