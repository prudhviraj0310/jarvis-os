# JARVIS OS — Final Integration Candidates & Tier Ranking

This document evaluates and ranks components extracted from the 6 surveyed repositories for clean-room implementation into JARVIS OS.

---

## 🏆 Component Tier Ranking

### 🌟 S-TIER (Crucial to Core Vision — High Priority)
1. **Baileys-Based Sandboxed WhatsApp Multi-Device Bridge** (`kar-ganap/jarvis`)
2. **Deterministic Action Confirmation & Policy Broker** (`LakshyaBadjatya/Friday` & `yashvar23/jarvis`)
3. **Full-Duplex Voice with Live Interruption** (`Raghava001-web/Jarvis`)
4. **Offline Zero-Cloud Voice STT (Vosk/Whisper.cpp)** (`ambartsumov/jarvis-agent`)
5. **Personal Memory Wiki & Provenance Matrix** (`LakshyaBadjatya/Friday` & `MIRA`)

### 🥇 A-TIER (Highly Useful Capabilities)
6. **IMAP/Gmail Inbox Deliverable Classifier & Auto-Drafter** (`dev-core-busy/jarvis`)
7. **Dual-Tier Model Auto-Router (<10ms Edge vs <50ms Deep Reasoning)** (`dev-core-busy/jarvis` & `MIRA`)
8. **Desktop Awareness & Active Window Inspector** (`yashvar23/jarvis`)
9. **Curated Morning Intelligence Briefing Aggregator** (`Raghava001-web/Jarvis` & `Friday`)

### 🥈 B-TIER (Valuable Optional Enhancements)
10. **MediaPipe Hand Gesture & Face Emotion Perception** (`Raghava001-web/Jarvis`)
11. **OpenClaw Multi-Agent Web Automation Bridge** (`ambartsumov/jarvis-agent`)
12. **Office / Notion / Todoist Productivity Connectors** (`kar-ganap/jarvis`)

### 🥉 C-TIER (Reference & Conceptual Study Only)
13. **Enterprise SAP / JIRA / Confluence Connectors** (`dev-core-busy/jarvis`)
14. **Stock Market Order Execution** (`Friday`)

---

## 🔍 Deep Dive on S-Tier Components

---

### 1. Baileys Sandboxed WhatsApp Multi-Device Bridge
* **Inspired by**: `kar-ganap/jarvis` (`bridge/whatsapp/`)
* **Problem it solves**: Enables personal WhatsApp message ingestion, intent parsing, and outbound sending without requiring expensive official Meta Business API tokens.
* **Why it is better**: Uses the real WhatsApp multi-device web protocol.
* **Action Strategy**: **ADAPT / SANDBOX**. Package the Node.js Baileys engine inside a dedicated isolated daemon (`jarvis-whatsapp-bridge`) communicating over localhost Unix sockets.
* **Dependencies**: Node.js, `@whiskeysockets/baileys`.
* **OS Architecture Impact**: Fully compliant; runs as a confined system service.
* **License**: MIT (Permissive).
* **Architectural Location**: `Userland/Services/JarvisConnectors/WhatsAppBridge/`.

---

### 2. Deterministic Action Confirmation & Policy Broker
* **Inspired by**: `LakshyaBadjatya/Friday` (`action_broker.py`) & `yashvar23/jarvis` (`src/authority/`)
* **Problem it solves**: Prevents the LLM from executing destructive actions (sending unverified emails, modifying files, executing terminal commands) without explicit human confirmation.
* **Why it is better**: Upholds the **Machine Sovereignty Invariant**: `Model != Authority`.
* **Action Strategy**: **REIMPLEMENT (Clean-Room Native C++ / Rust)**.
* **Dependencies**: None (native OS capability).
* **OS Architecture Impact**: Core to kernel and userland security.
* **License**: MIT / Architecture Pattern.
* **Architectural Location**: `Userland/Services/JarvisService/PolicyGate.cpp`.

---

### 3. Full-Duplex Voice with Live Interruption
* **Inspired by**: `Raghava001-web/Jarvis` (`gemini_live_engine.py`)
* **Problem it solves**: Traditional voice assistants make you wait until they finish talking before you can speak. Full-duplex allows instant voice interruption.
* **Why it is better**: Transforms the assistant into a natural, conversational partner.
* **Action Strategy**: **REIMPLEMENT (Native PipeWire / WebRTC Stream)**.
* **Dependencies**: PipeWire audio buffer or Web Speech / WebSocket stream.
* **OS Architecture Impact**: Fully compliant with Wayland audio layer.
* **License**: MIT.
* **Architectural Location**: `Userland/Services/JarvisVoice/VoiceMatrix.cpp`.

---

### 4. Offline Zero-Cloud Voice STT (Vosk / Whisper.cpp)
* **Inspired by**: `ambartsumov/jarvis-agent` (`vosk/voice_server.py`)
* **Problem it solves**: Allows basic voice commands (`"Open browser"`, `"Morning briefing"`, `"Handle it"`) to work 100% offline with zero cloud latency and total privacy.
* **Why it is better**: Works without an internet connection.
* **Action Strategy**: **ADAPT / REIMPLEMENT**.
* **Dependencies**: `vosk-api` or `whisper.cpp`.
* **OS Architecture Impact**: Native local daemon.
* **License**: MIT / Apache 2.0.
* **Architectural Location**: `Userland/Services/JarvisVoice/OfflineSTT.cpp`.

---

### 5. Personal Memory Wiki & Provenance Matrix
* **Inspired by**: `LakshyaBadjatya/Friday` (`src/friday/vault/`) & `MIRA` (`MIRAMemoryWiki`)
* **Problem it solves**: Separates verified user facts (`[OBSERVED]`) from LLM assumptions (`[INFERRED, confidence=0.88]`), eliminating hallucinations.
* **Why it is better**: Provides transparent auditability for memory recall.
* **Action Strategy**: **REIMPLEMENT (Native C++ / SQLite / JSON Vault)**.
* **Dependencies**: None (native SQLite or structured JSON).
* **OS Architecture Impact**: Core to personal context engine.
* **License**: MIT.
* **Architectural Location**: `Userland/Services/JarvisService/PersonalMemory.cpp`.
