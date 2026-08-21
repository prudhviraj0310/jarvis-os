# JARVIS OS — Next-Generation Reference Architecture

This architecture synthesizes the strongest patterns discovered across the open-source landscape while preserving the foundational core principle of JARVIS OS:

```
============================================================
             MACHINE SOVEREIGNTY INVARIANT
============================================================
                 MODEL ≠ AUTHORITY

           The LLM proposes.
           The policy decides.
           The execution layer acts.
           The machine verifies.
============================================================
```

---

## 🏛️ End-to-End System Data Flow

```
                         JARVIS EXPERIENCE
                                 │
            ┌────────────────────┼────────────────────┐
            ↓                    ↓                    ↓
      Voice Matrix      Holographic HUD     Multi-Channel Gateway
    (PipeWire Duplex)    (Wayland Layer)    (WhatsApp/Mail/Slack)
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 ↓
                          CONTEXT ENGINE
              (Morning Briefing, Schedule, Attendance 87.5%)
                                 ↓
                         PERSONAL MEMORY
             (Knowledge Graph, [OBSERVED] vs [INFERRED])
                                 ↓
                       INTENT / EVENT ROUTER
               (Fast Edge <10ms vs Deep Reasoner <50ms)
                                 ↓
                        AGENT ORCHESTRATOR
                    (MIRA Dynamic Task Graph)
                                 ↓
                           POLICY BROKER
              (Read-Only / Safe vs Consequential Confirmation)
                                 ↓
                          TOOL REGISTRY
             (Sandboxed Native Capabilities & MCP Tools)
                                 ↓
            ┌────────────────────┼────────────────────┐
            ↓                    ↓                    ↓
     Desktop Sidecar      Browser Engine      External Services
     (Wayland Control)    (Real Chromium)     (WhatsApp / Gmail)
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 ↓
                         VERIFICATION GATE
                   (Pre- & Post-Execution Proofs)
                                 ↓
                          JOURNAL SERVICE
              (Cryptographic SHA-256 Block Ledger)
```

---

## 🧩 Architectural Subsystem Breakdown

### 1. Ingestion & Experience Layer
* **Voice Matrix**: PipeWire duplex audio capture + live interruption VAD stream + local Vosk / cloud streaming TTS.
* **Holographic HUD**: Wayland-native glassmorphic layer surface rendering the 60 FPS vector Arc Reactor, Morning Briefing, and active action proposal cards.
* **Multi-Channel Gateway**: Unified inbound channel bus (WhatsApp Baileys, Gmail IMAP, Telegram, Discord).

### 2. Context Engine & Memory Subsystem
* **Context Engine**: Continuously aggregates daily calendar agendas, unread emails, incoming WhatsApp commitments, and academic attendance into a real-time executive state.
* **Personal Memory & Knowledge Graph**: Persistent entity graph with strict provenance tagging (`[OBSERVED]`, `[DERIVED]`, `[INFERRED, confidence=0.88]`).

### 3. Intelligence, Planning & Auto-Routing
* **Dual-Tier Model Router**: Auto-routes low-latency commands (<10ms) to local edge classifiers, and complex multi-step planning (<50ms) to reasoning LLMs with offline resilience.
* **MIRA Orchestrator**: Manages proactive companion check-ins, deadline countdowns, and automated action proposals.

### 4. Machine Sovereignty & Policy Guard
* **PolicyGate**: Deterministic enforcement layer classifying all actions:
  * `Allowed`: Local reads, clock, status telemetry, audio volume, UI switches.
  * `ConfirmRequired`: Outbound WhatsApp messages, sending emails, terminal execution, filesystem mutations, calendar alterations.
* **Action Confirmation Gate**: Generates a modal dialog with draft preview before any execution.

### 5. Execution & Verification Layer
* **Tool Registry & MCP Host**: Dispatches verified payloads to sandboxed execution workers (Chromium CDP, terminal PTY, local connectors).
* **JournalService**: Appends SHA-256 cryptographic proofs to `/var/log/jarvis_journal.log` verifying that every single executed action was authorized.
