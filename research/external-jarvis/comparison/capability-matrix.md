# JARVIS OS — Open-Source Capability Comparison Matrix

| Capability Dimension | dev-core-busy | kar-ganap | yashvar23 | Raghava001 | Friday | ambartsumov | **JARVIS OS Target** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CORE INTELLIGENCE** | | | | | | | |
| Multi-Model Routing | ✅ (LiteLLM) | ⚠️ (Single) | ✅ (Multi-Tier) | ⚠️ (Gemini) | ✅ (LiteLLM) | ✅ (Router) | **✅ (Dual-Tier Edge/Deep)** |
| Agent Orchestration | ✅ (Monolithic) | ✅ (LangGraph) | ✅ (Distributed) | ⚠️ (State Mach) | ✅ (Deterministic) | ✅ (Multi-agent) | **✅ (MIRA Core Engine)** |
| Planning & Replanning| ✅ (TaskGraph) | ⚠️ (Basic) | ✅ (Workflows) | ❌ (Reactive) | ✅ (Simulate/Replan)| ✅ (OpenManus) | **✅ (Plan-Validate-Execute)**|
| Tool Calling Standard | ✅ (Custom/MCP) | ✅ (LangChain) | ✅ (Internal) | ⚠️ (Functions) | ✅ (ActionBroker)| ✅ (MCP Protocol) | **✅ (Native C++ & MCP Host)**|
| **PERSONAL MEMORY** | | | | | | | |
| Long-Term Memory | ✅ (ChromaDB) | ✅ (Vector/SQL) | ✅ (SQLite) | ✅ (JSON files) | ✅ (Vault/Graph) | ✅ (Vector/RAG) | **✅ (MIRA Memory Wiki)** |
| Knowledge Graph | ⚠️ (RAG-only) | ❌ | ⚠️ (Relational) | ❌ | ✅ (Entity Nodes) | ⚠️ (RAG) | **✅ (Knowledge Graph & Wiki)**|
| User Model & Provenance| ⚠️ (Basic Profile)| ⚠️ (Tone config)| ✅ (User Model) | ⚠️ (Habit log) | ✅ (Persona graph)| ⚠️ (Basic) | **✅ (Provenance Tags)** |
| Contact & Circle Graph| ⚠️ (LDAP/CRM) | ⚠️ (Contacts) | ⚠️ (Directory) | ❌ | ✅ (Circle Care) | ⚠️ (Chat lists) | **✅ (Relationship Matrix)** |
| **COMMUNICATION** | | | | | | | |
| WhatsApp Multi-Device | ✅ (Websocket) | ✅ (Baileys) | ❌ | ⚠️ (Mock bridge)| ⚠️ (WhatsApp Web)| ✅ (Baileys) | **✅ (Sandboxed Bridge)** |
| Telegram Bridge | ✅ (Bot API) | ❌ | ❌ | ❌ | ⚠️ (Bot API) | ✅ (Telethon) | **✅ (MIRA Gateway)** |
| Email / Gmail / IMAP | ✅ (IMAP Runner)| ✅ (Google API) | ❌ | ⚠️ (SMTP basic) | ✅ (Gmail API) | ⚠️ (IMAP) | **✅ (IMAP/Gmail Invariant)**|
| Slack / Discord | ✅ (Slack/Disc) | ✅ (Slack) | ❌ | ❌ | ⚠️ (Webhooks) | ❌ | **✅ (MIRA 8-Channel Bus)** |
| **PRODUCTIVITY** | | | | | | | |
| Calendar Synchronization| ✅ (CalDAV/GCal) | ✅ (Google Cal) | ❌ | ⚠️ (Local JSON) | ✅ (Google Cal) | ✅ (GCal) | **✅ (Calendar Matrix)** |
| Docs / Sheets / Notion | ✅ (Office/SAP) | ✅ (Full Suite) | ❌ | ❌ | ⚠️ (Vault docs) | ❌ | **✅ (Connector Layer)** |
| Attendance Tracking | ❌ | ❌ | ❌ | ❌ | ⚠️ (Exams/Vault)| ❌ | **✅ (Real Attendance Engine)**|
| **COMPUTER CONTROL** | | | | | | | |
| Desktop Observation | ✅ (VNC/Xdotool)| ❌ | ✅ (Go Sidecar) | ⚠️ (OpenCV) | ✅ (Screen OCR) | ✅ (OpenClaw) | **✅ (Wayland Layer)** |
| Real Browser Control | ✅ (Playwright) | ✅ (Playwright) | ✅ (Sidecar CDP)| ❌ | ✅ (Playwright) | ✅ (OpenClaw) | **✅ (Native Chromium)** |
| Native Sidecars | ❌ (Client/Srv) | ❌ | ✅ (Go Agent) | ❌ | ❌ | ❌ | **✅ (Native Daemon)** |
| **PERCEPTION & VISION**| | | | | | | |
| Screen OCR & Vision | ✅ (Tesseract) | ❌ | ✅ (OCR Pipeline)| ⚠️ (MediaPipe) | ✅ (Vision OCR) | ⚠️ (Screenshots)| **✅ (Native OCR Service)** |
| Face & Emotion Detection| ❌ | ❌ | ❌ | ✅ (MediaPipe) | ❌ | ❌ | **✅ (Perception Daemon)** |
| **VOICE INTERACTION** | | | | | | | |
| Full-Duplex Voice | ❌ (Turn-based) | ❌ | ❌ | ✅ (Gemini Live)| ⚠️ (Web Audio) | ❌ | **✅ (PipeWire Duplex)** |
| Interruption Support | ❌ | ❌ | ❌ | ✅ (Streaming) | ❌ | ❌ | **✅ (Live Mic Cut-off)** |
| Offline STT / TTS | ⚠️ (Local LLM) | ❌ | ❌ | ❌ | ⚠️ (Whisper-cpp)| ✅ (Vosk small) | **✅ (Offline Edge Fallback)**|
| **SECURITY & SOVEREIGNTY**| | | | | | | |
| Permission / Approval Gate| ⚠️ (Config-based)| ❌ (Ambient auth)| ✅ (Authority Engine)| ❌ | ✅ (ActionBroker)| ⚠️ (Guardrails)| **✅ (PolicyGate Invariant)** |
| Cryptographic Audit Ledger| ⚠️ (Text logs) | ⚠️ (SQLite log) | ✅ (Signed trace)| ❌ | ✅ (Audit DB) | ⚠️ (Logs) | **✅ (SHA-256 Block Ledger)** |
| Sandboxed Execution | ✅ (Docker/Seccomp)| ❌ | ⚠️ (OS user) | ❌ | ⚠️ (Isolated proc)| ⚠️ (Docker) | **✅ (Linux Cgroups/Pledge)** |
| PII & Injection Defense | ✅ (EgressGuard) | ❌ | ⚠️ (Basic) | ❌ | ⚠️ (Sanitizer) | ✅ (Guardrails) | **✅ (Pre-Dispatch Sanitizer)**|
| **UI & USER EXPERIENCE**| | | | | | | |
| Tactical Holographic HUD| ❌ (Vue dashboard)| ❌ (CLI/Web) | ⚠️ (Electron) | ✅ (3D Three.js) | ✅ (Svelte HUD) | ❌ (Telegram UI)| **✅ (60 FPS Arc Reactor HUD)**|
| Wayland / Modern Desktop| ❌ (Web browser) | ❌ (Web browser)| ⚠️ (Electron win)| ⚠️ (PyQt window)| ⚠️ (Web/PWA) | ❌ (Headless) | **✅ (Hyprland / Waybar)** |
