# JARVIS OS — Extracted Architectural Patterns from Open Source

This document distills the top 6 architectural patterns identified across the 6 surveyed open-source systems.

---

### PATTERN 1: Central Daemon & Decoupled Channel Bus (from *kar-ganap* & *dev-core-busy*)
```
Channel Ingestion (WhatsApp / Email / Telegram / Discord / Voice)
       ↓
Unified Inbound Event Struct (Sender, Timestamp, Content, RawPayload)
       ↓
Intent Router (Fast Local Cosine Classifier / Semantic Rule Engine)
       ↓
Agent Planner & Context Synthesis
       ↓
Capability / Tool Registry
       ↓
Security & Confirmation Gate
       ↓
Native Execution Engine (System Services / Network APIs)
```
* **Why it matters**: The central intelligence layer never hard-codes protocol details for WhatsApp, IMAP, or Telegram. It receives normalized `IncomingMessage` events and outputs normalized `ActionProposal` structs.

---

### PATTERN 2: Native Machine Sidecars & Execution Confinement (from *yashvar23*)
```
Central JARVIS Daemon (IPC Server / Unix Socket / D-Bus)
       ↓  (Cryptographically Signed JSON-RPC / Protobuf)
Machine Sidecar (Native C++ / Go / Rust process with OS privileges)
       ↓
[Desktop Observer]  [Window Compositor]  [Chromium CDP]  [Terminal PTY]
```
* **Why it matters**: Keeps the heavy agent and LLM planning processes decoupled from raw OS kernel calls. The sidecar enforces strict local sandboxing and process privilege drops.

---

### PATTERN 3: Personal Memory, Contact Graph & Provenance Tagging (from *Friday* & *MIRA*)
```
Raw Inbound Stream (Messages, Emails, Calendar Events, Documents)
       ↓
Continuous Reflection & Entity Extractor
       ↓
┌─────────────────────────────────────────────────────────────┐
│ PERSISTENT KNOWLEDGE GRAPH & PERSONAL MEMORY                │
│ • User Profile (Identity, Attendance, Deadlines, Goals)     │
│ • Contact & Circle Graph (Relationship, Trust, History)     │
│ • Explicit Facts: [OBSERVED] (Timestamps, Exact Quotes)     │
│ • Inferred Patterns: [INFERRED, confidence=0.88] (Tone)     │
└─────────────────────────────────────────────────────────────┘
       ↓
Context Engine (Generates synthesized morning briefings & prompt context)
```
* **Why it matters**: Prevents LLM hallucinations by enforcing strict provenance metadata (`[OBSERVED]` vs `[DERIVED]` vs `[INFERRED]`).

---

### PATTERN 4: Two-Step Event-Driven Automation & Confirmation Gate (from *yashvar23* & *Friday*)
```
Event Trigger (Email received / Deadline approaching / WhatsApp unread)
       ↓
Automation Engine generates Action Proposal (e.g. ACT-WA-001)
       ↓
PolicyGate Classification:
   ├── Read-Only / Safe → Auto-Executes & Logs
   └── Consequential (Send Message, Delete File, Terminal Exec)
          ↓
       UI Confirmation Gate (Modal Dialog / Voice Affirmation)
          ↓
       [User Rejects] → Action Discarded
       [User Approves] → Dispatched to Native Connector
          ↓
       SHA-256 Block Ledger (/var/log/jarvis_journal.log)
```
* **Why it matters**: Upholds the **Machine Sovereignty Invariant**: `Model != Authority`. The AI proposes drafts, but only the human authorizes execution.

---

### PATTERN 5: Full-Duplex Streaming Voice Matrix with Interruption (from *Raghava001*)
```
Host Microphone (PipeWire / ALSA Stream / CoreAudio)
       ↓
Voice Activity Detector (VAD) + Live PCM Ring Buffer
       ↓
Streaming STT (Vosk Offline / Whisper / Gemini Live WebSocket)
       ↓
Text-to-Speech Output Stream (Audio Sink)
       ↑ (When VAD detects user speaking during TTS playback)
   INTERRUPTION SIGNAL: Instantly pauses audio sink & flushes buffer
```
* **Why it matters**: Gives JARVIS a conversational feel where the user can interrupt the assistant naturally.

---

### PATTERN 6: Dual-Tier Model Auto-Routing with Offline Edge Resilience (from *dev-core-busy* & *ambartsumov*)
```
Incoming Command / Request
       ↓
Complexity & Latency Evaluator:
   ├── Tier 1 (Fast Edge <10ms): Status, Volume, Clock, UI Toggle
   │     ↳ Handled locally via Vector Intent Cache or Small Edge Model
   └── Tier 2 (Deep Reasoning <50ms): Multi-step Synthesis, Replanning
         ↳ Handled via Advanced LLM (Claude 3.5 / GPT-4o / DeepSeek)
         ↳ (If Network Offline) → Gracefully falls back to Local Ollama/Edge
```
* **Why it matters**: Reduces latency, eliminates cloud API bills for basic tasks, and ensures the OS remains functional during network dropouts.
