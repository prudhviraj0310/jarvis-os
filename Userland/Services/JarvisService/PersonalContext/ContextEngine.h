/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#pragma once

#include "UserProfile.h"
#include "ContactGraph.h"
#include "PersonalMemory.h"
#include "../Connectors/ConnectorRegistry.h"
#include "../Connectors/WhatsAppConnector.h"
#include "../Connectors/EmailConnector.h"
#include "../Connectors/CalendarConnector.h"
#include "../Connectors/NewsConnector.h"
#include "../Connectors/FilesConnector.h"
#include "../Automation/AutomationEngine.h"
#include "../Persona/PersonaModel.h"
#include <AK/ByteString.h>
#include <AK/JsonObject.h>

namespace JarvisService {

class ContextEngine {
public:
    static ContextEngine& the();

    ContextEngine();

    void initialize();
    ByteString generate_morning_briefing();
    ByteString generate_inbox_intelligence();
    ByteString generate_whatsapp_intelligence();
    ByteString generate_calendar_matrix();
    ByteString generate_news_briefing();

    JsonObject to_json();

private:
    RefPtr<WhatsAppConnector> m_whatsapp;
    RefPtr<EmailConnector> m_email;
    RefPtr<CalendarConnector> m_calendar;
    RefPtr<NewsConnector> m_news;
    RefPtr<FilesConnector> m_files;
};

}
