# Capability Blueprint: WhatsApp Intelligence

- **Inspired by**: `kar-ganap/jarvis` (Baileys Node.js Bridge), `dev-core-busy/jarvis` (WhatsApp Skill), `ambartsumov/jarvis-agent` (Guardrails)

---

## 1. Core Architecture
Personal WhatsApp integration requires interacting with WhatsApp Web protocol rather than the restricted Meta Cloud API for business.

```
WhatsApp Mobile Device (Linked via QR Code)
       ↕ (Multi-Device WebSockets)
Local Baileys Node.js Service (Isolated Sandboxed Process)
       ↕ (Localhost REST / WebSocket IPC)
JARVIS WhatsAppConnector (Native C++ / Python Daemon)
       ↓
Conversation Parser & Intent Classifier
       ↓
Draft Generator (Persona-Tuned)
       ↓
PolicyGate (Action Proposal ACT-WA-001)
       ↓ (Human Confirmation)
Outbound Send Message
```

---

## 2. Ingestion & Importance Classifier
* **High Priority / Actionable Criteria**:
  * Sender matches `ContactGraph` close circle (peers, teammates, family).
  * NLP Intent matches `REQUEST_FILES`, `MEETING_CONFIRMATION`, `DEADLINE_QUERY`, `EMERGENCY`.
* **Low Priority / Muted**: Group chatter, automated service notifications, marketing.

---

## 3. Two-Step Safe Action Execution
* The assistant never sends messages automatically. It produces structured action cards:
  ```json
  {
    "action_id": "ACT-WA-001",
    "recipient": "Rahul Sharma (+91-98765-43210)",
    "intent": "REQUEST_FILES",
    "proposed_draft": "Yes, I will send it tomorrow before noon.",
    "persona_confidence": 0.88,
    "status": "AWAITING_CONFIRMATION"
  }
  ```
