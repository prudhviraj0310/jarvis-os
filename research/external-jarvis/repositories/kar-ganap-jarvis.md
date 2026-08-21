# Research Inspection: kar-ganap / jarvis

- **Repository URL**: `https://github.com/kar-ganap/jarvis`
- **Primary License**: MIT License
- **Primary Languages**: Python 3.11+, JavaScript / Node.js (WhatsApp Baileys bridge)
- **Primary Frameworks**: FastAPI, LangChain / LangGraph, Pydantic, Baileys (@whiskeysockets/baileys)

---

## 1. System Architecture
`kar-ganap/jarvis` is designed as a personal life assistant with a clean decoupling between the core reasoning engine and external productivity services:
* **Tool Abstraction Layer (`src/jarvis/tools/`)**: Wraps Gmail, Google Calendar, Sheets, Docs, Notion, Todoist, Browser, and Web Search behind standard interfaces.
* **WhatsApp Multi-Device Bridge (`bridge/whatsapp/`)**: Standalone Node.js service running `@whiskeysockets/baileys` that exposes an HTTP/WebSocket REST API for QR-code authentication, message ingestion, and outbound sending.
* **Scheduler & Proactive Engine (`src/jarvis/scheduler/`)**: Periodic cron and event triggers that poll external data sources and initiate proactive conversation check-ins.
* **Agent Factory (`src/jarvis/agent/`)**: Configurable persona model adapting tone and verbosity based on user preferences.

---

## 2. Major Capabilities
1. **Real Multi-Device WhatsApp Ingestion**: Handles raw WhatsApp Web sockets without needing expensive official WhatsApp Business API tokens.
2. **Productivity Suite Synchronization**: Two-way sync with Google Workspace (Gmail, Calendar, Docs, Sheets) and Notion/Todoist.
3. **Persistent Memory (`src/jarvis/memory/`)**: Structured conversation logs, user preference extraction, and semantic vector memory.
4. **Proactive Notifications**: Triggers scheduled reminders and alerts based on upcoming deadlines or unread priority emails.

---

## 3. Entry Points & Key Modules
* **Core Application**: `src/jarvis/app.py`, `src/jarvis/__main__.py`.
* **WhatsApp Bridge Entry**: `bridge/whatsapp/src/index.js`, `session.js`, `routes.js`.
* **Tool Registry**: `src/jarvis/tools/` (Base tool class with input validation).
* **Scheduler Engine**: `src/jarvis/scheduler/engine.py` (APScheduler/Asyncio event loop).

---

## 4. Dependencies
* Python: `fastapi`, `langchain`, `pydantic`, `google-api-python-client`, `notion-client`, `todoist-api-python`, `apscheduler`
* Node.js: `@whiskeysockets/baileys`, `express`, `qrcode-terminal`

---

## 5. Security & Machine Sovereignty Analysis
* **Auth Storage**: Stores Google OAuth tokens and WhatsApp encryption keys in local directory (`config/tokens/`).
* **Tool Execution**: Tools execute with ambient credentials. Missing strict permission confirmation prompts before modifying Google Sheets or sending WhatsApp messages.

---

## 6. What Can Be Adapted to JARVIS OS
* **WhatsApp Baileys Bridge Architecture**: The Node.js bridge pattern is the industry standard for non-business personal WhatsApp integration. Can be packaged as a sandboxed local background service (`jarvis-whatsapp-bridge`).
* **Service Tool Abstraction Pattern**: Decoupling external APIs (Gmail, Calendar, Notion) behind clean capability interfaces.

---

## 7. What is NOT Suitable
* Heavy reliance on external cloud APIs (Google Cloud OAuth, Notion API) without local offline fallbacks.

---

## 8. License Compliance
* **MIT License**: Fully permissive for commercial modification and redistribution with copyright attribution.
