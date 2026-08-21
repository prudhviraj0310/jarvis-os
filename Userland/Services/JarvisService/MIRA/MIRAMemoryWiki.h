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

struct WikiArticle {
    ByteString title;
    ByteString category;
    ByteString content;
    ByteString last_updated;
    Vector<ByteString> linked_entities;

    JsonObject to_json() const;
};

class MIRAMemoryWiki {
public:
    static MIRAMemoryWiki& the();

    MIRAMemoryWiki();

    Vector<WikiArticle> const& articles() const { return m_articles; }
    Optional<WikiArticle> find_article(ByteString const& title) const;
    void record_reflection(ByteString const& topic, ByteString const& reflection);

    JsonObject to_json() const;

private:
    Vector<WikiArticle> m_articles;
};

}
